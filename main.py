import os
import io
import questionary
from rich.console import Console
from rich.progress import Progress
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.pdf_processor import pdf_to_images
from lib.image_processor import images_to_slides, collect_images_from_paths, SUPPORTED_EXTENSIONS
from lib.ocr_opensource import extract_text_opensource
from lib.image_cleaner_lama import clean_image_lama_auto
from lib.pptx_generator import create_pptx
from lib import config

console = Console()
console.print("[dim]使用完全免費方案（EasyOCR + Lama Cleaner）[/dim]")


def main():
    console.print("[bold cyan]NotebookLM 轉 PPTX (CLI 版)[/bold cyan]")

    action = questionary.select(
        "請選擇功能：",
        choices=[
            "1. PDF 轉 PPTX（完整流程：去背 + 文字還原）",
            "2. 圖片轉 PPTX（完整流程：去背 + 文字還原）",
            "3. 僅提取文字（白底 PPTX）",
            "4. 離開"
        ]
    ).ask()

    if action == "4. 離開":
        sys.exit()

    expand_px = config.DEFAULT_MASK_EXPAND_PIXELS
    mask_conf = config.DEFAULT_MASK_MIN_CONFIDENCE

    if "完整" in action:
        set_advanced = questionary.confirm("是否自訂進階參數？(包含遮罩擴展與偵測門檻)", default=False).ask()
        if set_advanced:
            ep_str = questionary.text(
                f"遮罩擴展 pixels (建議 5-20, 預設 {config.DEFAULT_MASK_EXPAND_PIXELS})：", 
                default=str(expand_px)
            ).ask()
            mc_str = questionary.text(
                f"遮罩偵測門檻 (建議 0.05-0.1, 預設 {config.DEFAULT_MASK_MIN_CONFIDENCE})：", 
                default=str(mask_conf)
            ).ask()
            try: expand_px = int(ep_str)
            except ValueError: pass
            try: mask_conf = float(mc_str)
            except ValueError: pass

    is_image_mode = "圖片" in action

    if is_image_mode:
        raw_path = questionary.path("請輸入圖片資料夾或圖片檔案路徑：").ask()
        if raw_path:
            raw_path = raw_path.strip('"').strip("'")
        if not raw_path or not os.path.exists(raw_path):
            console.print(f"[bold red]路徑不存在: {raw_path}[/bold red]")
            return

        image_paths = collect_images_from_paths([raw_path])
        if not image_paths:
            exts = ", ".join(SUPPORTED_EXTENSIONS)
            console.print(f"[bold red]未找到支援的圖片檔案（{exts}）[/bold red]")
            return

        with Progress() as progress:
            task1 = progress.add_task("[green]載入圖片...", total=None)
            images, page_sizes = images_to_slides(image_paths)
            progress.update(task1, completed=100)

        output_base = os.path.splitext(os.path.basename(raw_path))[0] or "images"

    else:
        pdf_path = questionary.path("請輸入 PDF 檔案路徑：").ask()
        if pdf_path:
            pdf_path = pdf_path.strip('"').strip("'")
        if not pdf_path or not os.path.exists(pdf_path):
            console.print(f"[bold red]錯誤：檔案不存在: {pdf_path}[/bold red]")
            return

        with Progress() as progress:
            task1 = progress.add_task("[green]正在解析 PDF...", total=None)
            images, page_sizes = pdf_to_images(pdf_path)
            progress.update(task1, completed=100)

        output_base = os.path.splitext(os.path.basename(pdf_path))[0]

    console.print(f"[green]成功載入 {len(images)} 頁[/green]")

    slides_data = []

    for i, img in enumerate(images):
        console.print(f"\n[bold]正在處理第 {i+1}/{len(images)} 頁...[/bold]")
        slide_info = {'page_size': page_sizes[i]}

        if "完整" in action:
            with console.status("[cyan]正在生成去文字背景 (Lama Cleaner)..."):
                try:
                    bg_image = clean_image_lama_auto(
                        img, 
                        ocr_engine='easyocr', 
                        model_name='lama',
                        expand_pixels=expand_px,
                        mask_min_confidence=mask_conf
                    )
                    if bg_image:
                        bg_stream = io.BytesIO()
                        bg_image.save(bg_stream, format="PNG")
                        bg_stream.seek(0)
                        slide_info['background_image'] = bg_stream
                        console.print("  [blue]背景生成完成（Lama Cleaner）[/blue]")
                    else:
                        console.print("  [yellow]背景生成失敗，將使用白底[/yellow]")
                except Exception as e:
                    console.print(f"  [red]背景處理錯誤: {e}[/red]")

        if "完整" in action or "提取文字" in action:
            with console.status("[yellow]正在辨識文字 (EasyOCR)..."):
                try:
                    text_blocks = extract_text_opensource(img, engine='easyocr')
                    slide_info['text_blocks'] = text_blocks
                    console.print(f"  [blue]辨識出 {len(text_blocks)} 個文字區塊[/blue]")
                except Exception as e:
                    console.print(f"  [red]OCR 錯誤: {e}[/red]")
                    slide_info['text_blocks'] = []

        slides_data.append(slide_info)

    if slides_data:
        from lib.config import get_output_path
        output_filename = output_base + "_converted.pptx"
        output_path = get_output_path(output_filename)
        saved = create_pptx(slides_data, output_path)
        for p in saved:
            console.print(f"\n[bold green]完成！檔案已儲存為：{p}[/bold green]")
    else:
        console.print("[red]沒有產生任何資料[/red]")


if __name__ == "__main__":
    main()
