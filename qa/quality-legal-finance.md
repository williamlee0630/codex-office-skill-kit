# v1.3.0 法務與財務成果品質驗收

日期：2026-11-02。以下是本次程式與來源內容核對，不將歷史測試、預填分析或成品存在等同全新 Codex 端到端成功。原歷史逾時、PermissionError 與用量限制紀錄保留。

## 可重現方式

一般學員仍使用講義完整提示詞及下載附件。維護者可在已具 requirements 套件的 Python 執行：

```text
python -m unittest discover -s tests -p test_legal.py -v
python -m unittest discover -s tests -p test_finance.py -v
python -m unittest discover -s tests -p test_quality_legal_finance.py -v
python .agents/skills/legal-reviewer/scripts/run.py --input examples/legal-reviewer/quality-input.json --output 新的法務成果資料夾
python .agents/skills/finance-assistant/scripts/run.py --input examples/finance-assistant/quality-input.json --output 新的財務成果資料夾
```

## 本次內容及實際成果

| 情境 | 來源／方法 | 實際產物與核對 |
|---|---|---|
| 法務甲方審查 | 第 9 章 `examples/quickstart/模擬服務合約_甲方審查.docx`；SHA-256 `20fd21f78881df7ce4f3cc037563b562046252a8acb4c187aa2a670c13954dfb`。與原測試合約位元相同；沿用已整理的審查測資，重新讀取原件核對所有位置與引用。未執行即時法律搜尋。 | `examples/legal-reviewer/quality-output/` 的 DOCX、XLSX、Markdown 與 audit。Word 首節主管風險摘要；五高四中，明細依風險排序，九項皆保留原 ID、位置、商業影響、理由及可協商修訂；法域與法律查證未確認。 |
| 公司帳與銀行對帳 | 第 10 章 `examples/quickstart/模擬公司內部帳務.csv`、`模擬銀行交易明細.csv`，程式直接讀取原始數值並以 Decimal 運算。 | `examples/finance-assistant/quality-output/` 的 Excel、DOCX、finance-result。對帳摘要置首；B 來源均為第 3 列，200−210＝-10；DUP 兩筆 50 保留，六類、一對一、TWD／USD、-25 沖銷、零額、日期不一與跨期保留。 |

## 產檔與錯誤處理

本次兩項新增摘要行為測試先失敗：原程式先列文件／來源，主管需往後找結論。修改後三項品質測試通過，包含以模擬 PermissionError 中斷第二成品移動時，撤回本次已移動的第一成品，避免單檔被誤當完整成功。此為可重現錯誤處理測試，不宣稱重現先前桌面沙箱的同一個 ACL 問題。

法務：四個檔案先在暫存位置完成，重新解析 Word／Excel 並核對風險 ID、順序、筆數與修訂文字；財務：三檔先在暫存位置完成，重新解析 Word／Excel 並核對工作表、筆數、分類、交易識別碼、雙方金額與差額。重新檢查目的地無舊檔後才交付；原件與舊成果不覆寫。公開成品僅記來源檔名與 SHA-256，不含個人工作目錄。

## 分層狀態與限制

| 關卡 | 法務 | 財務 |
|---|---|---|
| 必要成品實際產生、可由格式套件重新讀取 | 通過 | 通過 |
| 來源位置／內容／運算核對 | 本次原件引用、九項風險及修訂核對通過；法律真實性與現行效力未查證 | 六類、B -10、DUP、來源列及分幣計算通過；例外尚待人工確認 |
| 程式回歸 | 修改前九項、修改後九項皆通過；新三項品質測試另通過 | 修改前十四項通過；含兩項新摘要測試的十六項回歸通過；新三項品質測試另通過 |
| 原生 Word／Excel 開啟及畫面 | 本分工未執行，仍待本版整合驗收或人工檢查 | 本分工未執行，仍待本版整合驗收或人工檢查 |
| 全新 Codex／桌面完整互動 | 本分工未執行，不以本次程式測試替代先前逾時／權限失敗 | 本分工未執行，不把先前用量中斷改標完整成功 |

報表編製與預算差異的既有測試仍覆蓋：借貸不平不補造、資產負債核對、現金流量門檻、零分母、負數、Decimal 精度、多幣別、來源列與異常原因待查。正式財務查核、法律意見與人工決策均未由程式完成。
