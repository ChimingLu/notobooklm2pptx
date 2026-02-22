# Memory Bank 索引

## 📚 文件結構

Memory Bank 包含專案的所有重要資訊，分為以下幾個核心文件：

### 核心文件

#### 1. activeContext.md
**當前專案狀態**
- 專案焦點和目標
- 最新變更記錄
- 技術決策
- 風險管理
- 下一步計畫

#### 2. progress.md
**進度追蹤**
- 已完成功能
- 進行中項目
- 待辦事項
- 已知問題
- 版本歷史

#### 3. techContext.md
**技術背景**
- 技術架構
- 核心技術棧
- 設計模式
- 最佳實踐

#### 4. references.md
**技術參考資料**
- 技術文件連結
- 研究資料
- API 文件
- 開發工具
- 效能基準
- 授權資訊

#### 5. web-references.md ⭐ 新增
**網頁參考資料庫**
- 45+ 個參考資源
- 圖片修復技術研究
- OCR 技術資源
- PDF/PPTX 處理
- Gemini API 文件
- 學術論文
- 社群資源
- 替代方案研究
- 學習資源

## 🗂️ 使用指南

### 查找資訊

**想了解當前狀態？**
→ 閱讀 `activeContext.md`

**想查看進度？**
→ 閱讀 `progress.md`

**想了解技術細節？**
→ 閱讀 `techContext.md`

**想找技術文件？**
→ 閱讀 `references.md`

**想找網頁資源？**
→ 閱讀 `web-references.md`

### 更新規則

1. **每次重大變更後更新 `activeContext.md`**
   - 記錄變更內容
   - 更新決策記錄
   - 調整下一步計畫

2. **功能完成時更新 `progress.md`**
   - 移動項目到「已完成」
   - 更新版本歷史
   - 記錄已知問題

3. **技術架構變更時更新 `techContext.md`**
   - 更新架構圖
   - 記錄新技術
   - 更新最佳實踐

4. **發現新資源時更新 `references.md` 或 `web-references.md`**
   - 添加連結
   - 記錄重點內容
   - 分類整理

## 📊 文件關係圖

```
Memory Bank
├── activeContext.md    ← 當前狀態（最常更新）
├── progress.md         ← 進度追蹤（功能完成時更新）
├── techContext.md      ← 技術背景（架構變更時更新）
├── references.md       ← 技術參考（發現新資源時更新）
└── web-references.md   ← 網頁資源（研究時更新）
```

## 🔄 更新頻率

| 文件 | 更新頻率 | 觸發條件 |
|------|---------|----------|
| activeContext.md | 高 | 每次重大變更 |
| progress.md | 中 | 功能完成、問題解決 |
| techContext.md | 低 | 架構變更、技術升級 |
| references.md | 低 | 新技術文件 |
| web-references.md | 低 | 研究新工具 |

## 📝 維護檢查清單

### 每日檢查
- [ ] activeContext.md 是否反映當前狀態？
- [ ] 是否有新的決策需要記錄？

### 每週檢查
- [ ] progress.md 是否更新？
- [ ] 已知問題是否有變化？

### 每月檢查
- [ ] techContext.md 是否需要更新？
- [ ] references.md 是否有過時連結？
- [ ] web-references.md 是否需要補充？

## 🎯 最佳實踐

### 撰寫原則

1. **清晰簡潔**
   - 使用簡單的語言
   - 避免過度技術化
   - 重點突出

2. **結構化**
   - 使用標題和列表
   - 保持一致的格式
   - 適當使用表格

3. **可追溯**
   - 記錄日期
   - 記錄原因
   - 記錄影響

4. **實用性**
   - 包含實際範例
   - 提供操作步驟
   - 記錄常見問題

### 連結管理

1. **內部連結**
   - 使用相對路徑
   - 保持連結有效
   - 定期檢查

2. **外部連結**
   - 記錄完整 URL
   - 記錄存取日期
   - 備份重要內容

## 📖 閱讀順序建議

### 新成員入門
1. README.md（專案根目錄）
2. activeContext.md
3. progress.md
4. techContext.md

### 開發者
1. techContext.md
2. references.md
3. activeContext.md

### 研究者
1. web-references.md
2. references.md
3. techContext.md

## 🔍 快速查找

### 常見問題

**Q: 專案目前在做什麼？**
A: 查看 `activeContext.md` 的「專案焦點」

**Q: 有哪些功能已完成？**
A: 查看 `progress.md` 的「已完成功能」

**Q: 使用了哪些技術？**
A: 查看 `techContext.md` 的「核心技術棧」

**Q: 在哪裡找 Lama Cleaner 的文件？**
A: 查看 `web-references.md` 的「Lama Cleaner 主要資源」

**Q: API 配額限制是多少？**
A: 查看 `references.md` 的「Gemini API」

## 📌 重要提醒

1. **保持更新**
   - Memory Bank 是活文件
   - 需要持續維護
   - 過時資訊要及時更新

2. **版本控制**
   - 重大變更前備份
   - 使用 Git 追蹤變更
   - 記錄變更原因

3. **團隊協作**
   - 統一格式
   - 避免衝突
   - 定期同步

---

*Memory Bank 索引 v1.1*
*最後更新: 2026-02-22*
