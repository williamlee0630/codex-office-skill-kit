"""同步每個可獨立安裝技能的共用資源。"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def sync():
    paths = sorted((ROOT / '.agents/skills').glob('*/SKILL.md'))
    for skill in paths:
        target = skill.parent / 'scripts/_office.py'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / 'tools/office_common.py', target)
    return len(paths)


if __name__ == '__main__':
    print(f'已同步 {sync()} 個技能的共用資源。')
