"""建立 GitHub Pages artifact：保留講義的相對連結，不執行任何部署。"""
from pathlib import Path
import shutil
from publication import ROOT, PACKAGES, public_files, ensure_public, ASSETS
from check_release import check, check_links


def build(root=ROOT):
    root = Path(root).resolve()
    for name in [*PACKAGES, 'manifest.json']:
        if not (root / 'dist' / name).is_file():
            raise ValueError('Pages 缺少必要下載檔：dist/' + name)
    check(root, write_report=False)
    selected = []
    for path in public_files(root):
        relative = path.relative_to(root)
        parts = relative.parts
        if parts[0] in {'examples', 'dist', 'docs', 'qa'} or parts[:2] == ('.agents', 'skills'):
            selected.append(path)
        elif len(parts) == 1 and path.name in {'index.html', 'README.md', 'ACCEPTANCE.md', 'LICENSE', 'requirements.txt'}:
            selected.append(path)
        elif parts[0] == 'handbook' and (path.suffix == '.html' or len(parts) > 2 and parts[1] == 'assets' and path.suffix in ASSETS):
            selected.append(path)
    ensure_public(selected, root)
    destination = root / '.work/pages-site'
    # 固定且驗證後的工作區內 staging，清除舊 artifact 防止殘留私人檔案。
    if not destination.resolve().is_relative_to(root / '.work') or destination.is_symlink():
        raise ValueError('Pages 暫存目錄必須位於本工作區的 .work 內')
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for path in selected:
        target = destination / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    (destination / '.nojekyll').touch()
    count = check_links(destination)
    print(f'Pages artifact：.work/pages-site；已驗證 {count} 個本機相對連結。此步驟尚未部署。')
    return destination


if __name__ == '__main__':
    build()
