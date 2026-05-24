import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Image dimensions
WIDTH = 4088
HEIGHT = 2707

# Equal padding from left edge and bottom edge
PADDING = 200

# Font settings
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_PATH = os.path.join(FONT_DIR, "Cabin-Regular.ttf")
FONT_SIZE = 100
LINE_SPACING = 20

# Heavenly gradient palettes: each is (top_color, bottom_color)
GRADIENT_PALETTES = [
    # Soft blue sky
    ((25, 100, 200), (135, 220, 250)),
    # Deep blue to cyan
    ((10, 60, 150), (100, 210, 240)),
    # Purple dawn
    ((80, 40, 130), (180, 140, 220)),
    # Golden sunrise
    ((20, 60, 120), (240, 180, 100)),
    # Rose heaven
    ((100, 40, 80), (230, 160, 180)),
    # Teal serenity
    ((10, 80, 100), (120, 220, 210)),
    # Lavender mist
    ((60, 50, 120), (200, 180, 240)),
    # Ocean depth to light
    ((5, 30, 80), (80, 180, 220)),
    # Peach sunset
    ((60, 40, 80), (250, 180, 150)),
    # Emerald grace
    ((10, 60, 60), (130, 210, 180)),
    # Midnight blue to soft blue
    ((15, 20, 60), (100, 150, 220)),
    # Warm violet
    ((50, 20, 80), (180, 120, 200)),
    # Sky blue classic
    ((0, 90, 180), (135, 206, 250)),
    # Dusk pink
    ((40, 30, 70), (220, 150, 170)),
    # Celestial gold
    ((30, 50, 100), (220, 200, 140)),
]


def generate_gradient(width, height, top_color, bottom_color):
    """Generate a vertical gradient image from top_color to bottom_color."""
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return image


def get_luminance(r, g, b):
    """Calculate relative luminance of a color."""
    return 0.299 * r + 0.587 * g + 0.114 * b


def get_text_color(image, text_x, text_y, text_width, text_height):
    """Determine text color (dark or white) based on luminance of the text region."""
    # Sample the region where text will be placed
    region = image.crop((text_x, text_y, text_x + text_width, text_y + text_height))
    pixels = list(region.tobytes())
    # Convert flat byte list to RGB tuples
    pixels = [(pixels[i], pixels[i+1], pixels[i+2]) for i in range(0, len(pixels), 3)]

    if not pixels:
        return (0, 0, 0)

    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)

    luminance = get_luminance(avg_r, avg_g, avg_b)

    # Use white text on dark backgrounds, dark text on light backgrounds
    if luminance < 140:
        return (255, 255, 255)
    else:
        return (20, 20, 20)


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def generate_verse_image(verse_text, reference, output_path="output.png"):
    """Generate a poster image with a Bible verse on a gradient background."""
    # Pick a random gradient palette
    top_color, bottom_color = random.choice(GRADIENT_PALETTES)

    # Generate gradient
    image = generate_gradient(WIDTH, HEIGHT, top_color, bottom_color)
    draw = ImageDraw.Draw(image)

    # Load font
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Format the quote text
    full_text = f'"{verse_text}" \u2013 {reference}'

    # Max text width: from left padding to 60% of image width
    max_text_width = int(WIDTH * 0.6)

    # Wrap text
    lines = wrap_text(full_text, font, max_text_width, draw)

    # Calculate total text block height
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_heights.append(bbox[3] - bbox[1])

    total_text_height = sum(line_heights) + LINE_SPACING * (len(lines) - 1)

    # Position: bottom-left with equal padding from left and bottom
    text_x = PADDING
    text_y = HEIGHT - PADDING - total_text_height

    # Determine text color based on background luminance in text region
    text_color = get_text_color(image, text_x, text_y, max_text_width, total_text_height)

    # Draw each line
    current_y = text_y
    for line in lines:
        draw.text((text_x, current_y), line, font=font, fill=text_color)
        bbox = draw.textbbox((0, 0), line, font=font)
        current_y += (bbox[3] - bbox[1]) + LINE_SPACING

    # Save the image
    image.save(output_path, "PNG")
    return output_path


if __name__ == "__main__":
    # Fetch a live random verse for testing
    from main import fetch_random_verse
    verse, ref = fetch_random_verse()
    output = generate_verse_image(verse, ref, "test_output.png")
    print(f"Generated test image: {output}")
    print(f"Verse: \"{verse}\" \u2013 {ref}")
