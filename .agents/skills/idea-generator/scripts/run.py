"""只處理 Codex 已核對的有來源結構資料；不進行自然語言推論。"""
import argparse
import copy
import csv
from datetime import date
from pathlib import Path
import sys
from _office import load_json, require, write_json, write_markdown, write_docx, write_xlsx, safe_cell, protect_input

UNKNOWN = "待確認"


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}須為非空白文字")
    return value.strip()


def array(value, label):
    require(isinstance(value, list), f"{label}須為陣列")
    return value


def iso(value, label, optional=False):
    if optional and value in (None, ""):
        return None
    require(isinstance(value, str), f"{label}須為 YYYY-MM-DD 日期")
    try:
        parsed = date.fromisoformat(value)
        require(parsed.isoformat() == value, f"{label}須為 YYYY-MM-DD 日期")
        return parsed.isoformat()
    except ValueError:
        raise ValueError(f"{label}須為有效的 YYYY-MM-DD 日期") from None


def nullable(value, label):
    if value in (None, ""):
        return None
    return text(value, label)


def base(data):
    require(isinstance(data, dict), "JSON 根節點須為物件")
    text(data.get("title"), "title")
    sources = array(data.get("sources"), "sources")
    require(bool(sources), "至少提供一個來源；缺來源請先由 Codex 核對原始資料")
    identifiers = set()
    for source in sources:
        require(isinstance(source, dict), "每個來源須為物件")
        identifier = text(source.get("id"), "來源 id")
        require(identifier not in identifiers, "來源 id 不可重複")
        identifiers.add(identifier)
        text(source.get("label"), "來源 label")
        iso(source.get("date"), "來源 date", optional=True)
    return identifiers


def evidence(item, identifiers):
    require(isinstance(item, dict), "資料項目須為物件")
    refs = array(item.get("evidence"), "evidence")
    require(bool(refs), "事實項目須保留至少一筆來源引文")
    for ref in refs:
        require(isinstance(ref, dict), "來源引文須為物件")
        require(ref.get("source_id") in identifiers, "evidence 的 source_id 不存在")
        text(ref.get("quote"), "來源 quote")
    return refs


def cite(item):
    return "；".join(f"[{ref['source_id']}] {ref['quote']}" for ref in item.get("evidence", []))


def display(value):
    return UNKNOWN if value in (None, "") else str(value)


def source_sections(data):
    return [("來源紀錄", [f"[{s['id']}] {s['label']}｜日期：{display(s.get('date'))}" for s in data["sources"]])]


def markdown(title, sections):
    chunks = [f"# {title}", ""]
    for heading, body in sections:
        chunks += [f"## {heading}", ""]
        if isinstance(body, list):
            chunks += [f"- {line}" for line in body] or [f"- {UNKNOWN}"]
        else:
            chunks += [body or UNKNOWN]
        chunks.append("")
    return "\n".join(chunks)


def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([safe_cell(value) for value in headers])
        writer.writerows([[safe_cell(value) for value in row] for row in rows])


def cli():
    parser = argparse.ArgumentParser(description="依有來源的 JSON 產生本機工作成果")
    parser.add_argument("--input", required=True, help="Codex 已核對的 JSON 檔案")
    parser.add_argument("--output", required=True, help="本機輸出資料夾")
    args = parser.parse_args()
    try:
        result = run(args.input, args.output)
        print("已建立：" + "、".join(result["files"]))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2
    return 0

