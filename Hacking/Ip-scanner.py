import asyncio
import socket
import json
import csv
import subprocess
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn

console = Console()

def ping_host(ip, timeout=1):
    try:
        param = '-n' if subprocess.os.name == 'nt' else '-c'
        cmd = ['ping', param, '1', ip]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

async def async_scan_port(ip: str, port: int, timeout=1):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout)
        try:
            writer.write(b"\r\n")
            await writer.drain()
            banner = await asyncio.wait_for(reader.read(1024), timeout=1)
            banner = banner.decode(errors='ignore').strip()
        except Exception:
            banner = ""
        writer.close()
        await writer.wait_closed()
        return True, banner
    except:
        return False, ""

async def scan_ports(ip, ports, ping_before_scan, timeout, max_concurrency):
    results = []
    is_alive = True

    if ping_before_scan:
        console.print(f"[yellow]Ping de {ip} avant scan...[/yellow]")
        is_alive = ping_host(ip, timeout)
        if not is_alive:
            console.print(f"[red]{ip} ne répond pas au ping.[/red]")

    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "•",
        TimeElapsedColumn(),
        console=console,
    )
    task = progress.add_task(f"[cyan]Scan des ports sur {ip}...", total=len(ports))

    sem = asyncio.Semaphore(max_concurrency)

    async def limited_scan(port):
        async with sem:
            open_, banner = await async_scan_port(ip, port, timeout)
            progress.update(task, advance=1)
            return port, open_, banner

    progress.start()
    try:
        tasks = [limited_scan(port) for port in ports]
        for future in asyncio.as_completed(tasks):
            port, open_, banner = await future
            if open_:
                results.append({"ip": ip, "port": port, "banner": banner})
    finally:
        progress.stop()

    return results

def save_results(results, ip, ports, timeout, max_concurrency, ping_before_scan, duration):
    if not results:
        console.print("[red]Aucun port ouvert détecté.[/red]")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = {
        "scan_started": timestamp,
        "scan_duration_s": duration,
        "ip": ip,
        "ports": ports,
        "timeout": timeout,
        "max_concurrency": max_concurrency,
        "ping_before_scan": ping_before_scan
    }

    json_file = f"scan_results_{timestamp}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "results": results}, f, indent=2, ensure_ascii=False)
    console.print(f"[green]Résultats JSON sauvegardés dans {json_file}[/green]")

    csv_file = f"scan_results_{timestamp}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ip", "port", "banner"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    console.print(f"[green]Résultats CSV sauvegardés dans {csv_file}[/green]")

async def ask_input(prompt, validate_func=None, error_msg="Entrée invalide."):
    while True:
        value = input(prompt).strip()
        if validate_func is None or validate_func(value):
            return value
        console.print(f"[red]{error_msg}[/red]")

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def validate_ports(ports_str):
    try:
        ports = [int(p) for p in ports_str.split(",") if p.strip().isdigit()]
        return len(ports) > 0
    except:
        return False

def validate_timeout(t):
    try:
        return float(t) > 0
    except:
        return False

def validate_max_concurrency(c):
    try:
        return int(c) > 0
    except:
        return False

async def main():
    console.print("[bold cyan]=== IP Scanner avancé (mode interactif) ===[/bold cyan]")

    while True:
        ip = await ask_input("IP à scanner (ex: 192.168.1.1) : ", validate_ip, "IP invalide.")
        ports_input = await ask_input("Ports à scanner (ex: 22,80,443) : ", validate_ports, "Liste de ports invalide.")
        timeout = await ask_input("Timeout socket en secondes (ex: 1) : ", validate_timeout, "Timeout invalide.")
        max_concurrency = await ask_input("Nombre max de connexions simultanées (ex: 500) : ", validate_max_concurrency, "Nombre invalide.")
        ping_input = await ask_input("Ping avant scan TCP pour filtrer IP mortes ? (o/n) : ", lambda x: x.lower() in ["o","n"], "Répondre par o ou n.")
        ping_before_scan = ping_input.lower() == "o"

        ports = sorted(set(int(p) for p in ports_input.split(",") if p.strip().isdigit()))
        timeout = float(timeout)
        max_concurrency = int(max_concurrency)

        console.print(f"\n[bold cyan]Scan de {ip} sur ports {ports}[/bold cyan]")

        start = datetime.now()
        results = await scan_ports(ip, ports, ping_before_scan, timeout, max_concurrency)
        duration = (datetime.now() - start).total_seconds()

        save_results(results, ip, ports, timeout, max_concurrency, ping_before_scan, duration)

        cont = await ask_input("\nVoulez-vous lancer un autre scan ? (o/n) : ", lambda x: x.lower() in ["o","n"], "Répondre par o ou n.")
        if cont.lower() != "o":
            console.print("[green]Fin du programme.[/green]")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red]Scan interrompu par utilisateur[/red]")
