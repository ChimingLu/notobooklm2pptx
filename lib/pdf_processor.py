import pypdfium2 as pdfium
import io
from PIL import Image

def pdf_to_images(pdf_path, dpi=100):
    pdf = pdfium.PdfDocument(pdf_path)
    images = []
    
    for i in range(len(pdf)):
        page = pdf.get_page(i)
        bitmap = page.render(scale=dpi/72)
        pil_image = bitmap.to_pil()
        images.append(pil_image)
        
    return images