def run(input_path, output_dir):
    protect_input(input_path, output_dir)
    data = load_json(input_path)
    identifiers = base(data)
    text(data.get("goal"), "goal")
    evidence(data, identifiers)
    count = data.get("target_count", 10)
    require(type(count) is int and 1 <= count <= 30, "target_count 須為 1 到 30 的整數，預設 10")
    constraints = array(data.get("constraints", []), "constraints")
    constraint_ids = set()
    for constraint in constraints:
        evidence(constraint, identifiers)
        identifier = text(constraint.get("id"), "限制 id")
        require(identifier not in constraint_ids, "限制 id 不可重複")
        constraint_ids.add(identifier)
        text(constraint.get("text"), "限制 text")
    ideas = array(data.get("ideas"), "ideas")
    require(len(ideas) == count, f"需提供 {count} 個由 Codex 規劃的方案；腳本不自行補造創意")
    idea_ids, titles = set(), set()
    for idea in ideas:
        require(isinstance(idea, dict), "創意須為物件")
        identifier = text(idea.get("id"), "創意 id")
        title = text(idea.get("title"), "創意 title")
        require(identifier not in idea_ids and title not in titles, "創意 id 與標題不可重複")
        idea_ids.add(identifier)
        titles.add(title)
        for field in ("description", "cost", "difficulty", "value", "rationale"):
            text(idea.get(field), field)
        for field in ("resources", "pros", "cons"):
            require(all(isinstance(value, str) for value in array(idea.get(field), field)), f"{field} 須為文字陣列")
        refs = array(idea.get("constraint_ids", []), "constraint_ids")
        require(all(ref in constraint_ids for ref in refs), "constraint_ids 引用不存在的限制")
    selected = data.get("selected_id")
    require(selected is None or selected in idea_ids, "selected_id 不存在")
    plan = array(data.get("plan", []), "plan")
    require(selected is not None or not plan, "需先指定選定方案才可輸出工作計畫")
    if selected is not None:
        require(bool(plan), "選定方案須提供可執行的計畫步驟")
    for step in plan:
        require(isinstance(step, dict), "計畫步驟須為物件")
        text(step.get("step"), "計畫 step")
        text(step.get("deliverable"), "計畫 deliverable")
        nullable(step.get("owner"), "計畫 owner")
        iso(step.get("due"), "計畫 due", optional=True)
    sections = [("問題與目標", data["goal"]),
                ("限制與來源", [f"{c['id']}：{c['text']}｜{cite(c)}" for c in constraints] or ["限制未提供，待確認"]),
                ("評估方式", "以下成本、難度與預期價值均為主觀評估及規劃假設，尚未經實驗或報價驗證。")]
    rows = []
    for idea in ideas:
        body = [idea["description"], f"資源：{'、'.join(idea['resources']) or UNKNOWN}",
                f"成本：{idea['cost']}；難度：{idea['difficulty']}；預期價值：{idea['value']}（主觀評估）",
                f"優點：{'、'.join(idea['pros']) or UNKNOWN}；缺點：{'、'.join(idea['cons']) or UNKNOWN}",
                f"評估理由：{idea['rationale']}；對應限制：{'、'.join(idea.get('constraint_ids', [])) or UNKNOWN}"]
        sections.append((f"{idea['id']} {idea['title']}", body))
        rows.append([idea["id"], idea["title"], idea["cost"], idea["difficulty"], idea["value"], idea["rationale"], "主觀評估，尚待驗證"])
    sections.append(("建議與選擇", display(data.get("recommendation"))))
    sections += source_sections(data)
    plan_sections = [("選定方案", next((idea["title"] for idea in ideas if idea["id"] == selected), "尚未選定，待確認")),
                     ("執行計畫", [f"{index}. {step['step']}｜交付物：{step['deliverable']}｜建議負責人：{display(step.get('owner'))}｜建議期限：{display(step.get('due'))}；均須確認" for index, step in enumerate(plan, 1)] or ["請選定方案後建立步驟，待確認"]),
                     ("驗證方式", display(data.get("validation_plan")))]
    output = Path(output_dir)
    write_markdown(output / "ideas.md", markdown(data["title"], sections))
    write_csv(output / "comparison.csv", ["編號", "方案", "成本", "難度", "預期價值", "理由", "評估性質"], rows)
    write_markdown(output / "selected-plan.md", markdown(data["title"] + " 執行計畫", plan_sections))
    write_json(output / "evidence.json", data)
    return {"files": ["ideas.md", "comparison.csv", "selected-plan.md", "evidence.json"]}


if __name__ == "__main__":
    raise SystemExit(cli())

