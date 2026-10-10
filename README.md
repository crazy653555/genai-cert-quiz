# 資策會生成式AI能力認證 複習專案

考試資訊：https://www.iiiedu.org.tw/certifications/exam/6

🔗 **線上複習測驗網站**：https://crazy653555.github.io/genai-cert-quiz/

## 資料夾結構

- `考試題目/` — 擷取的考古題，依批次命名為 `題庫01.md`、`題庫02.md`...，是題庫的唯一真相來源
- `重點整理/` — 依主題分類的知識點筆記（模型架構、Prompt工程、模型訓練流程、各類生成工具、AI倫理法規等）
- `複習測驗網站/` — 由 `考試題目/` 自動建置產出的互動測驗網站（`index.html` + `quiz.db`），可離線使用，也已部署在 GitHub Pages 上線
- `_raw/` — 資料擷取與建置用的腳本（`build_db.py`、`build_html.py`）與暫存素材

## 使用方式

1. 貼上題目或重點內容給我，我會驗證後整理存入對應資料夾（`考試題目/` 或 `重點整理/`）
2. 題庫更新後，依序重跑 `python _raw/build_db.py` 與 `python _raw/build_html.py`，`複習測驗網站/` 會自動更新
3. 把更新 commit、push 到 GitHub，GitHub Actions 會自動重新部署線上測驗網站

詳細的建置流程與格式規則見 [`CLAUDE.md`](CLAUDE.md)。
