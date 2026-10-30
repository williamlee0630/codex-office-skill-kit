"""公開檔案白名單與隱私檢查；不連線、不發布、不讀取個人來源。"""
from datetime import datetime, timezone, timedelta
from io import BytesIO
from pathlib import Path, PurePosixPath
import argparse
import json
import os
import re
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.1.0'
PACKAGES = (f'practice-data-{VERSION}.zip', f'office-skills-{VERSION}.zip', f'codex-office-skill-kit-{VERSION}.zip')
ROOT_FILES = {'README.md', 'ACCEPTANCE.md', 'AGENTS.md', 'LICENSE', 'requirements.txt', '.gitignore', '.gitattributes', 'index.html', '.nojekyll'}
PUBLIC_DOCS = {'INSTALL.md', 'DEVELOPMENT.md', 'ACCEPTANCE.md', 'PROGRESS.md', 'CHANGELOG.md', 'OFFICIAL_SOURCES.md', 'DESIGN.md', 'USER_REQUEST.md', 'IMPLEMENTATION_PLAN.md', 'DEPLOYMENT_PLAN.md'}
EXCLUDED = {'__pycache__', '.tmp', '.work', '.git', '.venv', 'venv', 'node_modules', '.codex', '.aws', '.cache', 'office-render'}
TEXT = {'.md', '.txt', '.json', '.csv', '.tsv', '.py', '.ps1', '.yaml', '.yml', '.html', '.css', '.js', '.xml', '.rels', '.eml', '.svg', '.toml'}
ASSETS = {'.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.woff', '.woff2'}
EXAMPLE_TYPES = TEXT | {'.xlsx', '.docx', '.pptx', '.pdf', '.png', '.jpg', '.jpeg'}
HOME = re.compile(r'(?i)(?:[a-z]:[\\/]+Users[\\/]+[^\\/\s"<>]+|/(?:home|Users)/[^/\s"<>]+)')
EMAIL = re.compile(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}')
TOKEN = re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----)')
ASSIGNED_SECRET = re.compile(r'''(?im)["']?(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)["']?\s*[:=]\s*["']([^"'\r\n]{12,})["']''')


def taipei_date():
    return datetime.now(timezone(timedelta(hours=8))).date().isoformat()


def excluded(relative):
    lower = [part.lower() for part in PurePosixPath(relative).parts]
    return (any(part in EXCLUDED or part.startswith('.test-') for part in lower)
            or any(part.startswith(('.env', 'local-settings', '~$', 'credentials', 'secrets.')) for part in lower)
            or any(part.endswith(('.log', '.pyc', '.pyo', '.pem', '.key', '.p12', '.pfx')) for part in lower)
            or ('docs' in lower and 'qa' in lower)
            or ('qa' in lower and any(part.startswith(('raw-', 'environment', 'run-logs')) or 'events' in part for part in lower))
            or any(part in {'credentials', 'credentials.json', 'token.json', 'secrets.json'} for part in lower))


def public_files(root=ROOT):
    """回傳可加入公開 Git 的 Path 清單；不納入白名單以外檔案。"""
    root = Path(root).resolve()
    selected = []
    candidates = []
    for directory, folders, names in os.walk(root, followlinks=False):
        folder = Path(directory)
        folders[:] = sorted(name for name in folders if not excluded((folder / name).relative_to(root).as_posix()))
        candidates.extend(folder / name for name in names)
    for path in sorted(candidates):
        relative = path.relative_to(root).as_posix()
        if excluded(relative):
            continue
        parts = PurePosixPath(relative).parts
        accepted = relative in ROOT_FILES
        accepted |= len(parts) == 2 and parts[0] == 'docs' and parts[1] in PUBLIC_DOCS
        accepted |= len(parts) == 2 and parts[0] == 'qa' and path.suffix in {'.md', '.json'}
        accepted |= len(parts) == 2 and parts[0] == 'dist' and parts[1] in {*PACKAGES, 'manifest.json'}
        accepted |= parts[:2] == ('.agents', 'skills') and path.suffix in EXAMPLE_TYPES
        accepted |= parts[0] == 'examples' and path.suffix in EXAMPLE_TYPES
        accepted |= parts[0] == 'tools' and len(parts) == 2 and path.suffix in {'.py', '.ps1'}
        accepted |= parts[0] == 'tests' and path.suffix in {'.py', '.md'}
        accepted |= parts[0] == 'handbook' and (path.suffix in {'.html', '.md', '.py'} or len(parts) > 2 and parts[1] == 'assets' and path.suffix in ASSETS)
        accepted |= parts[:2] == ('.github', 'workflows') and len(parts) == 3 and path.suffix in {'.yml', '.yaml'}
        if accepted:
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError('公開檔案不得使用連往工作區外的連結：' + relative)
            selected.append(path)
    return selected


