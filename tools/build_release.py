"""從同一份公開白名單建立三種本機發行 ZIP；不連線、不發布。"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import re
from publication import ROOT, VERSION, PACKAGES, public_files, ensure_public, scan, taipei_date


def create_zip(path, files, extras=None):
    entries = {name: source.read_bytes() for source, name in files}
    for name, content in (extras or {}).items():
        entries[name] = content.encode('utf-8') if isinstance(content, str) else content
    for name, data in entries.items():
        problems = scan(data, label=name)
        if problems:
            raise ValueError('\n'.join(problems))
    with ZipFile(path, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP完整性檢查失敗：' + path.name)
        return {'name': path.name, 'bytes': path.stat().st_size, 'file_count': len(archive.namelist()),
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def _offline_text(path, root):
    text = path.read_text(encoding='utf-8')
    full_name = PACKAGES[2]
    if path.suffix == '.html':
        text = re.sub(r'<a\b([^>]*?)href=["\x27][^"\x27]*' + re.escape(full_name) + r'["\x27]([^>]*)>.*?</a>',
                      '<a href="../README.md">完整工具包（目前已解壓；返回使用說明）</a>', text, flags=re.S)
    elif path.name == 'README.md' and path.parent == root:
        text = re.sub(r'\[([^\]]+)\]\([^)]*' + re.escape(full_name) + r'\)',
                      '完整學員工具包（目前已解壓的這一包）', text)
    return text


def build(root=ROOT):
    root = Path(root).resolve()
    for name in ['README.md', 'ACCEPTANCE.md', 'AGENTS.md', 'LICENSE', 'requirements.txt',
                 'handbook/index.html', 'index.html']:
        if not (root / name).is_file():
            raise ValueError('發行缺少必要公開檔案：' + name)
    if not any((root / 'qa').glob('*.md')) and not any((root / 'qa').glob('*.json')):
        raise ValueError('發行缺少 qa/ 可公開驗收摘要')
    selected = [path for path in public_files(root) if path.relative_to(root).parts[0] != 'dist']
    ensure_public(selected, root)
    dist = root / 'dist'
    dist.mkdir(exist_ok=True)
    relative = lambda path: path.relative_to(root).as_posix()
    examples = [(p, relative(p)) for p in selected if relative(p).startswith('examples/')]
    practice = create_zip(dist / PACKAGES[0], examples, {'使用說明.txt': '此包全部為原創模擬資料。來源與待確認事項均保留；請搭配完整工具包講義練習。\n'})
    light = []
    for path in selected:
        name = relative(path)
        if (name.startswith(('.agents/skills/', 'examples/', 'tools/'))
                or name in {'requirements.txt', 'LICENSE', 'docs/INSTALL.md', 'docs/DEVELOPMENT.md', 'docs/OFFICIAL_SOURCES.md'}):
            light.append((path, name))
        elif name.startswith('tests/') and path.suffix == '.py' and not (path.name.startswith('test_handbook') or path.name == 'test_publication.py'):
            light.append((path, name))
    skills = create_zip(dist / PACKAGES[1], light, {'README.md': '''# AI 辦公室技能安裝包 1.1.0

此包包含十個完整技能、原創模擬資料與程式測試。完整講義請使用完整學員工具包。
安裝並載入技能 → 送出 $技能名稱 → 依引導說明工作或提供素材 → 必要時補答 → 開啟並核對成果。
可把完整技能資料夾帶到一般工作區。Codex 自行檢查環境、整理資料與產檔，不要求讀 MD、回報路徑、編輯 JSON 或貼長提示詞。
模擬資料僅明確要求示範時使用；既有目的、素材與補答沿用，不重問。
測試：python -m unittest discover -s tests -v（此包不含講義與公開發行測試）。
所有模擬案例均須核對原始來源；草稿不寄送，未知資訊與待確認事項不補猜。
tools/install_skills.py 預設預覽，--apply 才複製；同名技能拒絕覆寫。
'''})
    manifest = {'version': VERSION, 'date': taipei_date(), 'scope': 'embedded-components', 'packages': [practice, skills]}
    manifest_path = dist / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    full_files = [(path, 'codex-office-skill-kit/' + relative(path)) for path in selected]
    full_files += [(dist / name, 'codex-office-skill-kit/dist/' + name) for name in [PACKAGES[0], PACKAGES[1], 'manifest.json']]
    extras = {'codex-office-skill-kit/' + relative(path): _offline_text(path, root)
              for path in selected if path.suffix == '.html' or path == root / 'README.md'}
    full = create_zip(dist / PACKAGES[2], full_files, extras)
    manifest['packages'].append(full)
    manifest['scope'] = 'complete-release'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for package in manifest['packages']:
        print(f'{package["name"]}：{package["file_count"]} 個檔案，{package["bytes"]} bytes，SHA256 {package["sha256"]}')
    return manifest


if __name__ == '__main__':
    build()
