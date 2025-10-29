from PIL import Image, ImageDraw, ImageFont
import os

def generate_summary_image(total, top5, timestamp, output_path):

    img = Image.new('RGB', (1000, 600), color=(255,255,255))
    draw = ImageDraw.Draw(img)

    title = f"Country Data Summary - Total: {total}"
    draw.text((20, 20), title, fill=(0,0,0))
    draw.text((20,60), f"Refreshed: {timestamp.isoformat()}", fill=(0,0,0))
    draw.text((20,100), "Top 5 Countries by GDP:", fill=(0,0,0))

    y = 150

    for i,c in enumerate(top5, start=1):
        line = f"{i}. {c.name} - {c.estimated_gdp:,.2f}"
        draw.text((40,y), line, fill=(0,0,0))

        y += 40

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)