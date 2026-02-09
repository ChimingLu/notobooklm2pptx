"""
快速測試 PDF 資訊
"""

import sys
import pypdfium2 as pdfium

if len(sys.argv) < 2:
    print("使用方式: python check_pdf.py <PDF路徑>")
    sys.exit(1)

pdf_path = sys.argv[1]

try:
    pdf = pdfium.PdfDocument(pdf_path)
    num_pages = len(pdf)
    
    print(f"PDF 檔案: {pdf_path}")
    print(f"總頁數: {num_pages}")
    print(f"\n預估處理時間:")
    print(f"  - PDF 解析: ~{num_pages} 秒")
    print(f"  - OCR 辨識: ~{num_pages * 5} 秒 (每頁約 5 秒)")
    print(f"  - PPTX 生成: ~1 秒")
    print(f"  - 總計: 約 {num_pages * 6 + 1} 秒 ({(num_pages * 6 + 1) / 60:.1f} 分鐘)")
    
    if num_pages > 10:
        print(f"\n⚠️  警告: PDF 有 {num_pages} 頁，處理時間較長")
        print("   建議: 先測試前幾頁，或確保 API 配額充足")
    
except Exception as e:
    print(f"錯誤: {e}")
    sys.exit(1)
