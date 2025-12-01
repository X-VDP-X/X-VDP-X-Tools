import socket

def get_ip(site):
    try:
        ip = socket.gethostbyname(site)
        return ip
    except socket.gaierror:
        return None

def main():
    while True:
        site = input("Entrez le nom du site web (ex: google.com) : ").strip()
        ip = get_ip(site)
        if ip:
            print(f"L'adresse IP de {site} est : {ip}")
        else:
            print(f"Impossible de résoudre l'adresse IP de {site}")

        choix = input("Veux-tu refaire une recherche ? (o/n) : ").strip().lower()
        if choix != 'o':
            print("Au revoir !")
            break

if __name__ == "__main__":
    main()
