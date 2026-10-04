---
title: "A06 部落格多語發布：為靜態預覽加入安全檢查"
type: article
source: synthetic-human-edited-translation
created: 2026-10-04
status: needs-review
tags:
  - multilingual
  - static-site
---

# 為靜態預覽加入安全檢查

這是一篇為示範而撰寫、內容可公開的技術短文。靜態網站的預覽流程不該因為內容尚未審閱，就把頁面混入發布目錄。最低限度的防護是先驗證中繼資料，再產生隔離的本機預覽。

## 一個小範例

以下命令只會啟動本機檔案伺服器，不會發布內容：

```bash
python3 -m http.server 8000 --directory site
```

預覽器必須保留程式碼中的 `Cache-Control`，也應保留專名 GitHub Pages。讀者可以造訪[範例文件](https://example.com/docs?a=1&b=2)，但產生 HTML 時必須跳脫連結屬性。

## 審閱清單

1. 逐項核對引文、程式碼區塊和專名。
2. 確認譯文表達自然，而不是機械地替換字形。
3. 只有來源雜湊相符且狀態為 `reviewed` 的版本，才具備發布資格。

> 本示範只產生隔離預覽；它不會修改正式環境路由，也不會自動發布。