def _scan_text(text, label):
    issues = []
    normalized = re.sub(r'\\{2,}', lambda match: chr(92), text)
    if HOME.search(normalized):
        issues.append(label + '：含個人家目錄絕對路徑')
    if TOKEN.search(text) or ASSIGNED_SECRET.search(text):
        issues.append(label + '：含疑似憑證或金鑰')
    for match in EMAIL.finditer(text):
        domain = match.group(0).rsplit('@', 1)[1].lower()
        if domain not in {'example.invalid', 'example.com', 'example.org', 'users.noreply.github.com', 'noreply.github.com'}:
            issues.append(label + '：含未允許的私人電子郵件')
            break
    return issues


def scan(path_or_data, label=None, _depth=0):
    """回傳不含私密值的問題清單；掃描檔案或 bytes，遞迴 ZIP／OOXML。"""
    if isinstance(path_or_data, (str, Path)):
        path = Path(path_or_data)
        data = path.read_bytes()
        label = label or path.name
    else:
        data = bytes(path_or_data)
        label = label or '資料'
    if _scan_text(label, '檔名'):
        label = '[隱私檔名]'
    encoding = 'utf-16' if data.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8'
    is_archive = data.startswith((b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'))
    # 壓縮資料不是文字；掃描展開內容與中繼資料，避免隨機位元組被誤認成信箱。
    issues = [] if is_archive else _scan_text(data.decode(encoding, errors='ignore'), label)
    if is_archive:
        if _depth >= 8:
            return issues + [label + '：ZIP巢狀深度超過限制']
        try:
            with ZipFile(BytesIO(data)) as archive:
                issues.extend(_scan_text(archive.comment.decode('utf-8', errors='ignore'), label + '：ZIP註解'))
                infos = archive.infolist()
                if len(infos) > 20000 or sum(info.file_size for info in infos) > 256 * 1024 * 1024:
                    return issues + [label + '：ZIP展開大小超過安全上限']
                if archive.testzip() is not None:
                    issues.append(label + '：ZIP CRC檢查失敗')
                if len(infos) != len({info.filename for info in infos}):
                    issues.append(label + '：ZIP含重複路徑')
                for info in infos:
                    name = info.filename
                    if name.startswith(('/', chr(92))) or '..' in PurePosixPath(name.replace(chr(92), '/')).parts or re.match(r'^[A-Za-z]:', name):
                        issues.append(label + '：ZIP含不安全路徑')
                    if excluded(name):
                        issues.append(label + '：ZIP含禁止公開的檔案類型或目錄')
                    issues.extend(_scan_text(name, label + '：ZIP檔名'))
                    issues.extend(_scan_text(info.comment.decode('utf-8', errors='ignore'), label + '：ZIP項目註解'))
                    if not info.is_dir():
                        issues.extend(scan(archive.read(info), label + '!' + name, _depth + 1))
        except (BadZipFile, RuntimeError, NotImplementedError, OSError) as error:
            issues.append(label + '：ZIP無法完整檢查（' + type(error).__name__ + '）')
    return list(dict.fromkeys(issues))


def ensure_public(files, root=ROOT):
    problems = []
    for path in files:
        relative = Path(path).relative_to(root).as_posix()
        problems.extend(_scan_text(relative, '公開檔名'))
        problems.extend(scan(path, label=relative))
    if problems:
        raise ValueError('公開隱私檢查失敗：\n' + '\n'.join(problems))


def _portable(text, root):
    for prefix in sorted({str(root), root.as_posix(), str(root).replace(chr(92), chr(92) * 2)}, key=len, reverse=True):
        text = text.replace(prefix + (chr(92) * 2 if chr(92) * 2 in prefix else chr(92)), '')
        text = text.replace(prefix + '/', '')
    return text


def _sanitize_json(text, root, path):
    data = json.loads(text)
    def convert(value, key=''):
        if isinstance(value, dict):
            return {name: convert(item, name) for name, item in value.items()}
        if isinstance(value, list):
            return [convert(item) for item in value]
        if not isinstance(value, str):
            return value
        updated = _portable(value, root)
        if key in {'pdftoppm_path', 'tesseract_path'} and HOME.search(updated):
            return re.split(r'[\\/]+', updated)[-1]
        if key == 'preserved_path' and updated.startswith(('.work/', '.work' + chr(92))):
            actual = path.parent / 'originals' / re.split(r'[\\/]+', updated)[-1]
            if actual.is_file():
                return actual.relative_to(root).as_posix()
        if updated != value:
            return updated.replace(chr(92), '/')
        return updated
    converted = convert(data)
    return json.dumps(converted, ensure_ascii=False, indent=2) + '\n' if converted != data else text


def sanitize_examples(root=ROOT):
    """只整理本專案 examples 模擬素材；先備份，保留來源與數字，不碰其他資料。"""
    root = Path(root).resolve()
    planned = []
    for path in public_files(root):
        relative = path.relative_to(root)
        if relative.parts[0] != 'examples':
            continue
        original = path.read_bytes()
        updated = original
        if path.suffix in TEXT:
            text = original.decode('utf-8')
            text = _sanitize_json(text, root, path) if path.suffix == '.json' else _portable(text, root)
            if path.suffix in {'.csv', '.md'} and text != original.decode('utf-8'):
                text = re.sub(r'((?:examples|\.agents)[\\/][^\r\n,<>]*)', lambda m: m.group(0).replace(chr(92), '/'), text)
            updated = text.encode('utf-8')
        elif path.suffix in {'.xlsx', '.docx', '.pptx'}:
            buffer = BytesIO()
            with ZipFile(BytesIO(original)) as source, ZipFile(buffer, 'w', ZIP_DEFLATED) as target:
                changed = False
                for info in source.infolist():
                    data = source.read(info)
                    if info.filename.endswith(('.xml', '.rels')):
                        portable = _portable(data.decode('utf-8'), root)
                        portable = re.sub(r'((?:examples|\.agents)[\\/][^<>]*)', lambda m: m.group(0).replace(chr(92), '/'), portable)
                        changed |= portable.encode('utf-8') != data
                        data = portable.encode('utf-8')
                    target.writestr(info, data)
            if changed:
                updated = buffer.getvalue()
        if updated != original:
            problems = scan(updated, label=relative.as_posix())
            if problems:
                raise ValueError('模擬資料整理後仍有待人工確認的隱私問題：\n' + '\n'.join(problems))
            planned.append((path, relative, original, updated))
    for path, relative, original, updated in planned:
        backup = root / '.work/publication-backup' / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            backup.write_bytes(original)
        path.write_bytes(updated)
    return [relative.as_posix() for _, relative, _, _ in planned]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='公開白名單與隱私檢查；模擬資料整理先保存本機備份。')
    parser.add_argument('--sanitize-examples', action='store_true')
    parser.add_argument('--list', action='store_true', help='逐行列出可加入 Git 的相對路徑')
    args = parser.parse_args()
    if args.sanitize_examples:
        print(json.dumps({'整理的模擬檔案': sanitize_examples()}, ensure_ascii=False, indent=2))
    files = public_files()
    ensure_public(files)
    if args.list:
        print('\n'.join(path.relative_to(ROOT).as_posix() for path in files))
    else:
        print(f'公開白名單 {len(files)} 個檔案通過隱私檢查；此結果不代表已發布。')
