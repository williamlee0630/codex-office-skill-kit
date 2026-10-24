# 開發與維護

## 結構與執行

每個 `.agents/skills/<name>` 都是可獨立攜帶的技能，包含 YAML frontmatter、流程、輸入契約、範例、腳本與共用 `_office.py`。語意由 Codex 對照原始資料判斷；產檔器不具有通用語意理解或 OCR 能力。自然語言要求與實際支援格式以各 SKILL.md 為準。

環境準備見 INSTALL.md。標準維護流程：

```powershell
python tools/sync_runtime.py
python tools/validate_kit.py
python -m unittest discover -s tests -v
python tools/run_examples.py
python handbook/build.py
python tools/build_release.py
```

若只改講義內容，編輯 handbook/lessons.py 或 build.py，再重新建置。網站使用預先產生的 HTML，不透過 fetch 載入本機資料。不要加入 CDN 或外部字型。

## 驗證層級

1. 結構：name/description、路徑、技能數量、無未完成骨架、各自 scripts 與 references。
2. 自動化：正常、不完整、錯誤資料、來源引用、日期、金額、公式注入、實際 OOXML 檔案讀回、獨立複製執行。
3. 產物畫面：實際開啟產生的 Word、Excel、PowerPoint；確認中文字型、文字溢出、列寬及換頁。結構檢查不能代替畫面。
4. Codex 行為：依 tests/manual/trigger-cases.md 在新聊天測明確與自然語言觸發，從原文開始、記錄載入路徑、語意結果與實際檔案。測試腳本執行成功不能代替這一層。

目前環境與已驗收項目以 ACCEPTANCE.md / PROGRESS.md 為準；不能從此維護說明推論已全部通過。

## 官方 skill-creator

本版已實際使用環境提供的 skill-creator/scripts/init_skill.py 初始化十個技能，再完成內容與程式。用 scripts/quick_validate.py 檢查 name、description、frontmatter 與骨架。工具本身需要 PyYAML；本環境使用具有 PyYAML 的系統 Python 執行官方 validator，格式產檔使用 Codex 內建 Python。這兩種執行環境須分別記錄。

## 修改規則

先寫能暴露目標問題的行為測試，再修改運算／產檔。程式只驗證能觀察到的條件，不把「引用存在」寫成「主張已查證」。共用工具變更後執行 sync_runtime.py，避免十份副本漂移。發行前重跑範例，檢查 ZIP 雜湊及解壓後相對連結。

## 第三方套件與資料

ZIP 不內含第三方套件二進位。requirements.txt 限定主要相容範圍；reportlab供自動測試產生PDF測資，並非OCR引擎。環境實測版本記錄在 docs/qa/environment.json。範例皆為原創模擬資料，不包含真實個資或公司文件。源碼與教學的使用條款見 LICENSE。
