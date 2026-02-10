# 打包與發佈指南

已完成 Python 獨立執行檔 (Single-folder Executable) 的製作。請依照以下步驟完成最終安裝檔 (`Setup.exe`) 的製作與驗證。

## 1. 驗證執行檔
在製作安裝程式前，請先測試已產生的執行檔是否運作正常：
1.  進入資料夾：`dist\NotebookLM2PPTX`
2.  執行：`NotebookLM2PPTX.exe` (可能會看到一個黑色命令視窗伴隨 GUI 開啟，這是為了除錯方便，正式版可關閉)
3.  測試功能：
    -   點擊「選擇 PDF 檔案」並轉換一個檔案。
    -   確認 OCR 模型載入成功 (console log 應無錯誤)。
    -   確認 Lama Cleaner 模型載入成功。
    -   確認 PPTX 輸出至預設的文件資料夾 (或是您指定的資料夾)。

## 2. 製作安裝程式 (Setup.exe)
您需要安裝 [Inno Setup](https://jrsoftware.org/isdl.php) (免費開源安裝製作工具)。

1.  安裝 Inno Setup。
2.  雙擊開啟專案根目錄下的 `setup_script.iss`。
3.  在 Inno Setup 編譯器中，點擊 **Build > Compile** (或按 Ctrl+F9)。
4.  編譯完成後，安裝檔 `NotebookLM2PPTX_Setup.exe` 將產生於 `installers` 資料夾中。

## 3. 安裝與測試
1.  將 `NotebookLM2PPTX_Setup.exe` 複製到桌面或其他位置。
2.  執行安裝程式，依指示安裝。
    -   確認是否建立桌面捷徑。
3.  安裝完成後，直接點擊桌面捷徑執行。
4.  再次進行功能測試。

## 常見問題
- **執行檔過大**：因為包含了 Torch 和完整的 AI 模型 (EasyOCR, Lama)，總大小可能接近 1GB，這是離線執行的必要代價。
- **防毒軟體誤判**：未簽章的執行檔可能會被 Windows Defender 警告，這是正常現象，點擊「仍要執行」即可。
