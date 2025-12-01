import platform
import subprocess

def clean_host(host):
    if host.startswith("http://"):
        host = host[7:]
    elif host.startswith("https://"):
        host = host[8:]

    host = host.strip("/")
    return host

def ping(host):
    host = clean_host(host)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if output.returncode == 0:
            print(f"[+] {host} est joignable")
        else:
            print(f"[-] {host} n'est pas joignable")
    except Exception as e:
        print(f"[!] Erreur lors du ping: {e}")

def main():
    while True:
        cible = input("Entrez une IP ou un domaine à ping (ou 'exit' pour quitter) : ").strip()
        if cible.lower() == 'exit':
            break
        ping(cible)

if __name__ == "__main__":
    main()
