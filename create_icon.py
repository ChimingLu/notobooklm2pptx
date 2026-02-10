from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=(256, 256), output_path="app_icon.ico"):
    # Create distinct layers for icon complexity
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Background shape (Rounded Rectangle)
    bg_color = (66, 133, 244) # Google Blue
    padding = 20
    draw.rounded_rectangle(
        [(padding, padding), (size[0]-padding, size[1]-padding)], 
        radius=40, 
        fill=bg_color
    )

    # NotebookLM Page representation (White/Light Grey)
    page_color = (255, 255, 255)
    page_rect = [
        (size[0]*0.2, size[1]*0.2), 
        (size[0]*0.45, size[1]*0.8)
    ]
    draw.rectangle(page_rect, fill=page_color)
    
    # Lines on page
    line_color = (200, 200, 200)
    for i in range(1, 5):
        y = page_rect[0][1] + (page_rect[1][1] - page_rect[0][1]) * (i/6)
        draw.line(
            [(page_rect[0][0]+10, y), (page_rect[1][0]-10, y)], 
            fill=line_color, 
            width=3
        )

    # Arrow (Transformation)
    arrow_color = (255, 165, 0) # Orange
    arrow_start = (size[0]*0.48, size[1]*0.5)
    arrow_end = (size[0]*0.58, size[1]*0.5)
    draw.line([arrow_start, arrow_end], fill=arrow_color, width=8)
    # Arrow head
    draw.polygon([
        (arrow_end[0], arrow_end[1]-10),
        (arrow_end[0]+15, arrow_end[1]),
        (arrow_end[0], arrow_end[1]+10)
    ], fill=arrow_color)


    # Slide representation (Orange/Red for PPT)
    slide_color = (234, 67, 53) # Google Red / PPT Orange-ish
    slide_rect = [
        (size[0]*0.6, size[1]*0.3), 
        (size[0]*0.85, size[1]*0.7)
    ]
    # Draw slide (landscape)
    draw.rectangle([
        (size[0]*0.6, size[1]*0.35), 
        (size[0]*0.88, size[1]*0.65)
    ], fill=slide_color)
    
    # Simple chart on slide
    chart_color = (255, 255, 255)
    chart_base_y = size[1]*0.65 - 10
    chart_x_start = size[0]*0.6 + 10
    bar_width = 10
    gap = 5
    
    # Draw bars
    draw.rectangle([(chart_x_start, chart_base_y - 20), (chart_x_start+bar_width, chart_base_y)], fill=chart_color)
    draw.rectangle([(chart_x_start+bar_width+gap, chart_base_y - 40), (chart_x_start+2*bar_width+gap, chart_base_y)], fill=chart_color)
    draw.rectangle([(chart_x_start+2*(bar_width+gap), chart_base_y - 30), (chart_x_start+3*bar_width+2*gap, chart_base_y)], fill=chart_color)


    # Save as ICO
    image.save(output_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Icon created at {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_icon()
