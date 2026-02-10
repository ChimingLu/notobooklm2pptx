import flet as ft
import os
import sys
import logging
import threading
import time

# Add current directory to path so we can import lib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.pdf_processor import pdf_to_images
from lib.ocr_opensource import extract_text_opensource  # 使用免費 OCR
from lib.image_cleaner_lama import clean_image_lama_auto  # 使用 Lama Cleaner
from lib.pptx_generator import create_pptx
from lib import config

# Setup Logging
logging.basicConfig(
    filename='app_error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Setup

def main(page: ft.Page):
    page.title = "NotebookLM 轉 PPTX (視窗版) - 免費版"
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 不再需要 API Key
    page.add(ft.Text("✓ 使用完全免費方案（EasyOCR + Lama Cleaner）", color="green", size=14))

    # UI Components
    status_text = ft.Text("請選擇 PDF 檔案以開始...", size=16)
    progress_bar = ft.ProgressBar(width=600, visible=False)
    log_column = ft.Column(scroll="always", height=200)
    
    def log(msg, color="black"):
        log_column.controls.append(ft.Text(msg, color=color, size=12))
        log_column.update()
        if color == "red":
            logging.error(msg)
        else:
            logging.info(msg)

    def process_pdf(e):
        if not e.files:
            return
            
        file_path = e.files[0].path
        status_text.value = f"正在處理: {os.path.basename(file_path)}"
        progress_bar.visible = True
        pick_files_button.disabled = True
        page.update()
        
        def run_task():
            try:
                log(f"開始解析 PDF: {file_path}", "blue")
                pdf_images = pdf_to_images(file_path)
                log(f"成功解析 {len(pdf_images)} 頁", "green")
                
                slides_data = []
                total_pages = len(pdf_images)
                
                for i, img in enumerate(pdf_images):
                    page_num = i + 1
                    log(f"正在處理第 {page_num}/{total_pages} 頁...", "blue")
                    
                    slide_info = {}
                    
                    # 1. Image Cleaning - 使用 Lama Cleaner
                    try:
                        log(f"  [{page_num}] 正在生成去文字背景 (Lama Cleaner)...", "purple")
                        bg_image = clean_image_lama_auto(img, ocr_engine='easyocr', model_name='lama')
                        if bg_image:
                            import io
                            bg_stream = io.BytesIO()
                            bg_image.save(bg_stream, format="PNG")
                            bg_stream.seek(0)
                            slide_info['background_image'] = bg_stream
                            log(f"  [{page_num}] ✓ 背景生成完成", "green")
                        else:
                            log(f"  [{page_num}] ⚠ 背景生成失敗", "orange")
                    except Exception as err:
                        log(f"  [{page_num}] ✗ 背景錯誤: {err}", "red")

                    # 2. OCR - 使用 EasyOCR
                    try:
                        log(f"  [{page_num}] 正在辨識文字 (EasyOCR)...", "orange")
                        text_blocks = extract_text_opensource(img, engine='easyocr')
                        slide_info['text_blocks'] = text_blocks
                        log(f"  [{page_num}] ✓ 辨識出 {len(text_blocks)} 個文字區塊", "green")
                    except Exception as err:
                         log(f"  [{page_num}] ✗ OCR 錯誤: {err}", "red")
                         slide_info['text_blocks'] = []
                    
                    slides_data.append(slide_info)
                    progress_bar.value = page_num / total_pages
                    page.update()
                
                # Generate PPTX
                from lib.config import get_output_path
                output_filename = os.path.splitext(os.path.basename(file_path))[0] + "_converted.pptx"
                output_path = get_output_path(output_filename)
                create_pptx(slides_data, output_path)
                
                log(f"完成！檔案已儲存為：{output_path}", "green")
                status_text.value = f"完成！檔案已儲存為：{output_path}"
                
                page.snack_bar = ft.SnackBar(ft.Text(f"完成！儲存於: {output_path}"))
                page.snack_bar.open = True
                
            except Exception as ex:
                log(f"發生未預期的錯誤: {ex}", "red")
                status_text.value = "處理失敗"
                logging.exception("Unexpected error in run_task")
                
            finally:
                progress_bar.visible = False
                pick_files_button.disabled = False
                page.update()

        threading.Thread(target=run_task).start()

    # Function to handle file picking using Tkinter (native dialog)
    def pick_files_click(e):
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            # Hide the root Tk window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True) # Bring dialog to front
            
            file_path = filedialog.askopenfilename(
                title="選擇 PDF 檔案",
                filetypes=[("PDF Files", "*.pdf")]
            )
            
            root.destroy()
            
            if file_path:
                # Mock an event object to reuse processing logic
                class FileEvent:
                    def __init__(self, path):
                        self.path = path
                        
                class EventWrapper:
                    def __init__(self, path):
                        self.files = [FileEvent(path)]
                        
                # Use a separate thread to avoid freezing the UI during processing if not already threaded?
                # process_pdf already starts a thread!
                process_pdf(EventWrapper(file_path))
                
        except Exception as ex:
            log(f"開啟檔案對話框失敗: {ex}", "red")
            logging.error(f"File dialog error: {ex}")

    pick_files_button = ft.ElevatedButton(
        "選擇 PDF 檔案",
        on_click=pick_files_click
    )

    # 選擇輸出資料夾功能
    output_path_text = ft.Text(f"輸出儲存於: {config.OUTPUT_DIR}", size=12, color=ft.Colors.GREY_700)
    
    def pick_output_dir_click(e):
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            folder_selected = filedialog.askdirectory(
                title="選擇輸出資料夾",
                initialdir=config.OUTPUT_DIR
            )
            
            root.destroy()
            
            if folder_selected:
                config.set_output_dir(folder_selected)
                output_path_text.value = f"輸出儲存於: {config.OUTPUT_DIR}"
                log(f"輸出路徑已變更為: {config.OUTPUT_DIR}", "blue")
                page.update()
                
        except Exception as ex:
            log(f"選擇資料夾失敗: {ex}", "red")

    pick_output_button = ft.OutlinedButton(
        "變更輸出資料夾",
        on_click=pick_output_dir_click,
        height=30,
    )

    page.add(
        ft.Column(
            [
                ft.Text("NotebookLM 轉 PPTX 工具", size=30, weight="bold", color="blue"),
                ft.Divider(),
                ft.Row([pick_files_button], alignment="center"),
                ft.Container(height=10),
                ft.Row([output_path_text, pick_output_button], alignment="center"),
                ft.Container(height=20),
                ft.Row([status_text], alignment="center"),
                progress_bar,
                ft.Container(height=20),
                ft.Text("執行日誌:", weight="bold"),
                ft.Container(
                    content=log_column,
                    border=ft.border.all(1, ft.Colors.GREY),
                    border_radius=10,
                    padding=10,
                    bgcolor=ft.Colors.GREY_100,
                    expand=True,
                )
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)


