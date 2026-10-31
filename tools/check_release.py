"""驗證實際 ZIP 的 CRC、SHA-256、隱私、九技能與完整本機連結。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile
import hashlib
import json
import posixpath
import re
from publication import ROOT, VERSION, PACKAGES, SKILLS, scan


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.add(data['id'])
        for key in ['href', 'src']:
            if data.get(key):
                self.links.append(data[key])
        if tag == 'meta' and data.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url\s*=\s*(.+)', data.get('content', ''), re.I)
            if match:
                self.links.append(match.group(1).strip(' "' + chr(39)))


def _check_documents(files):
    parsed = {}
    for name, data in files.items():
        if name.endswith('.html'):
            document = Links()
            document.feed(data.decode('utf-8-sig'))
            parsed[name] = document
    count = 0
    for name, data in files.items():
        if name.endswith('.html'):
            links = parsed[name].links
        elif name.endswith('.md'):
            text = re.sub(r'```.*?```', '', data.decode('utf-8-sig'), flags=re.S)
            links = re.findall(r'\]\(([^)]+)\)', text)
        else:
            continue
        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                raise ValueError(f'本機連結不能使用網站絕對路徑：{name} -> {link}')
            if not url.path:
                target = name
            else:
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
            if target not in files:
                # 只有實際含 index.html 的目錄入口才視為可使用的網站連結。
                if target.rstrip('/') + '/index.html' in files:
                    target = target.rstrip('/') + '/index.html'
                else:
                    raise ValueError(f'本機連結不存在：{name} -> {link}')
            if url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:
                raise ValueError(f'本機錨點不存在：{name} -> {link}')
            count += 1
    return count


def check_links(folder):
    """驗證完整 Pages／離線資料夾，不略過不存在的 ZIP 下載。"""
    folder = Path(folder)
    return _check_documents({path.relative_to(folder).as_posix(): path.read_bytes()
                             for path in folder.rglob('*') if path.is_file()})


def check(root=ROOT, write_report=True):
    root = Path(root).resolve()
    manifest = json.loads((root / 'dist/manifest.json').read_text(encoding='utf-8-sig'))
    if manifest.get('version') != VERSION:
        raise ValueError('發行版本與工具版本不一致')
    packages = manifest.get('packages', [])
    # 完整包內附的 manifest 只描述實際包含的兩個子包，避免自我雜湊循環。
    expected = set(PACKAGES[:2]) if manifest.get('scope') == 'embedded-components' else set(PACKAGES)
    if {p['name'] for p in packages} != expected or len(packages) != len(expected):
        raise ValueError('manifest 的套件清單不完整或重複')
    results = []
    for package in packages:
        path = root / 'dist' / package['name']
        if not path.is_file():
            raise ValueError('發行檔不存在：' + package['name'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != package['sha256']:
            raise ValueError('ZIP SHA-256 雜湊不符：' + path.name)
        if path.stat().st_size != package['bytes']:
            raise ValueError('ZIP 檔案大小不符：' + path.name)
        privacy = scan(path, label='dist/' + path.name)
        if privacy:
            raise ValueError('\n'.join(privacy))
        with ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP CRC 檢查失敗：' + path.name)
            names = archive.namelist()
            if len(names) != package['file_count']:
                raise ValueError('ZIP 檔案數量不符：' + path.name)
            skills = [name for name in names if '/skills/' in name and name.endswith('/SKILL.md')]
            if 'practice-data' not in path.name and (len(skills) != len(SKILLS) or {Path(name).parent.name for name in skills} != set(SKILLS)):
                raise ValueError('技能包必須恰好包含指定9個 SKILL.md')
            checked_links = 0
            if path.name == PACKAGES[1]:
                checked_links = _check_documents({name: archive.read(name) for name in names})
            if path.name == PACKAGES[2]:
                checked_links = _check_documents({name: archive.read(name) for name in names})
                for required in ['ACCEPTANCE.md', 'README.md', 'handbook/index.html']:
                    if 'codex-office-skill-kit/' + required not in names:
                        raise ValueError('完整包缺少必要入口：' + required)
                if not any(name.startswith('codex-office-skill-kit/qa/') for name in names):
                    raise ValueError('完整包缺少公開驗收摘要')
                nested = json.loads(archive.read('codex-office-skill-kit/dist/manifest.json'))
                if {p['name'] for p in nested['packages']} != set(PACKAGES[:2]):
                    raise ValueError('完整包內的 manifest 必須只列實際附帶的兩個子包')
                for item in nested['packages']:
                    content = archive.read('codex-office-skill-kit/dist/' + item['name'])
                    if hashlib.sha256(content).hexdigest() != item['sha256']:
                        raise ValueError('完整包內嵌套件的 SHA-256 不符')
            results.append({'package': path.name, 'files': len(names), 'skills': len(skills),
                            'checked_local_links': checked_links, 'crc_sha256_paths_privacy_valid': True})
    if write_report:
        output = root / 'qa/release-check.json'
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


if __name__ == '__main__':
    check()
