import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_target(target):
    target = target.strip().lower()
    if target.startswith("http://"):
        target = target[7:]
    elif target.startswith("https://"):
        target = target[8:]
    target = target.rstrip('/')
    return target

def scan_port(target, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except Exception:
        return None

def main():
    raw_target = input("Entrez l'IP ou le domaine à scanner : ")
    target = clean_target(raw_target)

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Impossible de résoudre le domaine : {target}")
        return

    print(f"Scan des ports de {ip} ({target})...\n")

    try:
        start_port = int(input("Port de début : ").strip())
        end_port = int(input("Port de fin : ").strip())
    except ValueError:
        print("Ports invalides. Veuillez entrer des nombres entiers.")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Plage de ports invalide. Doit être entre 1 et 65535, et début <= fin.")
        return

    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in as_completed(futures):
            port = future.result()
            if port:
                print(f"[+] Port {port} ouvert")
                open_ports.append(port)

    if open_ports:
        print(f"\nPorts ouverts détectés : {sorted(open_ports)}")
    else:
        print("\nAucun port ouvert détecté.")

if __name__ == "__main__":
    main()
