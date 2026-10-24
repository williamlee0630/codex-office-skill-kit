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

CATEGORIES = {"completed": "本週完成", "progress": "進度與成果", "problem": "問題與阻礙", "next_plan": "下週計畫", "support": "需要主管協助"}
STAR = {"situation": "情境 S", "task": "任務 T", "action": "行動 A", "result": "結果 R"}


def run(input_path, output_dir):
    protect_input(input_path, output_dir)
    data = load_json(input_path)
    identifiers = base(data)
    start = iso(data.get("period_start"), "period_start")
    end = iso(data.get("period_end"), "period_end")
    require(start <= end, "週報起始日期不得晚於結束日期")
    records = array(data.get("records", []), "records")
    for record in records:
        evidence(record, identifiers)
        text(record.get("summary"), "summary")
        require(record.get("category") in CATEGORIES, "週報 category 不支援")
        day = iso(record.get("date"), "紀錄 date", optional=True)
        if day and record["category"] != "next_plan":
            require(start <= day <= end, "本週紀錄日期不在週報期間")
        if day and record["category"] == "next_plan":
            require(day > end, "下週計畫日期須晚於週報結束日；未知可填 null")
        star = record.get("star", {})
        require(isinstance(star, dict), "star 須為物件")
        for key in STAR:
            nullable(star.get(key), f"STAR {key}")
    brief = [("報告期間", f"{start} 至 {end}。未提供的成果與數字保留待確認。")]
    detailed = list(brief)
    for category, heading in CATEGORIES.items():
        brief_lines, detail_lines = [], []
        for record in records:
            if record["category"] != category:
                continue
            brief_lines.append(f"{record['summary']}｜日期：{display(record.get('date'))}")
            detail_lines.append(f"{record['summary']}｜日期：{display(record.get('date'))}｜依據：{cite(record)}")
            if category in {"completed", "progress"}:
                star = record.get("star", {})
                for key, label in STAR.items():
                    fallback = "待確認；成果數字未提供" if key == "result" else UNKNOWN
                    detail_lines.append(f"STAR {label}：{star.get(key) or fallback}")
        brief.append((heading, brief_lines or ["未提供，待確認"]))
        detailed.append((heading, detail_lines or ["未提供，待確認"]))
    brief += source_sections(data)
    detailed += source_sections(data)
    output = Path(output_dir)
    for name, sections in [("weekly-brief", brief), ("weekly-detailed", detailed)]:
        write_markdown(output / f"{name}.md", markdown(data["title"], sections))
        write_docx(output / f"{name}.docx", data["title"], sections)
    write_json(output / "evidence.json", data)
    return {"files": ["weekly-brief.md", "weekly-detailed.md", "weekly-brief.docx", "weekly-detailed.docx", "evidence.json"]}


if __name__ == "__main__":
    raise SystemExit(cli())

