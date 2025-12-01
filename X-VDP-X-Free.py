import os
import subprocess
import time
import webbrowser
import sys
from colorama import Fore, init

titre = "X-VDP-X Free 1.5"
os.system(f"title {titre}" if os.name == "nt" else "")

init(autoreset=True)

logo = """
██╗░░██╗░░░░░░██╗░░░██╗██████╗░██████╗░░░░░░░██╗░░██╗
╚██╗██╔╝░░░░░░██║░░░██║██╔══██╗██╔══██╗░░░░░░╚██╗██╔╝
░╚███╔╝░█████╗╚██╗░██╔╝██║░░██║██████╔╝█████╗░╚███╔╝░
░██╔██╗░╚════╝░╚████╔╝░██║░░██║██╔═══╝░╚════╝░██╔██╗░
██╔╝╚██╗░░░░░░░░╚██╔╝░░██████╔╝██║░░░░░░░░░░░██╔╝╚██╗
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░░░░░░░░░░╚═╝░░╚═╝
"""

red = Fore.RED
blue = Fore.LIGHTBLUE_EX
reset = Fore.RESET

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    clear_screen()
    terminal_width = os.get_terminal_size().columns
    for line in logo.splitlines():
        padding = max((terminal_width - len(line)) // 2, 0)
        print(blue + " " * padding + line)

def print_menu():
    menu = f"""{red}
╔═════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                          MENU PRINCIPAL                                         ║
╠═════════════════╗════════════╗═══════════════════════════════════════════╔═══════╗══════════════╣
║ TOOL-HACKING    ║ IP-DEAD    ║                   X-VDP-X                 ║ DDOS  ║   SUB        ║
╠═════════════════╝════════════╝═══════════════════════════════════════════╚═══════╝══════════════╣
║ Page N°1                                                                                        ║
║ [1]. Ip-Scanner                    [7]. Port-Scanner                [13]. Browser-Private       ║
║ [2]. Bot-Nuke                      [8]. Ip-Pinger                   [14]. Dark-Web              ║
║ [3]. Fake-Info                     [9]. Bot-Mass-DM                 [15]. Token-Close-DM        ║                 
║ [4]. DOS-URL                       [10]. DOS-IP                     [16]. Email-Info            ║
║ [5]. My-Token-discord              [11]. Sub-Domain-Scanner         [17]. Token-Checker         ║
║ [6]. Subdirectory-Scanner          [12]. Server-Info                [18]. Token-Info            ║
║ [19]. Token-Grabber                [20]. Builder-Keylloger          [21]. Tools-info            ║
║ [22]. Ip-Website                   [23]. Buy-Hack-X-VDP-X           [24]. Password-Dehash       ║
╚═════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
    print(menu + reset)

def run_script(path):
    if not os.path.isfile(path):
        print(red + f"[!] Script non trouvé : {path}")
        time.sleep(2)
        return
    try:
        subprocess.run([sys.executable, path], check=True)
    except subprocess.CalledProcessError as e:
        print(red + f"[!] Erreur lors de l'exécution : {e}")
        time.sleep(2)

def main():
    script_paths = {
        '1': 'Hacking/Ip-scanner.py',
        '2': 'Hacking/Bot-Nuke.py',
        '3': 'Hacking/Fake-Info.py',
        '4': 'Hacking/Dos-Url.py',
        '5': 'Hacking/My-Token-discord.py',
        '6': 'Hacking/Subdirectory-scanner.py',
        '7': 'Hacking/Port-Scanner.py',
        '8': 'Hacking/Ip-Pinger.py',
        '9': 'Hacking/Bot-Spam-DM.py',
        '10': 'Hacking/DOS-IP.py',
        '11': 'Hacking/Subdomain.py',  
        '12': 'Hacking/Server-Info.py',
        '13': 'Hacking/Browser-Private.py',
        '14': 'Hacking/Dark-Web.py',
        '15': 'Hacking/Close-DM.py',    
        '16': 'Hacking/Email-Info.py',   
        '17': 'Hacking/Token-Checker.py', 
        '18': 'Hacking/Token-Info.py',
        '19': 'Hacking/Token-Grabber.py',
        '20': 'Hacking/Builder-Keylloger.py',
        '21': 'Hacking/Tools-Info.py',
        '22': 'Hacking/Ip-Website.py',
        '23': 'https://discord.gg/SuZm6RrDWY',
        '24': 'Hacking/Password-dehash.py'
    }

    while True:
        print_logo()
        print_menu()
        choice = input(red + "\n--> " + reset).strip()

        if choice.lower() in ('exit', 'quit', 'q'):
            confirm = input("Voulez-vous vraiment quitter ? (o/n) : ").strip().lower()
            if confirm == 'o':
                print("Fermeture du programme...")
                time.sleep(1)
                break
            else:
                continue

        if choice in script_paths:
            target = script_paths[choice]
            if target.startswith("http"):
                print(f"{blue}Ouverture du lien dans le navigateur...{reset}")
                webbrowser.open(target)
                time.sleep(1)
            else:
                run_script(target)
        else:
            print(red + "Option invalide !" + reset)
            time.sleep(1)

if __name__ == "__main__":
    main()
