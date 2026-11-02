# v1.3.0 郵件、文件、創意與研究成果驗證

日期：2026-11-02。這是維護者依章首原始素材整理證據後，執行本機產檔器的驗證；不是全新 Codex 對話、桌面操作或真實 Gmail 帳號端到端成功紀錄。舊驗收與舊 `output/` 均保留。

## 缺口與修正

五項新增行為測試先觀察到失敗：郵件拒絕含17:00等完整ISO期限；郵件跨時區期限未以台北日期初判；文件不呈現版本與核准狀態；創意未選案仍產空白計畫；研究忽略結論與比較表。修正後五項通過（16.536秒，0失敗／錯誤）。另重跑原有foundation八項、information十一項通過；完整套件狀態以整合驗收為準。

完成後差異審查另重現創意未選案時`validation_plan`遺失，已把後續驗證納入必要`ideas.md`，不依賴額外計畫檔。此斷言已加入既有創意行為測試；最後五項重跑通過（14.560秒，0失敗／錯誤）。

| 技能／情境 | 本次來源 | 實際產物 | 內容核對 | 原生Office／完整互動 |
| --- | --- | --- | --- | --- |
| 郵件：三封活動郵件備案 | `examples/email-assistant/quality-source.md`，對照講義收合備案；非Gmail | `quality-output/daily-summary.md`、`drafts.md`、`evidence.json` | 三封均保留寄件人、主旨、時間與來源；回覆／執行分類可重疊；10/26 17:00為確認期限，10/27中午為客戶要求，討論未定；三語氣使用相同事實 | Markdown已重新讀取；真實Gmail讀信與完整Codex互動未測 |
| 文件：客服案件交接SOP | `examples/document-writer/quality-source.md`，等同第5章完整教學背景 | `quality-output/document-formal.docx/.md`、`document-concise.docx/.md`、`evidence.json` | 兩版依同一九項來源事實產生；正式版含目的、範圍、角色、流程、例外、限制；精簡版按交班前、交接時、例外、結案安排；未知工具、上線日、時限、保存年限、簽核層級保留 | 兩DOCX以python-docx重新開啟並核對段落；原生Word及逐頁視覺另列整合驗收，不在此宣稱 |
| 創意：8,000元、兩位人員、十案 | `examples/idea-generator/quality-source.md`，等同第7章情境 | `quality-output/ideas.md`、`comparison.csv`、`evidence.json` | 十種不同做法，逐案含人力分配、成本估算假設、優缺、風險與驗證；CSV有UTF-8 BOM及十筆；未選案且不產selected-plan或XLSX | CSV解析通過；原生Excel及完整Codex互動另列整合驗收 |
| 研究：24人方案A/B | 第8章實際兩份Word附件，`quality-input.json`引用`../quickstart/`來源 | `quality-output/research-report.md`、`sources.csv`、`evidence.json` | 逐字摘錄實際存在DOCX；A24×1200=28800、B20×950=19000且少4名；日期2026-10-01／2025-08-15；幣別、稅額、取消、新年度與擴額保留缺口 | Markdown/CSV已重新讀取；未執行即時網路搜尋；完整Codex互動未測 |

所有 `quality-input.json` 是已整理的維護者證據，僅供重現程式結果，不能用來聲稱 Codex 從原始資料獨立判讀成功。正式來源快照與舊案分開；郵件原本 `input.json` 是另一批歷史本機郵件，文件舊案是「內部知識分享提案」，創意舊案有已選定I1，均不混稱新版章首結果。

SOP九項引文另逐一核對存在於原始教學輸入。共用Word表格支援同步後，正式版已重新產生並確認角色表為原生Word表格（4列）；重建精簡版時遇到`PermissionError`（原生Office唯讀驗收進行中），因此不能把該次整組重建標成功。後續由整合工作者在新資料夾重建，再更新交付成果；以整合驗收的最終檔案核對為準。

## 重現方式（維護者）

對四技能分別執行 `python .agents/skills/<技能>/scripts/run.py --input examples/<技能>/quality-input.json --output <新的輸出資料夾>`，使用有安裝相應requirements的Python。輸出目錄須另建，保留本次已檢查成果。

行為測試：`python -m unittest discover -s tests -p test_quality_semantic.py -v`。基礎與資訊回歸：同方式執行`test_foundation.py`及`test_information.py`。

Gmail只檢查當前工具契約與Skill指引：搜尋ID後實際full讀取可取得內文；query與label_ids不可混用；預設不呼叫寄送、建立草稿或變更狀態。工具介面存在不代表帳號可用，真實讀信仍須使用者授權環境另驗證；不得沿用上述貼文備案的通過紀錄。
