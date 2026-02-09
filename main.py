import os
import io
import questionary
from rich.console import Console
from rich.progress import Progress
import sys

# Add current directory to path so we can import lib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.pdf_processor import pdf_to_images
from lib.ocr_opensource import extract_text_opensource  # 使用免費 OCR
from lib.image_cleaner_lama import clean_image_lama_auto  # 使用 Lama Cleaner
from lib.pptx_generator import create_pptx
from lib import config

# Setup
console = Console()
console.print("[dim]ℹ 使用完全免費方案（EasyOCR + Lama Cleaner）[/dim]")

def main():
    console.print("[bold cyan]NotebookLM 轉 PPTX (CLI 版)[/bold cyan]")
    
    action = questionary.select(
        "請選擇功能：",
        choices=[
            "1. 下載範例 PDF (測試用)", # Placeholder, maybe skip
            "2. PDF 轉 PPTX (完整流程：去背 + 文字還原)",
            "3. 僅提取文字 (白底 PPTX)",
            "4. 僅處理圖片 (去文字背景)",
            "5. 離開"
        ]
    ).ask()
    
    if action == "5. 離開":
        sys.exit()
        
    # Get PDF file
    pdf_path = questionary.path("請輸入 PDF 檔案路徑：").ask()
    if not os.path.exists(pdf_path):
        console.print("[bold red]錯誤：檔案不存在[/bold red]")
        return

    # Convert PDF to Images
    with Progress() as progress:
        task1 = progress.add_task("[green]正在解析 PDF...", total=None)
        images = pdf_to_images(pdf_path)
        progress.update(task1, completed=100)
    
    console.print(f"[green]成功解析 {len(images)} 頁[/green]")
    
    slides_data = []
    
    # Process Loop
    for i, img in enumerate(images):
        console.print(f"\n[bold]正在處理第 {i+1}/{len(images)} 頁...[/bold]")
        
        slide_info = {}
        
        # 1. Image Cleaning (Background) - 使用 Lama Cleaner
        if "完整" in action or "處理圖片" in action:
            with console.status("[cyan]正在生成去文字背景 (Lama Cleaner)..."):
                try:
                    bg_image = clean_image_lama_auto(img, ocr_engine='easyocr', model_name='lama')
                    if bg_image:
                        import io
                        bg_stream = io.BytesIO()
                        bg_image.save(bg_stream, format="PNG")
                        bg_stream.seek(0)
                        slide_info['background_image'] = bg_stream
                        console.print("  [blue]✓ 背景生成完成（Lama Cleaner）[/blue]")
                    else:
                        console.print("  [yellow]⚠ 背景生成失敗，將使用白底[/yellow]")
                except Exception as e:
                    console.print(f"  [red]✗ 背景處理錯誤: {e}[/red]")
        
        # 2. Text Extraction (OCR) - 使用 EasyOCR
        if "完整" in action or "提取文字" in action:
            with console.status("[yellow]正在辨識文字與排版 (EasyOCR)..."):
                try:
                    text_blocks = extract_text_opensource(img, engine='easyocr')
                    slide_info['text_blocks'] = text_blocks
                    console.print(f"  [blue]✓ 辨識出 {len(text_blocks)} 個文字區塊[/blue]")
                except Exception as e:
                    console.print(f"  [red]✗ OCR 錯誤: {e}[/red]")
                    slide_info['text_blocks'] = []
        
        slides_data.append(slide_info)

    # Generate PPTX
    if slides_data:
        from lib.config import get_output_path
        output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_converted.pptx"
        output_path = get_output_path(output_filename)
        create_pptx(slides_data, output_path)
        console.print(f"\n[bold green]完成！檔案已儲存為：{output_path}[/bold green]")
    else:
        console.print("[red]沒有產生任何資料[/red]")

if __name__ == "__main__":
    main()
