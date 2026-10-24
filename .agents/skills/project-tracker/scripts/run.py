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

STATUSES = {"not_started": "未開始", "in_progress": "進行中", "completed": "已完成", "blocked": "受阻"}


def latest_confirmed(records, as_of):
    relevant = [record for record in records if record["date"] <= as_of and record["confirmation"] == "confirmed"]
    if not relevant:
        return None, False
    latest_date = max(record["date"] for record in relevant)
    latest = [record for record in relevant if record["date"] == latest_date]
    distinct = {tuple(record.get(key) for key in ("status", "owner", "due", "text")) for record in latest}
    return latest[-1], len(distinct) > 1


def run(input_path, output_dir):
    protect_input(input_path, output_dir)
    data = load_json(input_path)
    identifiers = base(data)
    as_of = iso(data.get("as_of"), "as_of")
    tasks = array(data.get("tasks", []), "tasks")
    decisions = array(data.get("decisions", []), "decisions")
    task_ids = set()
    for task in tasks:
        require(isinstance(task, dict), "任務須為物件")
        task_id = text(task.get("id"), "任務 id")
        require(task_id not in task_ids, "任務 id 不可重複")
        task_ids.add(task_id)
        text(task.get("title"), "任務 title")
        for update in array(task.get("updates", []), "updates"):
            evidence(update, identifiers)
            iso(update.get("date"), "更新 date")
            require(update.get("confirmation") in {"confirmed", "proposed"}, "confirmation 須為 confirmed/proposed")
            require(update.get("status") in STATUSES, "任務 status 不支援")
            nullable(update.get("owner"), "owner")
            iso(update.get("due"), "due", optional=True)
    for decision in decisions:
        evidence(decision, identifiers)
        text(decision.get("topic"), "決策 topic")
        text(decision.get("text"), "決策 text")
        iso(decision.get("date"), "決策 date")
        require(decision.get("confirmation") in {"confirmed", "proposed"}, "confirmation 須為 confirmed/proposed")
    resolved, risks, rows = [], [], []
    for task in tasks:
        current, conflict = latest_confirmed(task.get("updates", []), as_of)
        state = current.get("status") if current and not conflict else None
        owner = current.get("owner") if current and not conflict else None
        due = current.get("due") if current and not conflict else None
        category = STATUSES.get(state, UNKNOWN)
        if due and state != "completed" and due < as_of:
            category = "逾期"
        proposals = [u for u in task.get("updates", []) if u["date"] <= as_of and u["confirmation"] == "proposed"]
        if conflict:
            risks.append(f"{task['id']} 同日有互相衝突的已確認更新，待人工確認")
        if state == "blocked":
            risks.append(f"{task['id']} 工作受阻")
        if owner is None or due is None:
            risks.append(f"{task['id']} 負責人或期限未完整提供，待確認")
        if category == "逾期":
            risks.append(f"{task['id']} 截至 {as_of} 已逾期，尚無已完成依據")
        if proposals:
            risks.append(f"{task['id']} 有 {len(proposals)} 筆未確認更新，不覆寫已確認進度")
        record = {"id": task["id"], "title": task["title"], "status": state, "classification": category, "owner": owner, "due": due, "conflict": conflict, "evidence": current.get("evidence", []) if current else [], "proposals": proposals}
        resolved.append(record)
        rows.append([task["id"], task["title"], category, display(owner), display(due), cite(current or {})])
    decision_results, changes, pending = [], [], []
    for topic in dict.fromkeys(item["topic"] for item in decisions):
        history = [item for item in decisions if item["topic"] == topic and item["date"] <= as_of]
        current, conflict = latest_confirmed(history, as_of)
        decision_results.append({"topic": topic, "current": current["text"] if current and not conflict else None, "conflict": conflict, "evidence": current.get("evidence", []) if current else []})
        confirmed = sorted([item for item in history if item["confirmation"] == "confirmed"], key=lambda item: item["date"])
        for before, after in zip(confirmed, confirmed[1:]):
            if before["text"] != after["text"]:
                label = "同日衝突待確認" if before["date"] == after["date"] else "已確認變更"
                changes.append(f"{topic}｜{label}：{before['text']} → {after['text']}｜{cite(after)}")
        pending += [f"{topic}｜提議：{item['text']}｜{cite(item)}" for item in history if item["confirmation"] == "proposed"]
    sections = [("追蹤基準", f"截至 {as_of}。僅採基準日以前的已確認更新；缺漏與衝突均待確認。"),
                ("專案進度", [f"{r[0]} {r[1]}｜{r[2]}｜負責人：{r[3]}｜期限：{r[4]}｜{r[5]}" for r in rows] or ["未提供任務，待確認"]),
                ("最新已確認決策", [f"{r['topic']}：{display(r['current'])}" for r in decision_results] or ["未提供，待確認"]),
                ("決策變更", changes or ["未發現有來源的已確認變更"]),
                ("待確認提議", pending or ["未提供"]),
                ("風險摘要", risks or ["依現有資料未發現規則可判斷的風險；其他風險由 Codex 核對來源"])]
    sections += source_sections(data)
    output = Path(output_dir)
    write_markdown(output / "progress.md", markdown(data["title"], sections))
    headers = ["編號", "工作", "狀態", "負責人", "期限", "來源"]
    write_csv(output / "progress.csv", headers, rows)
    write_xlsx(output / "progress.xlsx", headers, rows, sheet_name="專案進度")
    evidence_data = copy.deepcopy(data)
    evidence_data.update(resolved_tasks=resolved, resolved_decisions=decision_results)
    write_json(output / "evidence.json", evidence_data)
    return {"files": ["progress.md", "progress.csv", "progress.xlsx", "evidence.json"]}


if __name__ == "__main__":
    raise SystemExit(cli())

