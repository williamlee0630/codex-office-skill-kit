# Codex 內部執行與資料契約

這份文件供 Codex 操作；一般使用者不需建 JSON 或下指令。所有資源相對本技能，自帶 `_office.py`，不依賴課程專案根目錄。使用可用 Python，缺套件時由 Codex 在工作區虛擬環境安裝 `scripts/requirements.txt`。Windows 避免主控台編碼問題，設定 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`。

擷取：`python <skill>/scripts/run.py --extract <原始檔> --output <新的擷取目錄>`，讀取 `source-index.json` 全部 blocks。TXT/MD/貼文定位 L1 等為原始行號（空白行仍計數），DOCX P1 等是正文段落編號；表格 T1/R1/C1；頁首頁尾 S1/HEADER/P1；PDF PAGE1/L1 等為頁數與擷取行號。引用必須逐字存在於該位置。跨行內容分多個引用。

產檔：`python <skill>/scripts/run.py --input <Codex內部分析.json> --output <新的成果目錄>`。執行前 Codex 必須通讀原件，不能把腳本視為法律分類器。JSON 全部文字為 UTF-8：

```json
{
  "document_name": "文件名稱",
  "document_type": "合作協議",
  "perspective": "甲方（或立場待確認）",
  "jurisdiction": null,
  "source": {"path": "相對本JSON的原件.docx"},
  "checked_locations": ["P1", "P2"],
  "review_topics": [],
  "findings": [],
  "legal_check": {"status": "unverified", "reason": "尚無法核實現行法律來源"},
  "legal_sources": [],
  "questions": ["請確認適用法域"]
}
```

貼文用 `source: {"text": "逐字原文"}`，與 path 擇一。原件 path 每次由產檔器重新讀取；checked_locations 必須完整包含來源所有非空位置，避免局部閱讀卻斷言缺漏。source hash 保存原件位元內容；貼文 hash 保存 UTF-8 原文。

`review_topics` 必須恰好九項，topic：`parties_purpose`、`term_renewal`、`payment`、`liability`、`confidentiality_privacy`、`ip`、`termination`、`law_disputes`、`special`。每項含 status（present/missing/not_applicable）、analysis（實質逐項分析）、citations（陣列）。present 每項至少一個 `{"location":"P2","quote":"逐字原文"}`。missing／not_applicable citations 為空，analysis 說明缺漏或依文件性質不適用原因。每個 missing 必須有風險及具體新增文字。

`findings` 每項欄位：id（唯一）、topic、missing_clause（布林，缺漏為 true）、citations（現有條款至少一個；缺漏為空）、issue（問題）、impact（商業或法律影響）、level（高／中／低）、reason（等級理由）、action（處理方式）、professional_confirmation（布林）、draft_terms（可協商修訂文字）、revision_reason、questions（文字陣列）、legal_basis_status（commercial_only／unverified／supported）、legal_source_ids（ID陣列）。所有判斷由 Codex 依原文及背景作成。高風險通常涉及重大不可控曝險或核心權利，低風險仍應給出實質理由，不能依特定用詞機械打分。

`legal_sources` 每項含 id、law_name、article、url、checked_at（YYYY-MM-DD）、jurisdiction（與本次法域相同）、authority、path（實際查讀後保存的官方來源文字快照）、quote（逐字摘錄）。有來源支持的風險必須引用存在的 ID，且法域已知、legal_check.status 為 checked，另填 as_of。程式會讀快照比對 quote 並記 hash，但不連線驗證官方身份、現行有效性或語意支持；這些由 Codex 查讀並在報告中說清楚。不能把只有網址當作完成查證。查證失敗用 unverified 與具體原因，不能硬填 supported。

零風險可產檔，但九項 analysis 仍要完整；結論不代表安全認證。錯誤原文、缺少檢查項、未知來源、OCR 限制及已存在成果會停止；改正資料或選新輸出目錄後重新執行，不沿用舊檔冒充新結果。三個主要成果及 audit.json 先在暫存目錄完成，再移至新目的地；不改來源。
