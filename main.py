from spotify import get_current_track
from glitch import generate_glitch
from render_music import create_music_image   # ← Novo import aqui
from display import show_image
import time

def main_loop():
    while True:
        track = get_current_track()
        if track:
            print(f"Tocando: {track['name']} - {track['artist']}")
            image = create_music_image(track)
        else:
            print("Nada tocando. Gerando glitch...")
            image = generate_glitch()

        show_image(image)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
