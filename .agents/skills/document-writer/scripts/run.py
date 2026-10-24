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
    purpose = nullable(data.get("purpose"), "purpose")
    audience = nullable(data.get("audience"), "audience")
    facts = array(data.get("facts", []), "facts")
    fact_ids = set()
    for fact in facts:
        evidence(fact, identifiers)
        fact_id = text(fact.get("id"), "事實 id")
        require(fact_id not in fact_ids, "事實 id 不可重複")
        fact_ids.add(fact_id)
        text(fact.get("text"), "事實 text")
    versions = data.get("versions")
    require(isinstance(versions, dict), "versions 須為物件")
    for version in ("formal", "concise"):
        sections = array(versions.get(version), f"versions.{version}")
        require(bool(sections), "正式版與精簡版都須提供至少一段")
        for section in sections:
            require(isinstance(section, dict), "文件段落須為物件")
            text(section.get("heading"), "段落 heading")
            text(section.get("text"), "段落 text")
            refs = array(section.get("fact_ids"), "fact_ids")
            require(bool(refs) or not facts, "每個事實段落須標記 fact_ids")
            require(all(ref in fact_ids for ref in refs), "fact_ids 引用不存在的原始事實")
    unknowns = array(data.get("pending_questions", []), "pending_questions")
    require(all(isinstance(value, str) for value in unknowns), "待確認事項須為文字")
    output = Path(output_dir)
    files = []
    for version, label in (("formal", "正式版"), ("concise", "精簡版")):
        sections = [("文件目的與讀者", f"目的：{display(purpose)}。讀者：{display(audience)}。")]
        sections += [(item["heading"], item["text"]) for item in versions[version]]
        sections.append(("原始事實與來源", [f"{fact['id']}：{fact['text']}｜{cite(fact)}" for fact in facts] or ["未提供原始事實，待確認"]))
        sections.append(("待確認事項", unknowns or ["未提供額外待確認事項；仍請核對原始事實與用語"]))
        sections += source_sections(data)
        name = f"document-{version}"
        write_markdown(output / f"{name}.md", markdown(data["title"] + " " + label, sections))
        write_docx(output / f"{name}.docx", data["title"] + " " + label, sections)
        files += [f"{name}.md", f"{name}.docx"]
    write_json(output / "evidence.json", data)
    return {"files": files + ["evidence.json"]}


if __name__ == "__main__":
    raise SystemExit(cli())

