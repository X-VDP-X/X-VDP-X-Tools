import asyncio
import aiohttp

subdomains_file = "Hacking/subdomains.txt"

async def check_subdomain(session, subdomain, domain):
    url = f"http://{subdomain}.{domain}"
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                print(f"[+] Subdomain found: {url}")
                return url
    except:
        pass
    return None

async def scan_domain(domain):
    with open(subdomains_file, "r") as f:
        subdomains = [line.strip() for line in f if line.strip()]

    async with aiohttp.ClientSession() as session:
        tasks = [check_subdomain(session, sub, domain) for sub in subdomains]
        results = await asyncio.gather(*tasks)

    found = [r for r in results if r]
    if found:
        print("\nSubdomains found:")
        for sub in found:
            print(sub)
    else:
        print("Aucun sous-domaine trouvé.")

def main():
    while True:
        domain = input("\nEnter the domain (ex: example.com): ").strip()
        asyncio.run(scan_domain(domain))

        while True:
            retry = input("Voulez-vous refaire un scan ? (o/n) : ").strip().lower()
            if retry == 'o':
                break  
            elif retry == 'n':
                print("Fin du programme. Bye !")
                return  
            else:
                print("Réponse invalide, veuillez taper 'o' pour oui ou 'n' pour non.")

if __name__ == "__main__":
    main()
