from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import math
from datetime import datetime
import json
import os


def draw_noise_image(width=250, height=122):
    arr = np.random.choice([0, 255], (height, width)).astype('uint8')
    return Image.fromarray(arr, 'L').convert('1')

def draw_fractal_image(width=250, height=122, max_iter=40):
    image = Image.new("1", (width, height), 1)
    pixels = image.load()

    now = datetime.now()
    total_minutes = now.hour * 60 + now.minute
    day_of_week = now.weekday()  # 0 = segunda, 6 = domingo

    # Zoom controlado por horário (logarítmico)
    zoom_factor = math.log(total_minutes + 1) * 0.3 + 0.8
    zoom = 1.5 / zoom_factor * 1.5

    # Variação horizontal conforme o dia da semana
    center_x = -0.75 + (day_of_week - 3) * 0.2  # varia de -1.35 a -0.15
    center_y = 0.0

    # Define plano complexo
    re_start = center_x - zoom
    re_end = center_x + zoom
    im_start = center_y - (zoom * height / width)
    im_end = center_y + (zoom * height / width)

    for x in range(width):
        for y in range(height):
            c = complex(
                re_start + (x / width) * (re_end - re_start),
                im_start + (y / height) * (im_end - im_start)
            )
            z = 0
            iter_count = 0
            while abs(z) <= 2 and iter_count < max_iter:
                z = z*z + c
                iter_count += 1

            pixels[x, y] = 0 if iter_count < max_iter else 1

    return image

def draw_waveform_image(width=250, height=122):
    image = Image.new("1", (width, height), 1)
    draw = ImageDraw.Draw(image)

    num_waves = random.randint(3, 6)
    spacing = random.randint(8, 16)  # espaço vertical entre ondas

    for i in range(num_waves):
        freq = random.uniform(0.03, 0.12)
        amp = random.randint(10, 30)
        phase = random.uniform(0, 2 * math.pi)
        thickness = random.randint(1, 2)

        for y_offset in range(0, height, spacing):
            points = []
            for x in range(width):
                y = int(y_offset + math.sin(x * freq + phase) * amp)
                if 0 <= y < height:
                    points.append((x, y))
            # Desenha linha de pontos
            if len(points) > 1:
                for t in range(thickness):
                    offset = t - (thickness // 2)
                    shifted = [(x, y + offset) for (x, y) in points if 0 <= y + offset < height]
                    draw.line(shifted, fill=0)

    return image

def draw_doppler_image(width=250, height=122):
    image = Image.new("1", (width, height), 1)
    draw = ImageDraw.Draw(image)

    num_sources = random.randint(5, 10)
    spacing = random.randint(12, 18)
    max_radius = int(math.hypot(width, height))

    sources = [
        (random.randint(0, width), random.randint(0, height))
        for _ in range(num_sources)
    ]

    for (cx, cy) in sources:
        for r in range(0, max_radius, spacing):
            x0 = cx - r
            y0 = cy - r
            x1 = cx + r
            y1 = cy + r
            # Evita desenhar fora da imagem
            if x1 < 0 or y1 < 0 or x0 > width or y0 > height:
                continue
            draw.ellipse([x0, y0, x1, y1], outline=0)

    return image

def generate_matrix_glitch(width=250, height=122):
    image = Image.new("1", (width, height), 0)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 12)
    except:
        font = ImageFont.load_default()

    matrix_chars = list("ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    char_width, char_height = draw.textbbox((0, 0), "A", font=font)[2:]
    cols = width // char_width

    for col in range(cols):
        y = random.randint(0, height - char_height)
        for i in range(random.randint(2, 6)):
            char = random.choice(matrix_chars)
            ypos = y - i * char_height
            if ypos >= 0:
                draw.text((col * char_width, ypos), char, font=font, fill=1)

    return image


def add_datetime_overlay(image):
    draw = ImageDraw.Draw(image)
    now = datetime.now()
    text = now.strftime("%d - %b, %H:%M")

    # Tenta uma fonte legível
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Black.ttc", 14)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    padding = 4

    x = image.width - text_width - padding * 2
    y = image.height - text_height - padding * 2

    # Desenha fundo branco
    draw.rectangle((x, y, x + text_width + padding * 2, y + text_height + padding * 2), fill=255)

    # Desenha texto preto
    draw.text((x + padding, y + padding), text, font=font, fill=0)

    return image

GLITCH_FUNCTIONS = {
    "noise": draw_noise_image,
    "fractal": draw_fractal_image,
    "waveform": draw_waveform_image,
    "doppler": draw_doppler_image,
    "matrix": generate_matrix_glitch,
}


RECENT_FILE = "recent_glitches.json"
MAX_HISTORY = 3


def load_recent():
    if os.path.exists(RECENT_FILE):
        try:
            with open(RECENT_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_recent(recent):
    with open(RECENT_FILE, "w") as f:
        json.dump(recent, f)


def choose_new_glitch_name():
    all_keys = list(GLITCH_FUNCTIONS.keys())
    recent = load_recent()

    available = [key for key in all_keys if key not in recent]
    if not available:
        available = all_keys

    chosen = random.choice(available)
    recent.append(chosen)
    if len(recent) > MAX_HISTORY:
        recent = recent[-MAX_HISTORY:]

    save_recent(recent)
    return chosen


def generate_glitch(width=250, height=122):
    glitch_name = choose_new_glitch_name()
    glitch_func = GLITCH_FUNCTIONS.get(glitch_name, draw_noise_image)
    image = glitch_func(width, height)
    return add_datetime_overlay(image)