# 參考資料

## 技術文件

### Lama Cleaner (IOPaint)
- **GitHub**: https://github.com/Sanster/IOPaint
- **PyPI**: https://pypi.org/project/iopaint/
- **說明**: 專業級開源圖片修復工具，使用 LaMa 深度學習模型
- **授權**: MIT License
- **安裝**: `pip install iopaint`

### EasyOCR
- **GitHub**: https://github.com/JaidedAI/EasyOCR
- **文件**: https://www.jaided.ai/easyocr/documentation/
- **說明**: 支援 80+ 語言的 OCR 工具
- **授權**: Apache 2.0
- **安裝**: `pip install easyocr`

### pypdfium2
- **GitHub**: https://github.com/pypdfium2-team/pypdfium2
- **文件**: https://pypdfium2.readthedocs.io/
- **說明**: PDF 處理函式庫，基於 PDFium
- **授權**: Apache 2.0 / BSD-3-Clause
- **安裝**: `pip install pypdfium2`

### python-pptx
- **GitHub**: https://github.com/scanny/python-pptx
- **文件**: https://python-pptx.readthedocs.io/
- **說明**: PowerPoint 檔案操作函式庫
- **授權**: MIT License
- **安裝**: `pip install python-pptx`

## 研究資料

### 圖片修復技術

#### LaMa (Large Masked Attention)
- **論文**: "Resolution-robust Large Mask Inpainting with Fourier Convolutions"
- **作者**: Roman Suvorov et al.
- **發表**: WACV 2022
- **重點**: 
  - 使用 Fourier 卷積處理大面積遮罩
  - 保持高解析度
  - 適合文字移除場景

#### 其他圖片修復工具對比
| 工具 | 類型 | 優點 | 缺點 |
|------|------|------|------|
| Lama Cleaner | 深度學習 | 效果最佳 | 需要模型 |
| OpenCV Inpaint | 傳統算法 | 快速 | 效果一般 |
| Stable Diffusion | 生成式 AI | 創意性強 | 資源需求高 |
| Cleanup.pictures | 線上服務 | 易用 | 需網路 |

### OCR 技術

#### EasyOCR 特點
- 基於深度學習（CRAFT + CRNN）
- 支援 80+ 語言
- 中文辨識率高
- CPU 可用（GPU 更快）

#### 替代方案
| 工具 | 優點 | 缺點 |
|------|------|------|
| Tesseract | 老牌穩定 | 中文效果較差 |
| PaddleOCR | 中文優秀 | 安裝複雜 |
| Google Vision API | 準確度高 | 需付費 |

## 網路資源

### 教學文章
1. **Lama Cleaner 使用教學**
   - https://www.youtube.com/watch?v=... (YouTube 教學)
   - https://toolify.ai/... (工具評測)

2. **圖片修復技術綜述**
   - "Best Free Open Source Image Inpainting Tools 2024"
   - 來源: Analytics Insight, GitHub

3. **PDF 處理最佳實踐**
   - pypdfium2 官方範例
   - PDF 解析度設定指南

### 相關專案
1. **IOPaint Desktop**
   - Lama Cleaner 的桌面版本
   - 提供 GUI 介面

2. **NotebookLM 原始專案**
   - Google AI Studio 範例
   - 網頁版實作參考

## API 文件

### Gemini API (備用方案)
- **文件**: https://ai.google.dev/gemini-api/docs
- **API Key**: https://aistudio.google.com/app/apikey
- **配額限制**:
  - 免費版: 15 RPM, 1,500 RPD
  - 付費版: 1,000+ RPM

### 模型資訊
- **gemini-2.0-flash**: 支援圖片生成和 OCR
- **gemini-1.5-pro**: 更高準確度，但較慢

## 開發工具

### Python 套件
```txt
# 核心功能
iopaint>=1.6.0          # Lama Cleaner
easyocr>=1.7.0          # OCR
pypdfium2>=4.0.0        # PDF 處理
python-pptx>=0.6.0      # PPTX 生成

# 圖片處理
opencv-python>=4.8.0    # 基礎圖片處理
Pillow>=9.5.0           # PIL

# 深度學習
torch>=2.0.0            # PyTorch
torchvision>=0.15.0     # 視覺模型

# 使用者介面
rich>=13.0.0            # CLI 美化
flet>=0.20.0            # GUI 框架
questionary>=2.0.0      # 互動式選單

# 工具
python-dotenv>=1.0.0    # 環境變數
```

### 開發環境
- **Python**: 3.10+
- **作業系統**: Windows 10/11
- **建議記憶體**: 8GB+
- **建議儲存**: 5GB+（含模型）

## 效能基準

### 處理速度（CPU）
| 階段 | 時間/頁 | 說明 |
|------|---------|------|
| PDF 解析 | ~1 秒 | 200 DPI |
| OCR 辨識 | ~5 秒 | EasyOCR |
| Lama 清理 | ~10 秒 | CPU 模式 |
| PPTX 生成 | <1 秒 | - |
| **總計** | **~16 秒** | 單頁完整流程 |

### GPU 加速
- 使用 CUDA: 可縮短至 ~5 秒/頁
- 需要: NVIDIA GPU, CUDA 11.8+

## 授權資訊

### 本專案
- **授權**: MIT License（待確認）
- **用途**: 教育、個人使用

### 依賴套件授權
- Lama Cleaner: MIT
- EasyOCR: Apache 2.0
- pypdfium2: Apache 2.0 / BSD-3
- python-pptx: MIT
- OpenCV: Apache 2.0

## 更新日誌

### 2026-02-08
- 新增 Lama Cleaner 參考資料
- 整理技術文件連結
- 建立效能基準資料

### 2026-02-07
- 初始版本
- 基本參考資料收集

## 相關連結

- **專案 GitHub**: (待建立)
- **問題回報**: (待建立)
- **討論區**: (待建立)

---

*最後更新: 2026-02-08*
