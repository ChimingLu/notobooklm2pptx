import argparse
import sys
import os
import time
from rich.console import Console
import io

# Add parent directory to path so we can import lib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.pdf_processor import pdf_to_images
from lib.ocr_opensource import extract_text_opensource  # 使用免費 OCR
from lib.image_cleaner_lama import clean_image_lama_auto  # 使用 Lama Cleaner
from lib.pptx_generator import create_pptx

# Setup
console = Console()

console.print("[dim]ℹ 使用完全免費方案（EasyOCR + Lama Cleaner）[/dim]")

def run_test(pdf_path, skip_ocr=False, skip_clean=False, max_pages=None):
    """
    執行自動測試流程（完全免費版本）
    Args:
        pdf_path (str): PDF 檔案路徑
        skip_ocr (bool): 是否跳過 OCR
        skip_clean (bool): 是否跳過圖片去背
        max_pages (int): 最大測試頁數
    """
    console.print(f"[bold cyan]開始自動測試：{pdf_path}[/bold cyan]")
    
    if not os.path.exists(pdf_path):
        console.print(f"[bold red]錯誤：檔案 {pdf_path} 不存在[/bold red]")
        return False

    try:
        # 1. PDF to Images
        start_time = time.time()
        console.print("[green]STEP 1: 正在解析 PDF...[/green]")
        images = pdf_to_images(pdf_path)
        console.print(f"[green]成功解析 {len(images)} 頁 (耗時 {time.time() - start_time:.2f}s)[/green]")
        
        if max_pages and max_pages > 0:
            console.print(f"[yellow]測試模式：僅處理前 {max_pages} 頁[/yellow]")
            images = images[:max_pages]
        
        slides_data = []
        valid_slides_count = 0 
        
        for i, img in enumerate(images):
            console.print(f"\n[bold]正在處理第 {i+1}/{len(images)} 頁...[/bold]")
            slide_info = {}

            # Clean Image - 使用 Lama Cleaner
            if not skip_clean:
                console.print("  [cyan]STEP 2: 圖片去背 (Lama Cleaner)...[/cyan]")
                try:
                    bg_image = clean_image_lama_auto(img, ocr_engine='easyocr', model_name='lama')
                    if bg_image:
                         bg_stream = io.BytesIO()
                         bg_image.save(bg_stream, format="PNG")
                         bg_stream.seek(0)
                         slide_info['background_image'] = bg_stream
                         console.print("  [blue]✓ 背景生成完成[/blue]")
                    else:
                         console.print("  [yellow]⚠ 背景生成失敗[/yellow]")
                except Exception as e:
                    console.print(f"  [red]✗ 去背過程發生錯誤: {e}[/red]")

            # OCR - 使用 EasyOCR
            if not skip_ocr:
                console.print("  [yellow]STEP 3: 文字辨識 (EasyOCR)...[/yellow]")
                try:
                    text_blocks = extract_text_opensource(img, engine='easyocr')
                    slide_info['text_blocks'] = text_blocks
                    console.print(f"  [blue]✓ 辨識出 {len(text_blocks)} 個文字區塊[/blue]")
                except Exception as e:
                    console.print(f"  [red]✗ OCR 失敗: {e}[/red]")
            
            # Check if this slide has any content
            if slide_info.get('background_image') or slide_info.get('text_blocks'):
                valid_slides_count += 1
            
            slides_data.append(slide_info)
            
            # Check if this slide has any content
            if slide_info.get('background_image') or slide_info.get('text_blocks'):
                valid_slides_count += 1
            
            slides_data.append(slide_info)

        # Generate PPTX
        console.print("\n[green]STEP 4: 生成 PPTX...[/green]")
        if valid_slides_count == 0:
             console.print("[yellow]警告：未生成任何有效內容 (背景或文字)，產出的 PPTX 可能為空白。[/yellow]")

        from lib.config import get_output_path
        output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_test_output.pptx"
        output_path = get_output_path(output_filename)
        create_pptx(slides_data, output_path)
        
        if os.path.exists(output_path):
             console.print(f"\n[bold green]測試完成！檔案已生成：{output_path}[/bold green]")
             console.print(f"有效頁面數: {valid_slides_count}/{len(images)} (若為 0 表示全部失敗，請檢查 API 配額)")
             return True
        else:
             console.print("\n[bold red]測試失敗：PPTX 未生成[/bold red]")
             return False
             
    except Exception as e:
        console.print(f"\n[bold red]測試過程中發生嚴重錯誤: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="NotebookLM2PPTX 自動測試程式")
        parser.add_argument("pdf_path", help="PDF 檔案路徑")
        parser.add_argument("--skip-ocr", action="store_true", help="跳過 OCR 測試")
        parser.add_argument("--skip-clean", action="store_true", help="跳過圖片去背測試")
        
        parser.add_argument("--limit", type=int, default=3, help="限制測試頁數 (預設 3 頁以避免觸發 Rate Limit)")
    
        args = parser.parse_args()
    
        success = run_test(args.pdf_path, args.skip_ocr, args.skip_clean, args.limit)
        sys.exit(0 if success else 1)
    else:
        # Interactive mode using questionary
        import questionary
        console.print("[yellow]未偵測到參數，進入互動模式[/yellow]")
        pdf_path = questionary.path("請輸入 PDF 檔案路徑：").ask()
        if not pdf_path:
            console.print("[red]取消操作[/red]")
            sys.exit(0)
            
        choices = questionary.checkbox(
            "請選擇測試選項 (空白即為完整測試)：",
            choices=[
                "跳過 OCR",
                "跳過去背"
            ]
        ).ask()
        
        limit_str = questionary.text("請輸入測試頁數限制 (預設 3)：", default="3").ask()
        try:
            limit = int(limit_str)
        except ValueError: # Changed from bare except to specific ValueError
            limit = 3
        
        skip_ocr = "跳過 OCR" in choices
        skip_clean = "跳過去背" in choices
        
        success = run_test(pdf_path, skip_ocr=skip_ocr, skip_clean=skip_clean, max_pages=limit)
        sys.exit(0 if success else 1)

