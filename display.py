import os
from PIL import Image

# Flag: está rodando no Raspberry?
ON_RASPBERRY = os.uname().machine in ("armv7l", "aarch64")

if ON_RASPBERRY:
    from waveshare_epd import epd2in13b_V4
    import logging
    import time

    epd = epd2in13b_V4.EPD()
    epd.init()
    epd.Clear()
    logging.basicConfig(level=logging.INFO)

def show_image(img):
    if ON_RASPBERRY:
        print("Enviando imagem para o display e-ink...")
        bw_img = img.convert("1")  # converte para 1-bit se não estiver já
        epd.display(epd.getbuffer(bw_img), epd.getbuffer(Image.new("1", img.size, 255)))
        epd.sleep()
    else:
        print("Salvando preview local...")
        img.save("preview_output.png")