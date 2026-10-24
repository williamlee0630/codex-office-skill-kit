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

KINDS = {"summary": "會議重點", "decision": "決議", "action": "待辦", "question": "未解決問題"}
STATES = {"proposed": "提議", "discussion": "討論中", "confirmed": "已確認", "pending": "待確認"}


def run(input_path, output_dir):
    protect_input(input_path, output_dir)
    data = load_json(input_path)
    identifiers = base(data)
    iso(data.get("meeting_date"), "meeting_date", optional=True)
    items = array(data.get("items", []), "items")
    for item in items:
        evidence(item, identifiers)
        text(item.get("text"), "項目 text")
        require(item.get("kind") in KINDS, "kind 須為 summary/decision/action/question")
        require(item.get("status") in STATES, "status 須為 proposed/discussion/confirmed/pending")
        nullable(item.get("owner"), "owner")
        iso(item.get("due"), "due", optional=True)
    sections = [("會議資訊", f"會議日期：{display(data.get('meeting_date'))}。紀錄依來源整理；未定案內容保持原狀。")]
    for heading, predicate in [
        ("會議重點", lambda x: x["kind"] == "summary"),
        ("已確認決議", lambda x: x["kind"] == "decision" and x["status"] == "confirmed"),
        ("提議與討論中事項", lambda x: x["kind"] == "decision" and x["status"] != "confirmed"),
        ("待辦與負責人", lambda x: x["kind"] == "action"),
        ("未解決問題", lambda x: x["kind"] == "question"),
    ]:
        lines = []
        for item in filter(predicate, items):
            line = f"【{STATES[item['status']]}】{item['text']}"
            if item["kind"] == "action":
                line += f"｜負責人：{display(item.get('owner'))}｜期限：{display(item.get('due'))}"
            lines.append(line + f"｜依據：{cite(item)}")
        sections.append((heading, lines or ["未提供，待確認"]))
    sections += source_sections(data)
    output = Path(output_dir)
    write_markdown(output / "minutes.md", markdown(data["title"], sections))
    write_docx(output / "minutes.docx", data["title"], sections)
    write_json(output / "evidence.json", data)
    return {"files": ["minutes.md", "minutes.docx", "evidence.json"]}


if __name__ == "__main__":
    raise SystemExit(cli())

