"""
使用免費 OCR 的 PDF 轉 PPTX 工具
不需要 Gemini API 配額
"""

import os
import sys
from rich.console import Console

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.pdf_processor import pdf_to_images
from lib.ocr_opensource import extract_text_opensource
from lib.pptx_generator import create_pptx

console = Console()

def process_pdf_free(pdf_path, output_name=None, max_pages=None, ocr_engine='easyocr'):
    """
    使用免費 OCR 處理 PDF
    
    Args:
        pdf_path: PDF 檔案路徑
        output_name: 輸出檔名
        max_pages: 最大處理頁數
        ocr_engine: 'tesseract' 或 'easyocr'
    """
    console.print(f"[bold cyan]使用免費 OCR 處理 PDF[/bold cyan]")
    console.print(f"OCR 引擎: {ocr_engine}")
    
    if not os.path.exists(pdf_path):
        console.print("[bold red]檔案不存在[/bold red]")
        return False
    
    # 1. PDF 轉圖片
    console.print("\n[yellow]步驟 1/3: 解析 PDF...[/yellow]")
    try:
        all_images = pdf_to_images(pdf_path)
        total_pages = len(all_images)
        
        if max_pages and max_pages < total_pages:
            images = all_images[:max_pages]
            console.print(f"[yellow]⚠️  僅處理前 {max_pages} 頁（共 {total_pages} 頁）[/yellow]")
        else:
            images = all_images
        
        console.print(f"[green]✓ 解析完成，將處理 {len(images)} 頁[/green]")
        
    except Exception as e:
        console.print(f"[red]✗ PDF 解析失敗: {e}[/red]")
        return False
    
    # 2. OCR 辨識
    console.print(f"\n[yellow]步驟 2/3: 文字辨識（{ocr_engine}）...[/yellow]")
    
    if ocr_engine == 'easyocr':
        console.print("[cyan]首次使用會下載模型，請稍候...[/cyan]")
    
    slides_data = []
    
    for i, img in enumerate(images):
        page_num = i + 1
        console.print(f"  [{page_num}/{len(images)}] 辨識中...", end="")
        
        try:
            text_blocks = extract_text_opensource(img, engine=ocr_engine)
            slides_data.append({'text_blocks': text_blocks})
            console.print(f" [green]✓ {len(text_blocks)} 個區塊[/green]")
            
        except Exception as e:
            console.print(f" [red]✗ 失敗: {e}[/red]")
            slides_data.append({'text_blocks': []})
    
    # 3. 生成 PPTX
    console.print("\n[yellow]步驟 3/3: 生成 PPTX...[/yellow]")
    
    if not output_name:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        if max_pages and max_pages < total_pages:
            output_name = f"{base_name}_OCR_前{max_pages}頁.pptx"
        else:
            output_name = f"{base_name}_OCR.pptx"
    
    try:
        from lib.config import get_output_path
        output_path = get_output_path(output_name)
        create_pptx(slides_data, output_path)
        console.print(f"\n[bold green]✓ 完成！{output_name}[/bold green]")
        console.print(f"\n輸出位置: {os.path.abspath(output_path)}")
        return True
    except Exception as e:
        console.print(f"[red]✗ 失敗: {e}[/red]")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]使用方式:[/yellow]")
        console.print('  python convert_free.py "PDF路徑"')
        console.print('  python convert_free.py "PDF路徑" 5              # 前 5 頁')
        console.print('  python convert_free.py "PDF路徑" 5 tesseract   # 使用 Tesseract')
        console.print('  python convert_free.py "PDF路徑" 5 easyocr     # 使用 EasyOCR（預設）')
        console.print("\n[cyan]注意：首次使用需要安裝 OCR 工具[/cyan]")
        console.print("  EasyOCR: pip install easyocr")
        console.print("  Tesseract: pip install pytesseract + 下載 Tesseract")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    ocr_engine = sys.argv[3] if len(sys.argv) > 3 else 'easyocr'
    
    success = process_pdf_free(pdf_path, max_pages=max_pages, ocr_engine=ocr_engine)
    sys.exit(0 if success else 1)
