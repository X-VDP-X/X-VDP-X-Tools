import os
from colorama import Fore, init
import requests
from concurrent.futures import ThreadPoolExecutor

titre = "Token Close DMs"

os.system(f"title {titre}")

init(autoreset=True)

def console(title):
    print(f"{Fore.GREEN}{title}{Fore.RESET}")

def close_dm(channel_id, headers):
    try:
        response = requests.delete(f"https://discord.com/api/v8/channels/{channel_id}", headers=headers)
        if response.ok:
            print(f"{Fore.GREEN}[Succès]{Fore.RESET} Canal {channel_id} fermé.")
        else:
            print(f"{Fore.RED}[Erreur]{Fore.RESET} Échec de la fermeture du canal {channel_id}.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Erreur]{Fore.RESET} Problème de connexion pour le canal {channel_id}: {e}")

def close_all_dm(token):
    console("X-VDP-X | Menu | Close DM")
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        close_dm_request = requests.get("https://discord.com/api/v8/users/@me/channels", headers=headers)
        close_dm_request.raise_for_status()
        channels = close_dm_request.json()
        if not channels:
            print(f"{Fore.YELLOW}[Info]{Fore.RESET} Aucun canal trouvé.")
        else:
            with ThreadPoolExecutor(max_workers=10) as executor:
                for channel in channels:
                    channel_id = channel['id']
                    print(f"[ {Fore.LIGHTCYAN_EX}C {Fore.RESET}] ID: {channel_id}")
                    executor.submit(close_dm, channel_id, headers)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Erreur]{Fore.RESET} Problème de connexion: {e}")

def main():
    token = input("Token Discord (Utilisateur) -> : ")
    close_all_dm(token)

if __name__ == "__main__":
    main()
