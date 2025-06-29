from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import datetime

def create_music_image(track, width=250, height=122):
    from PIL import Image, ImageDraw, ImageFont
    import requests
    from io import BytesIO
    import datetime

    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)

    cover_size = 120
    margin = 1
    text_x = cover_size + margin * 2
    text_width = width - text_x - margin

    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 16)
        font_artist = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 14)
    except:
        print("Nao consegue")
        font_title = ImageFont.load_default()
        font_artist = ImageFont.load_default()

    # Capa
    try:
        response = requests.get(track["image_url"])
        album_art = Image.open(BytesIO(response.content)).convert("L")
        album_art = album_art.resize((cover_size, cover_size)).convert("1")
        image.paste(album_art, (margin, margin))
    except:
        print("⚠️ Falha ao carregar imagem do álbum")

    # Quebra de nome da música
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines[:2]

    title_lines = wrap_text(track["name"], font_title, text_width)
    for i, line in enumerate(title_lines):
        draw.text((text_x, margin + i * 18), line, font=font_title, fill=0)

    # Trunca artista
    def truncate_with_ellipsis(text, font, max_width):
        while draw.textlength(text + "...", font=font) > max_width:
            if len(text) <= 1:
                return ""
            text = text[:-1]
        return text + "..." if len(text) < len(track["artist"]) else text

    artist_text = truncate_with_ellipsis(track["artist"], font_artist, text_width)
    draw.text((text_x, margin + 40), artist_text, font=font_artist, fill=0)

    # Data e hora no canto inferior direito
    agora = datetime.datetime.now()
    info = agora.strftime("%d %b – %H:%M")  # ex: "28 Jun – 19:58"
    info_bbox = draw.textbbox((0, 0), info, font=font_artist)
    info_width = info_bbox[2] - info_bbox[0]
    draw.text((width - info_width - 4, height - 18), info, font=font_artist, fill=0)

    return image
