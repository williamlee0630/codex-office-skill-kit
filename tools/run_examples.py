"""執行九組已整理測資，產生可檢查的真實成果；不代表語意觸發。"""
from pathlib import Path
import subprocess
import sys
import json
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {'data-analyst': 'sales.csv', 'presentation-maker': 'deck.json', 'receipt-organizer': 'receipts.json'}


def run_examples():
    results = []
    staging = ROOT / '.work' / ('example-runs-' + str(time.time_ns()))
    for skill in sorted((ROOT / '.agents/skills').iterdir()):
        if not (skill / 'SKILL.md').is_file():
            continue
        folder = ROOT / 'examples' / skill.name
        source = folder / INPUTS.get(skill.name, 'input.json')
        command = [sys.executable, '-X', 'utf8', str(skill / 'scripts/run.py'), '--input', str(source), '--output', str(staging / skill.name)]
        if skill.name == 'data-analyst':
            command += ['--group-by', 'category', '--value', 'amount', '--date-column', 'date']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        print(f'{skill.name}: ' + ('成功' if result.returncode == 0 else '失敗'))
        record = {'skill': skill.name, 'input': str(source.relative_to(ROOT)), 'returncode': result.returncode,
                  'output': result.stdout.strip(), 'error': result.stderr.strip()}
        results.append(record)
        if result.returncode == 0:
            shutil.copytree(staging / skill.name, folder / 'output', dirs_exist_ok=True)
        if result.returncode:
            print(result.stderr, file=sys.stderr)
    (ROOT / 'docs/qa').mkdir(parents=True, exist_ok=True)
    (ROOT / 'docs/qa/examples-results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    return all(r['returncode'] == 0 for r in results)


if __name__ == '__main__':
    raise SystemExit(0 if run_examples() else 1)
