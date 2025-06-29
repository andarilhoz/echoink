import requests
import urllib.parse
import webbrowser
import json

# Carregue as credenciais do config.json
with open("config.json") as f:
    config = json.load(f)
    client_id = config["spotify"]["client_id"]
    client_secret = config["spotify"]["client_secret"]
    redirect_uri = "https://example.com/callback"
    scopes = "user-read-playback-state user-read-currently-playing"

# 1. Criar URL de autorização
auth_url = "https://accounts.spotify.com/authorize"
params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scopes
}
url = f"{auth_url}?{urllib.parse.urlencode(params)}"

print("Abra este link no navegador para autorizar:")
print(url)
webbrowser.open(url)

# 2. Solicita o código da URL manualmente
code = input("\nDepois de autorizar, cole o parâmetro 'code' da URL aqui:\n> ").strip()

# 3. Trocar o code pelo token
token_url = "https://accounts.spotify.com/api/token"
payload = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(token_url, data=payload)
if response.status_code != 200:
    print("Erro ao obter token:", response.text)
    exit(1)

data = response.json()
refresh_token = data["refresh_token"]
access_token = data["access_token"]

# 4. Salvar refresh_token no config.json
config["spotify"]["refresh_token"] = refresh_token
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

print("\nAutenticação concluída!")
print("Refresh token salvo no config.json.")
