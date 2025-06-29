from spotify import get_current_track
from glitch import generate_glitch
from display import show_image
import time

def main_loop():
    while True:
        track = get_current_track()
        if track:
            print("Música tocando:", track['name'])
            # Aqui geraria imagem da música e exibiria
        else:
            print("Nada tocando, gerando glitch...")
            img = generate_glitch()
            show_image(img)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
