"""工作區靜態檢查；不是官方 validator 或語意驗收的替代品。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
from publication import SKILLS
EXPECTED = set(SKILLS)


def validate():
    errors = []
    paths = sorted((ROOT / '.agents/skills').glob('*/SKILL.md'))
    if {p.parent.name for p in paths} != EXPECTED or {p.name for p in (ROOT / '.agents/skills').iterdir() if p.is_dir()} != EXPECTED:
        errors.append('技能資料夾清單與9項指定名稱不一致。')
    descriptions = set()
    common = (ROOT / 'tools/office_common.py').read_bytes()
    for path in paths:
        skill = path.parent
        text = path.read_text(encoding='utf-8')
        match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
        if not match:
            errors.append(f'{skill.name} 缺少YAML frontmatter。')
            continue
        front = match.group(1)
        name = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)', front, re.M)
        desc = re.search(r'^description:\s*(.+)$', front, re.M)
        if not name or name.group(1) != skill.name:
            errors.append(f'{skill.name} 的name不符。')
        if not desc or desc.group(1) in descriptions:
            errors.append(f'{skill.name} description缺少或重複。')
        else:
            descriptions.add(desc.group(1))
        if '[TODO' in text or 'Add the task-specific' in text:
            errors.append(f'{skill.name} 還有未完成骨架。')
        for required in ['scripts/run.py', 'scripts/_office.py', 'references/workflow.md', 'agents/openai.yaml']:
            if not (skill / required).is_file():
                errors.append(f'{skill.name} 缺少{required}。')
        if (skill / 'scripts/_office.py').is_file() and (skill / 'scripts/_office.py').read_bytes() != common:
            errors.append(f'{skill.name} 共用工具副本不同，請執行sync_runtime.py。')
        # 實際 Markdown 連結，不把敘述中的路徑或 <參數> 當檔案。
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in link and not link.startswith('#'):
                target = (skill / link.split('#')[0]).resolve()
                if not target.exists():
                    errors.append(f'{skill.name} 連結不存在：{link}')
        example = ROOT / 'examples' / skill.name
        if not example.is_dir() or not list(example.glob('*.[jcm]*')):
            errors.append(f'{skill.name} 缺少模擬資料。')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join('錯誤：' + p for p in problems))
        raise SystemExit(1)
    print('9個技能結構、相對連結、共用資源與模擬資料檢查通過。此結果不代表Codex觸發驗收。')
