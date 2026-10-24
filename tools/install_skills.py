"""預設只預覽；明確 --apply 才複製，永不覆寫既有技能。"""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def install(target, apply=False):
    source = ROOT / '.agents/skills'
    folders = sorted(p.parent for p in source.glob('*/SKILL.md'))
    if len(folders) != 10:
        raise ValueError('來源技能數量不是10，請使用完整發行包。')
    target = Path(target).expanduser().resolve()
    conflicts = [target / p.name for p in folders if (target / p.name).exists()]
    if conflicts:
        raise ValueError('發現同名技能，整次安裝已停止且不覆寫：' + '、'.join(str(p) for p in conflicts))
    print(('將安裝至：' if apply else '預覽安裝位置：') + str(target))
    for folder in folders:
        print('  ' + folder.name)
    if not apply:
        print('尚未複製任何檔案。自行確認後加入 --apply 才會安裝。')
        return []
    target.mkdir(parents=True, exist_ok=True)
    copied = []
    for folder in folders:
        destination = target / folder.name
        shutil.copytree(folder, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.test-*'))
        copied.append(str(destination))
    print(f'已安裝 {len(copied)} 個技能；請在 Codex 核對實際載入路徑。')
    return copied


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='安裝完整技能資料夾，預設預覽且拒絕覆寫。')
    parser.add_argument('--target', required=True, help='目標 .agents/skills 資料夾，必須明確指定。')
    parser.add_argument('--apply', action='store_true', help='實際安裝（仍不覆寫）。')
    args = parser.parse_args()
    try:
        install(args.target, args.apply)
    except (OSError, ValueError) as exc:
        print('安裝停止：' + str(exc), file=sys.stderr)
        raise SystemExit(2)
