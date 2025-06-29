import requests
import json
import time

with open("config.json") as f:
    config = json.load(f)

client_id = config["spotify"]["client_id"]
client_secret = config["spotify"]["client_secret"]
refresh_token = config["spotify"]["refresh_token"]

def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        },
    )
    if response.status_code != 200:
        print("Erro ao renovar token:", response.text)
        return None
    return response.json()["access_token"]

def get_current_track():
    token = get_access_token()
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if response.status_code == 204:
        return None  # Nada tocando
    elif response.status_code != 200:
        print("Erro ao buscar faixa:", response.text)
        return None

    data = response.json()
    if not data.get("is_playing"):
        return None

    track = data["item"]
    return {
        "name": track["name"],
        "artist": ", ".join([a["name"] for a in track["artists"]]),
        "album": track["album"]["name"],
        "image_url": track["album"]["images"][0]["url"]
    }

if __name__ == "__main__":
    print("Consultando Spotify...")
    track = get_current_track()
    if track:
        print("🎵 Tocando agora:")
        print(f"{track['name']} – {track['artist']}")
        print(f"Álbum: {track['album']}")
        print(f"Capa: {track['image_url']}")
    else:
        print("Nada tocando no momento.")
