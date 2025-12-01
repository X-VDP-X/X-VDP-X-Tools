import requests

def check_token(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    url = "https://discord.com/api/v9/users/@me"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"[VALID] Token valide !")
        print(f"Username: {data['username']}#{data['discriminator']}")
        print(f"ID: {data['id']}")
        print(f"Avatar: https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png")
    else:
        print("[INVALID] Token invalide ou expiré.")

if __name__ == "__main__":
    while True:
        token = input("Token Discord à vérifier : ").strip()
        check_token(token)
        cont = input("Veux-tu continuer ? (o/n) : ").strip().lower()
        if cont != 'o':
            break
