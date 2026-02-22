"""
終極版 PDF 轉 PPTX 工具
使用 Lama Cleaner + EasyOCR
完全免費且高品質
"""

import os
import sys
from rich.console import Console
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.pdf_processor import pdf_to_images
from lib.ocr_opensource import extract_text_opensource
from lib.image_cleaner_lama import clean_image_lama_auto
from lib.pptx_generator import create_pptx

console = Console()

def process_pdf_ultimate(pdf_path, output_name=None, max_pages=None, 
                         dpi=200, model='lama', expand_pixels=5):
    """
    終極版 PDF 轉 PPTX
    
    Args:
        pdf_path: PDF 檔案路徑
        output_name: 輸出檔名
        max_pages: 最大處理頁數
        dpi: PDF 解析度 (預設 200，可提高至 300)
        model: Lama 模型 ('lama', 'ldm', 'zits', 'mat')
        expand_pixels: 遮罩擴大像素
    """
    console.print(f"[bold cyan]終極版 PDF 轉 PPTX (Lama Cleaner + EasyOCR)[/bold cyan]")
    console.print(f"解析度: {dpi} DPI")
    console.print(f"Lama 模型: {model}")
    
    if not os.path.exists(pdf_path):
        console.print("[bold red]檔案不存在[/bold red]")
        return False
    
    # 1. PDF 轉圖片（高解析度）
    console.print("\n[yellow]步驟 1/3: 解析 PDF（高解析度）...[/yellow]")
    try:
        all_images = pdf_to_images(pdf_path, dpi=dpi)
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
    
    # 2. 處理每一頁
    console.print(f"\n[yellow]步驟 2/3: 處理頁面（Lama Cleaner + OCR）...[/yellow]")
    console.print("[cyan]首次使用會下載 Lama 模型，請稍候...[/cyan]\n")
    
    slides_data = []
    
    for i, img in enumerate(images):
        page_num = i + 1
        console.print(f"[bold]處理第 {page_num}/{len(images)} 頁[/bold]")
        
        slide_info = {}
        
        # 2a. Lama Cleaner 清理背景
        try:
            cleaned_img = clean_image_lama_auto(
                img, 
                ocr_engine='easyocr',
                model_name=model,
                expand_pixels=expand_pixels
            )
            
            if cleaned_img:
                bg_stream = io.BytesIO()
                cleaned_img.save(bg_stream, format='PNG')
                bg_stream.seek(0)
                slide_info['background_image'] = bg_stream
                console.print(f"  [green]✓ 背景清理完成[/green]")
            else:
                console.print(f"  [yellow]⚠ 背景清理失敗，跳過[/yellow]")
                
        except Exception as e:
            console.print(f"  [red]✗ 背景處理錯誤: {e}[/red]")
        
        # 2b. OCR 辨識（如果還沒做過）
        console.print(f"  [4/4] 最終 OCR 辨識...")
        try:
            text_blocks = extract_text_opensource(img, engine='easyocr')
            slide_info['text_blocks'] = text_blocks
            console.print(f"  [green]✓ {len(text_blocks)} 個文字區塊[/green]\n")
        except Exception as e:
            console.print(f"  [red]✗ OCR 錯誤: {e}[/red]\n")
            slide_info['text_blocks'] = []
        
        slides_data.append(slide_info)
    
    # 3. 生成 PPTX
    console.print("[yellow]步驟 3/3: 生成 PPTX...[/yellow]")
    
    if not output_name:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        if max_pages and max_pages < total_pages:
            output_name = f"{base_name}_Lama_前{max_pages}頁.pptx"
        else:
            output_name = f"{base_name}_Lama.pptx"
    
    try:
        from lib.config import get_output_path
        output_path = get_output_path(output_name)
        create_pptx(slides_data, output_path)
        console.print(f"\n[bold green]✓ 完成！{output_name}[/bold green]")
        console.print(f"\n輸出位置: {os.path.abspath(output_path)}")
        console.print("\n[cyan]💡 特點：[/cyan]")
        console.print("  ✅ 專業級文字移除（Lama Cleaner）")
        console.print("  ✅ 高品質 OCR（EasyOCR）")
        console.print("  ✅ 完全免費，無 API 限制")
        console.print("  ✅ 背景自然修復")
        return True
    except Exception as e:
        console.print(f"[red]✗ 失敗: {e}[/red]")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]使用方式:[/yellow]")
        console.print('  python convert_ultimate.py "PDF路徑"')
        console.print('  python convert_ultimate.py "PDF路徑" 3')
        console.print('  python convert_ultimate.py "PDF路徑" 3 --dpi 300')
        console.print("\n[cyan]說明:[/cyan]")
        console.print("  使用 Lama Cleaner 專業級圖片修復")
        console.print("  結合 EasyOCR 高品質文字辨識")
        console.print("  完全免費，效果最佳")
        console.print("\n[cyan]選項:[/cyan]")
        console.print("  --dpi N      設定解析度（預設 200，建議 200-300）")
        console.print("  --model M    Lama 模型（lama/ldm/zits/mat，預設 lama）")
        console.print("  --expand N   遮罩擴大像素（預設 5）")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    max_pages = None
    dpi = 200
    model = 'lama'
    expand = 5
    
    # 解析參數
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.isdigit():
            max_pages = int(arg)
        elif arg == '--dpi' and i + 1 < len(sys.argv):
            dpi = int(sys.argv[i + 1])
            i += 1
        elif arg == '--model' and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 1
        elif arg == '--expand' and i + 1 < len(sys.argv):
            expand = int(sys.argv[i + 1])
            i += 1
        i += 1
    
    success = process_pdf_ultimate(
        pdf_path, 
        max_pages=max_pages,
        dpi=dpi,
        model=model,
        expand_pixels=expand
    )
    sys.exit(0 if success else 1)
