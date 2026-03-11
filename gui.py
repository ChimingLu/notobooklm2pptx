import flet as ft
import os
import sys
import io
import logging
import threading

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib import config

logging.basicConfig(
    filename='app_error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main(page: ft.Page):
    page.title = "NotebookLM 轉 PPTX（視窗版）- 免費版"
    page.window_width = 800
    page.window_height = 620
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(ft.Text("使用完全免費方案（EasyOCR + Lama Cleaner）", color="green", size=14))

    # --- 環境檢查 ---
    models_missing = []
    required_models = ["chinese.pth", "craft_mlt_25k.pth"] # 核心模型
    for m in required_models:
        if not os.path.exists(os.path.join(config.MODELS_DIR, m)):
            models_missing.append(m)
    
    if models_missing:
        # 顯示警告引導用戶，但不一定要強行關閉程式 (可能用戶有網路會自動下載)
        warning_msg = f"注意：模型資料夾似乎缺少必要檔案 ({', '.join(models_missing)})。首次執行轉換時將會嘗試自動下載 (約需數百 MB)，請確保網路連線。"
        page.add(ft.Container(
            content=ft.Text(warning_msg, color="orange800", size=13),
            bgcolor="amber100",
            padding=10,
            border_radius=5
        ))

    status_text = ft.Text("請選擇 PDF 或圖片檔案以開始...", size=16)
    progress_bar = ft.ProgressBar(width=600, visible=False)
    log_column = ft.Column(scroll="always", height=200)

    def log(msg, color="black"):
        log_column.controls.append(ft.Text(msg, color=color, size=12))
        log_column.update()
        if color == "red":
            logging.error(msg)
        else:
            logging.info(msg)

    def run_conversion(images, page_sizes, output_base, expand_pixels=15, mask_min_conf=0.1):
        """核心轉換流程，供 PDF 與圖片路徑共用"""
        from lib.image_cleaner_lama import clean_image_lama_auto
        from lib.ocr_opensource import extract_text_opensource
        from lib.pptx_generator import create_pptx

        slides_data = []
        total_pages = len(images)

        for i, img in enumerate(images):
            page_num = i + 1
            log(f"正在處理第 {page_num}/{total_pages} 頁...", "blue")
            slide_info = {'page_size': page_sizes[i]}

            try:
                log(f"  [{page_num}] 正在生成去文字背景 (Lama Cleaner)...", "purple")
                bg_image = clean_image_lama_auto(
                    img, 
                    ocr_engine='easyocr', 
                    model_name='lama',
                    expand_pixels=expand_pixels,
                    mask_min_confidence=mask_min_conf  # 遮罩用 OCR（建議 0.1 以下）
                )
                if bg_image:
                    bg_stream = io.BytesIO()
                    bg_image.save(bg_stream, format="PNG")
                    bg_stream.seek(0)
                    slide_info['background_image'] = bg_stream
                    log(f"  [{page_num}] 背景生成完成", "green")
                else:
                    log(f"  [{page_num}] 背景生成失敗，使用白底", "orange")
            except Exception as err:
                log(f"  [{page_num}] 背景錯誤: {err}", "red")

            try:
                log(f"  [{page_num}] 正在辨識文字 (EasyOCR)...", "orange")
                # 使用使用者設定的門檻進行辨識（避免門檻過高導致 0 文字區塊）
                text_blocks = extract_text_opensource(img, engine='easyocr', min_confidence=mask_min_conf)
                slide_info['text_blocks'] = text_blocks
                log(f"  [{page_num}] 辨識出 {len(text_blocks)} 個文字區塊", "green")
            except Exception as err:
                log(f"  [{page_num}] OCR 錯誤: {err}", "red")
                slide_info['text_blocks'] = []

            slides_data.append(slide_info)
            progress_bar.value = page_num / total_pages
            page.update()

        from lib.config import get_output_path
        output_filename = output_base + "_converted.pptx"
        output_path = get_output_path(output_filename)
        saved = create_pptx(slides_data, output_path)
        for p in saved:
            log(f"完成！檔案已儲存為：{p}", "green")
            status_text.value = f"完成！{os.path.basename(p)}"

        page.snack_bar = ft.SnackBar(ft.Text(f"轉換完成！共產生 {len(saved)} 個檔案"))
        page.snack_bar.open = True

    def process_file(file_path, source_type):
        """在背景執行緒中處理單一 PDF 或圖片來源"""
        status_text.value = f"正在處理: {os.path.basename(file_path)}"
        progress_bar.visible = True
        pick_pdf_button.disabled = True
        pick_image_button.disabled = True
        page.update()

        def run_task():
            try:
                if source_type == 'pdf':
                    log(f"開始解析 PDF: {file_path}", "blue")
                    from lib.pdf_processor import pdf_to_images
                    images, page_sizes = pdf_to_images(file_path)
                    log(f"成功解析 {len(images)} 頁", "green")
                    output_base = os.path.splitext(os.path.basename(file_path))[0]
                else:
                    log(f"載入圖片: {file_path}", "blue")
                    from lib.image_processor import collect_images_from_paths, images_to_slides, SUPPORTED_EXTENSIONS
                    image_paths = collect_images_from_paths([file_path])
                    if not image_paths:
                        log(f"未找到支援的圖片（{', '.join(SUPPORTED_EXTENSIONS)}）", "red")
                        return
                    images, page_sizes = images_to_slides(image_paths)
                    log(f"成功載入 {len(images)} 張圖片", "green")
                    output_base = os.path.splitext(os.path.basename(file_path))[0] or "images"

                try:
                    expand_px = int(expand_pixels_input.value)
                except ValueError:
                    expand_px = config.DEFAULT_MASK_EXPAND_PIXELS
                try:
                    mask_conf = float(mask_conf_input.value)
                except ValueError:
                    mask_conf = config.DEFAULT_MASK_MIN_CONFIDENCE

                run_conversion(images, page_sizes, output_base, expand_px, mask_conf)

            except Exception as ex:
                log(f"發生未預期的錯誤: {ex}", "red")
                status_text.value = "處理失敗"
                logging.exception("Unexpected error in run_task")
            finally:
                progress_bar.visible = False
                pick_pdf_button.disabled = False
                pick_image_button.disabled = False
                page.update()

        threading.Thread(target=run_task).start()

    # --- PDF 選擇 ---
    def pick_pdf_click(e):
        def _run_pick_pdf():
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                file_path = filedialog.askopenfilename(
                    title="選擇 PDF 檔案",
                    filetypes=[("PDF Files", "*.pdf")]
                )
                root.destroy()
                if file_path:
                    process_file(file_path, 'pdf')
            except Exception as ex:
                log(f"開啟 PDF 對話框失敗: {ex}", "red")
        
        threading.Thread(target=_run_pick_pdf).start()

    # --- 圖片選擇（資料夾或多選圖片）---
    def pick_image_click(e):
        choice = ft.AlertDialog(
            modal=True,
            title=ft.Text("圖片來源"),
            content=ft.Text("要選取整個資料夾，還是個別圖片檔案？"),
            actions=[
                ft.TextButton("選擇資料夾", on_click=lambda _: _pick_folder()),
                ft.TextButton("選擇圖片檔案", on_click=lambda _: _pick_images()),
            ],
        )

        def _pick_folder():
            choice.open = False
            page.update()
            
            def _run_pick_folder():
                try:
                    import tkinter as tk
                    from tkinter import filedialog
                    root = tk.Tk()
                    root.withdraw()
                    root.attributes('-topmost', True)
                    folder = filedialog.askdirectory(title="選擇包含圖片的資料夾")
                    root.destroy()
                    if folder:
                        process_file(folder, 'image')
                except Exception as ex:
                    log(f"開啟資料夾對話框失敗: {ex}", "red")
            
            threading.Thread(target=_run_pick_folder).start()

        def _pick_images():
            choice.open = False
            page.update()
            
            def _run_pick_images():
                try:
                    import tkinter as tk
                    from tkinter import filedialog
                    from lib.image_processor import SUPPORTED_EXTENSIONS
                    root = tk.Tk()
                    root.withdraw()
                    root.attributes('-topmost', True)
                    ext_str = " ".join(f"*.{ex.lstrip('.')}" for ex in SUPPORTED_EXTENSIONS)
                    files = filedialog.askopenfilenames(
                        title="選擇圖片檔案（可多選）",
                        filetypes=[("圖片檔案", ext_str)]
                    )
                    root.destroy()
                    if files:
                        image_paths = sorted(list(files), key=lambda x: os.path.basename(x).lower())
                        _run_image_paths(image_paths)
                except Exception as ex:
                    log(f"開啟圖片對話框失敗: {ex}", "red")
            
            threading.Thread(target=_run_pick_images).start()

        if hasattr(page, 'show_dialog'):
            page.show_dialog(choice)
        elif hasattr(page, 'open'):
            page.open(choice)
        else:
            page.overlay.append(choice)
            choice.open = True
            page.update()

    def _run_image_paths(image_paths):
        """直接以圖片路徑清單啟動轉換（略過資料夾收集步驟）"""
        status_text.value = f"正在處理 {len(image_paths)} 張圖片..."
        progress_bar.visible = True
        pick_pdf_button.disabled = True
        pick_image_button.disabled = True
        page.update()

        def run_task():
            try:
                log(f"載入 {len(image_paths)} 張圖片", "blue")
                from lib.image_processor import images_to_slides
                images, page_sizes = images_to_slides(image_paths)
                log(f"成功載入 {len(images)} 張圖片", "green")
                output_base = os.path.splitext(os.path.basename(image_paths[0]))[0] + "_batch"
                
                try:
                    expand_px = int(expand_pixels_input.value)
                except ValueError:
                    expand_px = config.DEFAULT_MASK_EXPAND_PIXELS
                try:
                    mask_conf = float(mask_conf_input.value)
                except ValueError:
                    mask_conf = config.DEFAULT_MASK_MIN_CONFIDENCE
                    
                run_conversion(images, page_sizes, output_base, expand_px, mask_conf)
            except Exception as ex:
                log(f"發生未預期的錯誤: {ex}", "red")
                status_text.value = "處理失敗"
                logging.exception("Unexpected error in _run_image_paths")
            finally:
                progress_bar.visible = False
                pick_pdf_button.disabled = False
                pick_image_button.disabled = False
                page.update()

        threading.Thread(target=run_task).start()

    pick_pdf_button = ft.ElevatedButton("選擇 PDF 檔案", on_click=pick_pdf_click)
    pick_image_button = ft.ElevatedButton(
        "選擇圖片（PNG / JPG ...）",
        on_click=pick_image_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_400, color=ft.Colors.WHITE)
    )

    # 進階設定區塊
    expand_pixels_input = ft.TextField(label="遮罩擴展 px", value=str(config.DEFAULT_MASK_EXPAND_PIXELS), width=150, height=40, text_size=12)
    mask_conf_input = ft.TextField(label="遮罩 OCR 門檻", value=str(config.DEFAULT_MASK_MIN_CONFIDENCE), width=150, height=40, text_size=12)
    
    advanced_explanation = ft.Column([
        ft.Text("【進階設定說明】", weight="bold", size=13, color="blueGrey700"),
        ft.Text("• 擴展 px (預設 15)：控制抹除範圍。去字後如有殘影請增加 (如 20)，若背景被吃掉太多請降低 (如 5)。", size=12, color="grey700"),
        ft.Text("• OCR 門檻 (預設 0.1)：偵測文字敏感度。若淺色浮水印沒被清掉，請降低此值 (如 0.05)。", size=12, color="grey700"),
    ], spacing=2)

    advanced_settings = ft.Container(
        content=ft.Column([
            ft.Row([expand_pixels_input, mask_conf_input], alignment="center", spacing=20),
            advanced_explanation
        ], horizontal_alignment="center", spacing=10),
        visible=False,
        padding=10,
        bgcolor="#f4f6f8",
        border_radius=8,
        margin=ft.margin.only(top=10, bottom=10)
    )
    
    def toggle_advanced(e):
        advanced_settings.visible = not advanced_settings.visible
        toggle_advanced_btn.text = "隱藏進階參數" if advanced_settings.visible else "顯示進階參數"
        page.update()
        
    toggle_advanced_btn = ft.TextButton("顯示進階參數", on_click=toggle_advanced)

    # 輸出資料夾設定
    output_path_text = ft.Text(f"輸出儲存於: {config.OUTPUT_DIR}", size=12, color=ft.Colors.GREY_700)

    def pick_output_dir_click(e):
        def _run_pick_output():
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
        
        threading.Thread(target=_run_pick_output).start()

    pick_output_button = ft.OutlinedButton("變更輸出資料夾", on_click=pick_output_dir_click, height=30)

    page.add(
        ft.Column(
            [
                ft.Text("NotebookLM 轉 PPTX 工具", size=30, weight="bold", color="blue"),
                ft.Divider(),
                ft.Row([pick_pdf_button, pick_image_button], alignment="center", spacing=20),
                ft.Row([toggle_advanced_btn], alignment="center"),
                advanced_settings,
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
                ),
                ft.Container(height=5),
                ft.Row(
                    [
                        ft.Text(
                            spans=[
                                ft.TextSpan("版次：v1.1 | 開源專案出處：", style=ft.TextStyle(color=ft.Colors.GREY_600)),
                                ft.TextSpan(
                                    "NotebookLM-to-PPTX", 
                                    url="https://github.com/ChimingLu/notobooklm2pptx.git", 
                                    style=ft.TextStyle(color=ft.Colors.BLUE, decoration=ft.TextDecoration.UNDERLINE)
                                ),
                            ],
                            size=12,
                        )
                    ],
                    alignment="center"
                )
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
