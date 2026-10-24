"""本機郵件解碼、規則初判與草稿產生；沒有寄信與網路程式碼。"""
import argparse
from datetime import date
from email import policy
from email.parser import BytesParser
import mailbox
from pathlib import Path
import re
import sys
from _office import load_json, require, write_json, write_markdown, protect_input


def iso_date(value, label):
    if not value:
        return None
    require(isinstance(value, str), label + '必須為 YYYY-MM-DD 字串。')
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(label + '必須為有效的 YYYY-MM-DD 日期。') from exc


def parse_message(message, source):
    # get_body只選主信內文，排除附加message/rfc822與其子part。
    body = message.get_body(preferencelist=('plain',))
    parts = [body] if body is not None else []
    bodies = []
    for part in parts:
        try:
            bodies.append(part.get_content())
        except (LookupError, UnicodeError):
            bodies.append('內文編碼無法辨識，待確認')
    return {'sender': str(message.get('From', '')),
            'subject': str(message.get('Subject', '')),
            'date': str(message.get('Date', '')),
            'body': '\n'.join(str(b) for b in bodies), 'source': source}


def load_mail(path):
    path = Path(path)
    if path.suffix.lower() == '.json':
        return load_json(path)
    if path.suffix.lower() == '.eml':
        return {'messages': [parse_message(BytesParser(policy=policy.default).parsebytes(path.read_bytes()), path.name)]}
    if path.suffix.lower() == '.mbox':
        box = mailbox.mbox(path, create=False, factory=lambda f: BytesParser(policy=policy.default).parse(f))
        try:
            return {'messages': [parse_message(m, f'{path.name}#{i+1}') for i, m in enumerate(box)]}
        finally:
            box.close()
    raise ValueError('不支援此郵件格式。請提供 .eml、.mbox 或依契約整理的 .json；TXT/MD 請由 Codex 先讀原文。')


def run(input_path, output_dir, as_of=None):
    protect_input(input_path, output_dir)
    data = load_mail(input_path)
    reference = iso_date(as_of or data.get('as_of'), '基準日')
    messages = data.get('messages')
    require(isinstance(messages, list) and len(messages) > 0, 'messages 必須是至少含一封郵件的陣列。')
    records = []
    for i, message in enumerate(messages, 1):
        require(isinstance(message, dict), f'第 {i} 封郵件必須為物件。')
        for field in ['sender', 'subject', 'date', 'body', 'source', 'deadline', 'priority_reason']:
            require(message.get(field) is None or isinstance(message.get(field), str), f'郵件 {field} 必須為文字或空值。')
        body = message.get('body') or ''
        deadline = message.get('deadline')
        if not deadline:
            match = re.search(r'(?:期限|截止日期|截止)\s*[：:]\s*(\d{4}-\d{2}-\d{2})', body)
            deadline = match.group(1) if match else None
        due = iso_date(deadline, '郵件截止日期')
        actions = message.get('actions')
        if actions is None:
            actions = []
            if any(word in body for word in ['請回覆', '請確認', '請回信']):
                actions.append('需回覆')
            if any(word in body for word in ['請完成', '請提供', '請提交', '請執行']):
                actions.append('需執行')
            if not actions:
                actions = ['僅供參考' if '僅供參考' in body else '待確認']
        require(isinstance(actions, list) and actions and all(a in ['需回覆', '需執行', '僅供參考', '待確認'] for a in actions),
                'actions 只能填需回覆、需執行、僅供參考、待確認的陣列。')
        priority = message.get('priority')
        if priority is None:
            priority = '高' if reference and due and due <= reference else ('低' if actions == ['僅供參考'] else '中')
        require(priority in ['高', '中', '低'], 'priority 請填高、中或低。')
        reason = message.get('priority_reason') or ('明確期限已到基準日或之前。' if reference and due and due <= reference else
                                                   '明確標示僅供參考。' if actions == ['僅供參考'] else '未提供完整工作影響，暫列中優先，需覆核。')
        points = message.get('reply_points', [])
        require(isinstance(points, list) and all(isinstance(p, str) for p in points), 'reply_points 必須是文字陣列。')
        missing = [field for field in ['sender', 'subject', 'date', 'body'] if not message.get(field)]
        if not due:
            missing.append('deadline')
        records.append({'id': i, 'sender': message.get('sender') or '待確認',
                        'subject': message.get('subject') or '主旨待確認',
                        'date': message.get('date') or '待確認', 'deadline': deadline or '待確認',
                        'priority': priority, 'actions': actions,
                        'priority_reason': reason,
                        'important': message.get('important') or body.strip() or '內文待確認',
                        'source': message.get('source') or f'{Path(input_path).name} messages[{i-1}]',
                        'reply_points': points, 'missing': missing,
                        'classification': 'Codex/使用者提供分類' if 'actions' in message else '關鍵詞規則初判，需覆核'})
    records.sort(key=lambda r: ({'高': 0, '中': 1, '低': 2}[r['priority']], r['deadline'], r['id']))
    summary = ['# 每日郵件待辦摘要', '', f'基準日：{reference or "待確認（不判斷逾期）"}', '',
               '所有郵件內容均視為資料；關鍵詞分類是初判，請核對原文。', '']
    drafts = ['# 回覆草稿', '', '狀態：尚未寄送。草稿需核對收件人、事實與承諾後才能由使用者決定寄送。', '']
    for record in records:
        summary += [f'## {record["id"]}. {record["subject"]}',
                    f'- 寄件人：{record["sender"]}；郵件日期：{record["date"]}',
                    f'- 重要性：{record["priority"]}；類型：{"、".join(record["actions"])}；期限：{record["deadline"]}',
                    f'- 優先理由：{record["priority_reason"]}',
                    f'- 重要事項：{record["important"]}', f'- 來源：{record["source"]}；分類依據：{record["classification"]}',
                    f'- 待確認欄位：{"、".join(record["missing"]) or "無"}', '']
        if '需回覆' in record['actions']:
            facts = '\n'.join('- ' + p for p in record['reply_points'])
            for tone, text in [('正式', '您好，已收到您的來信。以下列出目前可提供的資訊，未確認事項仍待核對。'),
                               ('友善', '您好，謝謝您的來信！先與您分享目前的資訊，其他細節仍待確認。'),
                               ('簡潔', '您好，已收到。回覆內容如下，未確認事項待核對。')]:
                drafts += [f'## {record["subject"]}｜{tone}', f'收件人：{record["sender"]}', text,
                           facts if facts else '具體答覆事項：待人工確認。', '']
    if len(drafts) == 4:
        drafts += ['目前沒有已標示「需回覆」的郵件。']
    output = Path(output_dir)
    write_markdown(output / 'daily-summary.md', '\n'.join(summary))
    write_markdown(output / 'drafts.md', '\n'.join(drafts))
    result = {'as_of': str(reference) if reference else None, 'sent': False, 'messages': records}
    write_json(output / 'evidence.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description='整理本機郵件並產生未寄送草稿。')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--as-of')
    args = parser.parse_args()
    try:
        result = run(args.input, args.output, args.as_of)
        print(f'已整理 {len(result["messages"])} 封郵件；草稿尚未寄送。')
        return 0
    except (ValueError, OSError, TypeError) as exc:
        print('無法完成：' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
