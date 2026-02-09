from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_pptx(slides_data, output_file):
    """
    slides_data: List of dictionaries.
    Each dict contains:
      - background_image: PIL Image or path (optional)
      - text_blocks: List of OCR blocks (optional)
    """
    prs = Presentation()
    # Set to wide screen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_slide_layout = prs.slide_layouts[6] 
    
    for slide_data in slides_data:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # 1. Add Background if available
        if 'background_image' in slide_data and slide_data['background_image']:
            # Save temp image or use stream? python-pptx needs file path or file-like object
            # Assuming it's a file path or BytesIO
            try:
                slide.shapes.add_picture(slide_data['background_image'], 0, 0, prs.slide_width, prs.slide_height)
            except Exception as e:
                print(f"Error adding background: {e}")

        # 2. Add Text Blocks
        if 'text_blocks' in slide_data:
            for block in slide_data['text_blocks']:
                text = block.get('text', '')
                if not text: continue
                
                box = block.get('box_2d', [0, 0, 0, 0])
                # box is [ymin, xmin, ymax, xmax] in 0-1000 scale
                ymin, xmin, ymax, xmax = box
                
                # Convert to inches
                left = (xmin / 1000) * prs.slide_width
                top = (ymin / 1000) * prs.slide_height
                width = ((xmax - xmin) / 1000) * prs.slide_width
                height = ((ymax - ymin) / 1000) * prs.slide_height
                
                textbox = slide.shapes.add_textbox(left, top, width, height)
                tf = textbox.text_frame
                tf.word_wrap = True
                
                p = tf.paragraphs[0]
                p.text = text
                
                # Formatting
                # Formatting
                # Calculate font size from box height to handle resolution differences
                # box values are 0-1000 relative to slide
                box_height_rel = (ymax - ymin) / 1000
                slide_height_pt = 7.5 * 72  # 540 points
                # Factor 0.75 estimates font size from line height
                calculated_size = int(box_height_rel * slide_height_pt * 0.75)
                
                # Enforce reasonable limits
                if calculated_size < 8: calculated_size = 8
                if calculated_size > 100: calculated_size = 100
                
                p.font.size = Pt(calculated_size)
                    
                if block.get('is_bold'):
                    p.font.bold = True
                    
                # Color handling (simple hex)
                color_hex = block.get('color', '000000').replace('#', '')
                try:
                    p.font.color.rgb = RGBColor.from_string(color_hex)
                except:
                    p.font.color.rgb = RGBColor(0, 0, 0)
                    
                # Alignment
                align = block.get('align', 'left').lower()
                if 'center' in align:
                    p.alignment = PP_ALIGN.CENTER
                elif 'right' in align:
                    p.alignment = PP_ALIGN.RIGHT
                else:
                    p.alignment = PP_ALIGN.LEFT

    prs.save(output_file)
    print(f"PPTX saved to {output_file}")
