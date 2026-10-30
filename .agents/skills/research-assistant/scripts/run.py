"""以本機可核對來源建立研究報告；此腳本本身不存取網路。"""
import argparse
import csv
from datetime import date
import hashlib
from pathlib import Path
import sys
from _office import load_json, read_text, require, safe_cell, write_json, write_markdown, protect_input


def parse_date(value, label):
    if value is None or value == '':
        return None
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(label + '必須為 YYYY-MM-DD 或空值。') from exc


def run(input_path, output_dir):
    protect_input(input_path, output_dir)
    input_path = Path(input_path).resolve()
    data = load_json(input_path)
    require(isinstance(data.get('question'), str) and data['question'].strip(), '請提供 question 研究問題。')
    as_of = parse_date(data.get('as_of'), '資料基準日')
    sources = data.get('sources', [])
    claims = data.get('claims', [])
    require(isinstance(sources, list) and isinstance(claims, list), 'sources 與 claims 必須為陣列。')
    catalog = {}
    for source in sources:
        require(isinstance(source, dict), '來源必須為物件。')
        sid = source.get('id')
        require(isinstance(sid, str) and sid and sid not in catalog, '來源 id 需為非空且不重複的文字。')
        require(isinstance(source.get('path'), str) and source['path'], '來源需要本機 path；只有網址不能當成已讀取的來源。')
        path = (input_path.parent / source['path']).resolve()
        protect_input(path, output_dir)
        content = read_text(path)
        published = parse_date(source.get('published_at'), '來源日期')
        status = '日期待確認'
        if published and as_of:
            status = '日期晚於基準，需確認適用時間' if published > as_of else ('超過一年，需核對是否仍適用' if (as_of-published).days > 365 else '一年內資料，仍需依主題核對時效')
        catalog[sid] = {**source, 'path': str(path), 'content': content,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'freshness': status}
    checked_claims = []
    for claim in claims:
        require(isinstance(claim, dict) and isinstance(claim.get('text'), str), '每個研究主張需要 text。')
        ids = claim.get('source_ids', [])
        require(isinstance(ids, list) and all(isinstance(s, str) for s in ids), '主張 source_ids 必須為文字陣列。')
        require(all(s in catalog for s in ids), '研究主張引用了不存在的來源。')
        kind = claim.get('kind', 'fact')
        require(kind in ['fact', 'interpretation', 'recommendation'], 'kind 只能為 fact、interpretation 或 recommendation。')
        require(kind != 'fact' or bool(ids), '事實主張至少需要一個可核對來源。')
        excerpts = claim.get('excerpts', {})
        require(isinstance(excerpts, dict), 'excerpts 必須是來源 id 對原文摘錄的物件。')
        for sid, quote in excerpts.items():
            require(sid in ids and isinstance(quote, str) and bool(quote.strip()) and quote in catalog[sid]['content'],
                    '來源摘錄必須逐字存在於被引用的本機來源，請核對後再執行。')
        require(kind != 'fact' or all(s in excerpts for s in ids), '每個事實引用都需要 excerpts 原文摘錄；腳本只能檢查摘錄存在，仍須人工核對是否支持主張。')
        checked_claims.append({**claim, 'kind': kind})
    gaps = data.get('gaps', [])
    comparison = data.get('comparison', [])
    require(isinstance(gaps, list) and all(isinstance(g, str) for g in gaps), 'gaps 必須為文字陣列。')
    require(isinstance(comparison, list) and all(isinstance(c, str) for c in comparison), 'comparison 必須為文字陣列。')
    report = ['# 資料研究與調查報告', '', f'研究問題：{data["question"]}',
              f'資料基準日：{as_of or "待確認"}', '',
              '產檔程序：離線來源核對。本程式沒有執行網路搜尋；網址記錄來源位置，Codex 另行查讀的範圍須見查讀紀錄。',
              '若來源標示模擬，結論只適用於教學情境；不能當作真實供應商或市場調查。', '',
              '## 調查方向', data.get('plan') or '比較各方案的適用範圍、限制、資料日期與仍需補證的資訊。', '',
              '## 有來源的發現與判斷']
    labels = {'fact': '來源可核對事實', 'interpretation': '分析推論', 'recommendation': '建議'}
    for claim in checked_claims:
        report += [f'- 【{labels[claim["kind"]]}】{claim["text"]} [{", ".join(claim.get("source_ids", [])) or "無直接來源"}]']
    if not checked_claims:
        report += ['無足夠來源或尚未整理主張，目前不能形成可驗證的研究結論。']
    report += ['', '## 來源比較與衝突'] + (['- ' + c for c in comparison] or ['尚未提供跨來源比較；請核對各來源適用條件，保留無法解決的差異。'])
    report += ['', '## 資訊缺口與不確定性'] + (['- ' + g for g in gaps] or ['尚未提出明確缺口，仍需由研究者檢查資料覆蓋範圍。'])
    if not catalog:
        report += ['- 無足夠來源；請提供可讀取的本機參考文件。']
    report += ['', '## 來源清單']
    for sid, source in catalog.items():
        report += [f'- [{sid}] {source.get("title") or "標題待確認"}；資料日期：{source.get("published_at") or "待確認"}；類型：{source.get("kind") or "待確認"}',
                   f'  - 本機檔案：{source["path"]}', f'  - 時效檢查：{source["freshness"]}',
                   f'  - 來源品質評估：{source.get("quality") or "待研究者說明作者、原始性與可能利益衝突"}',
                   f'  - SHA-256：{source["sha256"]}']
        if source.get('url'):
            report += [f'  - 來源網址（本程式未連線）：{source["url"]}']
    report += ['', '## 驗證界線', '原文摘錄存在與檔案雜湊可由程式確認；來源真實性、語意支持程度與最新公開資訊仍需研究者核對。']
    output = Path(output_dir)
    write_markdown(output / 'research-report.md', '\n'.join(report))
    with (output / 'sources.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['來源ID', '標題', '日期', '檔案', '時效', 'SHA256'])
        for sid, source in catalog.items():
            writer.writerow([safe_cell(v) for v in [sid, source.get('title'), source.get('published_at'), source['path'], source['freshness'], source['sha256']]])
    result = {'mode': 'offline', 'network_used': False, 'question': data['question'],
              'sources': [{k: v for k, v in source.items() if k != 'content'} for source in catalog.values()],
              'claims': checked_claims, 'gaps': gaps}
    write_json(output / 'evidence.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description='根據已提供的本機資料產生可追溯研究報告。')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        result = run(args.input, args.output)
        print(f'已產生離線研究報告，核對 {len(result["sources"])} 個來源；未連線搜尋。')
        return 0
    except (ValueError, OSError, TypeError, ImportError) as exc:
        print('無法完成：' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
