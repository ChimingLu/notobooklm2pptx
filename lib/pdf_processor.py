import pypdfium2 as pdfium
from PIL import Image

def pdf_to_images(pdf_path, dpi=100):
    """
    將 PDF 每頁轉為 PIL Image，並同時回傳每頁的原始尺寸。

    回傳:
        (images, page_sizes)
        - images: list of PIL Image
        - page_sizes: list of (width_pt, height_pt)，以 PDF 點（pt）為單位
    """
    pdf = pdfium.PdfDocument(pdf_path)
    images = []
    page_sizes = []

    for i in range(len(pdf)):
        page = pdf.get_page(i)
        width_pt, height_pt = page.get_width(), page.get_height()
        page_sizes.append((width_pt, height_pt))

        bitmap = page.render(scale=dpi / 72)
        pil_image = bitmap.to_pil()
        images.append(pil_image)

    return images, page_sizes
