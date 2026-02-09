# Project Brief: NotebookLM PDF 轉 PPTX (Web → Local Free)

## 專案目標

將 Google NotebookLM 生成的 PDF 講義轉換為可編輯的 PowerPoint 簡報，保留原始排版和文字。

本專案已轉型為**完全免費的本地應用程式**，不再依賴 Google API，無需 API Key，保護使用者隱私並解除使用配額限制。

## 核心功能

*   **PDF 解析**：使用 `pypdfium2` 高解析度渲染 PDF 頁面。
*   **背景清理**：整合 `Lama Cleaner`深度學習模型，自動移除圖片中的文字水印。
*   **OCR 文字辨識**：使用 `EasyOCR` 進行多語言文字與排版辨識。
*   **PPTX 生成**：生成圖層分明的 PowerPoint 檔案，文字可編輯，背景乾淨。
*   **雙介面**：提供 `CLI` (命令列) 與 `GUI` (視窗介面) 兩種操作模式。

## 技術選型

*   **語言**：Python 3.10+
*   **CLI 框架**：`Rich`, `Questionary`
*   **GUI 框架**：`Flet` (Flutter based)
*   **PDF 處理**：`pypdfium2`
*   **OCR 引擎**：`EasyOCR` (本地執行)
*   **圖片修復**：`Lama Cleaner` (IOPaint, 本地執行)
*   **PPTX 生成**：`python-pptx`

## 專案狀態 (2026-02-09)

*   [x] 核心功能 (PDF->IMG->Clean->OCR->PPTX) 完成
*   [x] 移除所有 Google API 依賴
*   [x] 整合 Lama Cleaner 與 EasyOCR
*   [x] 完成 CLI 與 GUI 介面開發
*   [x] 專案結構優化與清理

## 下一步計畫

*   [ ] 效能優化 (多執行緒/批次處理)
*   [ ] 支援 GPU 加速設定
*   [ ] 封裝為獨立執行檔 (.exe)
