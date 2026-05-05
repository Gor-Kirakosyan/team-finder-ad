import random
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


AVATAR_SIZE_WIDTH = 200
AVATAR_SIZE_HEIGHT = 200
FONT_SIZE = 100

COLOR_BLUE = "#4A90E2"
COLOR_MINT = "#50E3C2"
COLOR_ORANGE = "#F5A623"
COLOR_RED = "#D0021B"
COLOR_BROWN = "#8B572A"
COLOR_GREEN = "#7ED321"
COLOR_LIGHT_GREEN = "#B8E986"
COLOR_YELLOW = "#F8E71C"
COLOR_PURPLE = "#BD10E0"
COLOR_PINK = "#9013FE"
COLOR_DARK_GREEN = "#417505"
COLOR_CORAL = "#E34D4D"
COLOR_DARK_BLUE = "#2C3E50"
COLOR_ORANGE_DARK = "#E67E22"
COLOR_TEAL = "#1ABC9C"

AVATAR_COLORS = [
    COLOR_BLUE, COLOR_MINT, COLOR_ORANGE, COLOR_RED, COLOR_BROWN,
    COLOR_GREEN, COLOR_LIGHT_GREEN, COLOR_YELLOW, COLOR_PURPLE, COLOR_PINK,
    COLOR_DARK_GREEN, COLOR_CORAL, COLOR_DARK_BLUE, COLOR_ORANGE_DARK, COLOR_TEAL
]


def generate_avatar_from_initials(name, surname):
    first_letter = (name[0] if name else "U").upper()
    background_color = random.choice(AVATAR_COLORS)

    image = Image.new(
        "RGB", (AVATAR_SIZE_WIDTH, AVATAR_SIZE_HEIGHT), color=background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((AVATAR_SIZE_WIDTH - text_width) // 2,
                (AVATAR_SIZE_HEIGHT - text_height) // 2)

    draw.text(position, first_letter, fill="#FFFFFF", font=font)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"avatar_{name}_{surname}.png")


def normalize_phone(phone):
    if phone.startswith('8'):
        phone = '+7' + phone[1:]
    return phone


def validate_github_url(url):
    if url and 'github.com' not in url:
        raise ValidationError("Ссылка должна вести на GitHub")
    return url
