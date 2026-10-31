"""重建原創教學模擬合約與固定分析快照；不是自動法律判斷器。"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / '.agents/skills/legal-reviewer'
sys.path.insert(0, str(SKILL / 'scripts'))
from run import TOPICS, extract_source
from docx import Document
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

RISKY = [
    '教學模擬資料｜星芽數位服務合作合約（原創虛構案例，非法律範本）',
    '第一條 當事人與目的：甲方為青禾企劃股份有限公司，乙方為星芽數位有限公司，均為虛構公司。乙方為甲方建置內部客戶管理系統，交付項目由雙方簽署的附件一列明；本次未附附件一。',
    '第二條 期限：合約期間為一年，期滿自動續約三年。甲方應於期滿前一百八十日以書面拒絕續約，逾期視為同意；續約價格由乙方單方決定。',
    '第三條 付款：總價新臺幣三十萬元，甲方於簽署後七日內支付全額。系統是否驗收、交付或上線，不影響付款義務；已付款項均不退還。',
    '第四條 違約與賠償：甲方遲延付款每日按總價百分之三支付違約金，沒有累計上限。甲方因本案造成乙方任何損失，包括間接損失及預期利益，均負無限賠償責任；乙方對甲方之賠償以新臺幣一千元為上限。',
    '第五條 保密：雙方對標示機密之技術及價格資料負保密義務，僅供履約使用；依法令要求揭露時應於可行範圍事先通知。保密義務於合約終止後三年內有效。',
    '第六條 個人資料：甲方得提供員工與客戶聯絡資料供系統測試。乙方得將該資料提供任何合作廠商作行銷使用，無須另行告知甲方或資料當事人，且可永久保存。',
    '第七條 智慧財產：乙方保有既有工具之權利；雙方應另行議定專為甲方開發成果之歸屬及使用授權，未議定前甲方僅得於乙方持續收取服務費期間使用。',
    '第八條 終止：乙方得隨時不附理由立即終止並保留全部已收款。甲方不得提前終止，亦不得要求資料匯出、刪除或交接。',
    '第九條 其他：乙方得以網站公告修改服務內容及本合約，公告當日生效；甲方繼續使用視為接受。',
    '第十條 簽署：雙方簽署日期、簽署人職權與附件一內容均待確認。本文件未約定適用法律及爭議解決方式。'
]
NORMAL = [
    '教學模擬資料｜青禾系統維護服務合約（原創虛構案例，非法律範本）',
    '第一條 當事人與目的：甲方青禾企劃股份有限公司委託乙方星芽數位有限公司維護內部系統，均為虛構公司。範圍為每月例行更新與每月十小時故障排除；新增需求另簽書面報價。',
    '第二條 期限與續約：期間自二〇二六年十一月一日至二〇二七年十月三十一日。期滿即終止，續約應由雙方另以書面同意，費用亦另行約定。',
    '第三條 付款與驗收：每月費用新臺幣二萬元，乙方提交維護紀錄後，甲方於十個工作日內依約定範圍驗收並提出具體缺失；乙方於十個工作日內修正。甲方於驗收合格並收受發票後三十日內付款，爭議部分待確認，無爭議部分仍依期支付。',
    '第四條 違約與責任：任一方重大違約，經他方書面通知後十五日仍未改善，應賠償可證明且具因果關係之直接損失。一般違約之雙方累計責任以最近十二個月已付及應付服務費為限；故意、重大過失及依法不得限制者不受該上限拘束。',
    '第五條 保密與個資：雙方僅得為履約使用機密資料，限制必要人員存取並採合理安全措施；公開、原已合法持有及依法須揭露者除外。個資僅依甲方書面指示處理，分包應先書面同意，事故應立即通知並協助處理。終止後三十日返還或刪除，法定保存例外應隔離存取。保密義務於終止後三年有效。',
    '第六條 智慧財產：各方保有既有權利；乙方為本案製作並收款的維護文件授權甲方永久於內部使用，乙方既有工具授權以履行本案必要範圍為限。第三方套件授權及費用應事前書面揭露，異動需甲方同意。',
    '第七條 終止與交接：任一方得提前三十日書面通知終止，費用按已完成且驗收工作比例結算，未履行預收款應返還。重大違約經十五日催告未改善可終止；乙方應提供甲方資料可讀匯出檔與必要交接。',
    '第八條 法律與爭議：本契約適用中華民國（台灣）法律。爭議應先協商三十日，未解決時由臺灣臺北地方法院為第一審管轄法院，依法有專屬管轄者從其規定。',
    '第九條 其他：契約修改與新增費用應由雙方授權代表書面同意。不可抗力時應及時通知、減輕損害，持續三十日仍無法履行者任一方得終止，依已履行比例結算。簽署人權限與實際營業資料請於簽署前確認。'
]


def write_contract(folder, name, lines):
    (folder / (name + '.txt')).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    doc = Document()
    from docx.oxml.ns import qn
    doc.styles['Normal'].font.name = 'Microsoft JhengHei'
    doc.styles['Normal']._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
    for line in lines:
        doc.add_paragraph(line)
    doc.save(folder / (name + '.docx'))
    font_path = Path(os.environ.get('LEGAL_DEMO_FONT', 'C:/Windows/Fonts/msjh.ttc'))
    if not font_path.is_file():
        raise ValueError('重建 PDF 請設定 LEGAL_DEMO_FONT 為可嵌入的繁體中文字型；已封裝的 PDF 不需安裝字型。')
    pdfmetrics.registerFont(TTFont('TrainingCJK', str(font_path), subfontIndex=0))
    style = ParagraphStyle('Contract', fontName='TrainingCJK', fontSize=11, leading=18, wordWrap='CJK')
    SimpleDocTemplate(str(folder / (name + '.pdf')), pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45).build([item for line in lines for item in [Paragraph(line, style), Spacer(1, 10)]])


def cite(index, fragment):
    for i, b in enumerate(index['blocks']):
        if fragment in b['text']:
            result = [{'location': b['location'], 'quote': b['text']}]
            if index['kind'] == 'pdf':
                for following in index['blocks'][i + 1:]:
                    if following['text'].startswith('第'):
                        break
                    result.append({'location': following['location'], 'quote': following['text']})
            return result
    # PDF wraps paragraphs; preserve every extracted line, including wrapped quotations.
    for b in index['blocks']:
        if fragment[:8] in b['text']:
            return [{'location': b['location'], 'quote': b['text']}]
    raise ValueError('找不到示範原文：' + fragment)


def analysis(folder, filename, normal=False):
    index = extract_source({'path': filename}, folder)
    lines = NORMAL if normal else RISKY
    starts = ['第一條', '第二條', '第三條', '第四條', '第五條', '第六條' if normal else '第七條', '第七條' if normal else '第八條', '第八條' if normal else '第十條', '第九條']
    normal_notes = ['當事人、維護目的與十小時範圍明確；新增需求另簽報價，須另核對虛構案例以外的真實主體與權限。', '一年固定期間且無自動續約，續約及價格須雙方書面同意，控制後續預算承諾。', '付款與驗收、發票相連，並規範具體異議與修正時間；爭議和無爭議款分開，執行上仍需保存驗收紀錄。', '違約補正期、直接損失因果關係與雙方對稱責任上限清楚，故意重大過失及強制規定保留例外；上限是否足敷業務曝險須依實際資料量評估。', '保密例外、必要存取、目的限制、分包同意、事件通知及刪除返還均有約定；個資法義務的現行條文與實際委託處理情境仍需另查。', '既有權利保留與已付維護文件永久內用授權區分，第三方授權事前揭露；如實際需要修改原始碼，應另約權利。', '雙方均可預告終止、依比例結算、返還未履行預付款並資料匯出交接，退出安排具體且相對對稱。', '明確選台灣法律及臺北地院，保留專屬管轄例外；這只是條款記錄，未完成現行法律有效性查證，跨境或特殊案件需法務確認。', '修改需雙方授權書面同意，不可抗力有通知、減損及終止結算，未授權乙方單方變更；仍應實查簽署權限。']
    risk_notes = ['雙方名稱與系統建置目的存在，但交付依賴未提供的附件一，無法驗證功能、時程與驗收標準。', '一年合約透過一百八十日前拒絕要求自動續三年，且續價乙方單方決定，甲方存在長期不可控承諾。', '全額預付與交付驗收脫鉤，且一律不退，付款後甲方缺少交付槓桿與退出回收保障。', '每日總價百分之三違約金無上限，甲方含間接與預期利益無限責任，但乙方上限僅一千元，責任配置嚴重不對稱。', '第五條有相互保密與例外、三年期間；但第六條將員工客戶資料擴張行銷、任意轉交且永久留存，與履約最小範圍衝突。實際合法依據須確定法域後查證。', '既有工具保留合理，但專案成果授權與歸屬留待未來；即使支付開發價款，也可能受持續付費限制。', '乙方可即時無理由終止保留款項；甲方不能終止、匯出或交接，營運中斷及鎖定風險高。', '全文未實質選定法域、法院或仲裁；不能假定新臺幣計價就必然適用台灣法律。需查履約地與當事人設立地。', '網站公告當日單方修改，甲方繼續使用視同接受，無審查與無成本退出機會，可能使原交付承諾不穩定。']
    topics = []
    for i, key in enumerate(TOPICS):
        topics.append({'topic': key, 'status': 'missing' if not normal and key == 'law_disputes' else 'present', 'analysis': (normal_notes if normal else risk_notes)[i], 'citations': [] if not normal and key == 'law_disputes' else cite(index, starts[i])})
    if not normal:
        topics[4]['citations'] += cite(index, '第六條')
    result = {'document_name': lines[0], 'document_type': '系統維護服務契約' if normal else '系統建置服務合作合約', 'perspective': '甲方', 'jurisdiction': '中華民國（台灣）' if normal else None, 'source': {'path': filename}, 'checked_locations': [b['location'] for b in index['blocks']], 'review_topics': topics, 'findings': [], 'legal_check': {'status': 'unverified', 'reason': '此離線教學案例沒有保存官方法律來源；未完成最新法規查證，不據此認定條款違法。'}, 'legal_sources': [], 'questions': ['確認公司登記、簽署權限、實際履約地與完整附件。']}
    result['simulation'] = True
    if normal:
        return result
    entries = [
        ('parties_purpose', '中', '交付附件缺失', '可能對完成範圍、時程與驗收認定發生爭執。', '核心功能範圍未能核對，但可在簽署前補正。', '附件一應列明功能清單、交付里程碑、驗收測試及完成期限，經雙方簽署後始生效；未確認項目以書面變更程序議定，不視為甲方已接受。', '請補附件一及驗收測試。'),
        ('term_renewal', '高', '長期自動續約與單方續價', '遺漏提前拒絕時點即承擔三年未知價格服務費。', '承諾期間超出原約且價格不可控。', '本合約期滿即終止；續約應於期滿前由雙方另以書面確認期間、服務內容及價格，未達成書面合意者不自動續約。', '確認是否確實需要自動續約。'),
        ('payment', '高', '預付全額且與驗收無關、一律不退', '交付失敗或未履行時資金回收與談判成本增加。', '甲方主要款項在取得成果前全數曝險。', '總價新臺幣三十萬元分期支付，各期比例與里程碑為【待雙方確認】；甲方於對應里程碑驗收合格並收受發票後三十日內付款。乙方重大違約經書面催告十五日未改善者，甲方得終止並請求返還未履行部分價款。', '確認分期比例與各里程碑。'),
        ('liability', '高', '無上限日計違約金及責任極不對稱', '甲方小額遲付可能累積超過契約價款，乙方實質責任難以涵蓋系統損害。', '無限曝險與一千元上限不對稱，具重大資金影響；不直接判違法。', '遲延付款之違約金計算基礎、日率與累計上限由雙方於簽署前書面約定【待確認】，以逾期未付且無爭議款項為計算基礎。雙方對可證明且具因果關係之直接損失負責，累計責任上限為【待協商金額】；故意、重大過失及依法不得限制者不受上限拘束。', '責任上限是否涵蓋可能資料外洩損害？'),
        ('confidentiality_privacy', '高', '個資擴張行銷、任意轉交與永久保存', '資料當事人權益、資安與合規義務不明，可能造成客訴、事件處理與法遵成本。', '用途及接收人範圍皆未受控制，涉及大量員工客戶資料；法律依據未查證。', '乙方僅得依甲方書面指示及合法履約目的處理個人資料，不得自行行銷或提供第三人；分包應經甲方事前書面同意並受同等義務拘束。乙方應採適當安全措施，事故立即通知並協助處理，終止後三十日返還或刪除，依法須保存者另列明依據及期限。', '確認個資類別、當事人告知及合法處理依據。'),
        ('ip', '中', '成果使用權留待後議且繫於持續繳費', '甲方付費後仍可能無法永久使用專案成果或更換服務商。', '核心成果權利未確定，能於簽署前具體協商。', '乙方保有既有工具權利；就專為本案開發且甲方已付清對應款項之成果，授權甲方永久、不可任意撤回於內部使用及委託第三人維護。必要原始碼、介面文件、第三方授權與移轉範圍應於附件一逐項列明【待確認】。', '是否需要所有權移轉、原始碼及第三方維護權？'),
        ('termination', '高', '單方立即終止且封鎖資料退出', '甲方可能突然失去系統及客戶資料，另付遷移成本，預付款仍無法返還。', '營運持續與資料取回缺乏保障。', '任一方得提前三十日書面通知終止；重大違約經書面催告十五日未改善者，他方得終止。乙方應於終止後十五日提供可讀取資料匯出及必要交接，已履行且驗收部分依比例結算，未履行預收款應返還；資料返還或刪除依個資條款辦理。', '確認資料格式、交接工時與備援安排。'),
        ('law_disputes', '中', '缺少準據法及爭議解決安排', '爭議時可能先爭執法院、法律及程序，增加時間與費用。', '缺少跨境背景，尚不能確定適當法域或違法。', '本契約適用【待雙方確認法域】法律；爭議應先由雙方協商三十日，未能解決時提交【待確認法院或仲裁機構及地點】處理，依法不得排除之強制規定從其規定。', '確認設立地、履約地、資產所在地與管轄選擇。'),
        ('special', '中', '公告立即生效之單方修改', '原定價值及服務範圍可能在無明確合意下變動，甲方難以掌握費用與功能。', '權利受單方變更影響，但可藉書面合意及退出條款控制。', '涉及價格、服務範圍或雙方權利義務之修改，應經雙方授權代表書面同意後生效；一般技術調整應提前三十日通知，且不得實質減損已約定功能或安全性，甲方對重大不利調整得終止並按比例退還未履行價款。', '網站公告哪些類型需視為重要變更？')]
    for i, (topic, level, issue, impact, reason, draft, question) in enumerate(entries, 1):
        result['findings'].append({'id': f'R{i}', 'topic': topic, 'missing_clause': topic == 'law_disputes', 'citations': [] if topic == 'law_disputes' else cite(index, starts[list(TOPICS).index(topic)] if topic != 'confidentiality_privacy' else '第六條'), 'issue': issue, 'impact': impact, 'level': level, 'reason': reason, 'action': '簽署前協商具體修訂，確認未決條件並取得書面同意。', 'professional_confirmation': True, 'draft_terms': draft, 'revision_reason': '回應原條款的具體曝險，補足可執行的權利義務、程序與範圍。', 'questions': [question], 'legal_basis_status': 'unverified' if topic in {'liability', 'confidentiality_privacy', 'law_disputes'} else 'commercial_only', 'legal_source_ids': []})
    return result


def main():
    folder = Path(__file__).resolve().parent
    demo = SKILL / 'references/demo'
    demo.mkdir(parents=True, exist_ok=True)
    for name, lines in [('風險服務合約', RISKY), ('正常服務合約', NORMAL)]:
        write_contract(folder, name, lines)
        for ext in ['txt', 'docx', 'pdf']:
            shutil.copyfile(folder / (name + '.' + ext), demo / (name + '.' + ext))
    for filename, raw, normal in [('input.json', '風險服務合約.docx', False), ('normal-input.json', '正常服務合約.docx', True), ('pdf-input.json', '風險服務合約.pdf', False)]:
        data = analysis(demo, raw, normal)
        (demo / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (folder / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    expected = '# 教學模擬資料｜預期審查結果\n\n原創虛構合約，非法律範本或正式法律意見。由甲方立場審查，評級屬教學比較，不等同違法判定。\n\n風險服務合約預期九個檢查項均完成，九項風險，其中高風險五項、中風險四項；每項具原文位置（缺漏為全文範圍）、影響、等級理由與具體修訂。\n\n|ID|項目|等級|原件位置|\n|---|---|---|---|\n'
    data = analysis(demo, '風險服務合約.docx')
    for f in data['findings']:
        expected += f'|{f["id"]}|{f["issue"]}|{f["level"]}|{f["citations"][0]["location"] if f["citations"] else "全文缺漏；P1–P11"}|\n'
    expected += '\n正常服務合約：九項均有相應條款，本範圍無高風險、沒有必須修訂項；仍記錄簽署權限、真實營業資料、實際曝險、附件及現行法規待核對。不因出現付款、賠償、保密用語而機械標高風險。\n\n風險契約法域未定，不推定台灣；正常契約有台灣法律選擇條款，但兩者皆未附官方法律來源，因此報告應明示未完成最新法規查證、不引用虛構法條。文字型 PDF 應有可讀文字並可回查 PAGE 頁／行；掃描 PDF 無 OCR 時不得假裝完整讀取。\n\n產檔應包括 合約審查報告.docx、合約風險清單.xlsx、條款修訂建議.md 及 audit.json。獨立安裝可直接使用 references/demo 中原件與 JSON。JSON 是預填語意快照，僅供程式回歸測試，不等同現場 Codex 語意驗收。\n'
    (folder / '預期審查結果.md').write_text(expected, encoding='utf-8')
    shutil.copyfile(folder / '預期審查結果.md', demo / '預期審查結果.md')


if __name__ == '__main__':
    main()
