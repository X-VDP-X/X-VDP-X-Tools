import discord
import asyncio
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

guild_id_global = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

@client.event
async def on_ready():
    clear()
    print(f"[✓] Connecté en tant que : {client.user}")
    await main_menu()

async def dm_user():
    try:
        user_id = int(input("ID de l'utilisateur à DM : "))
        count = int(input("Combien de messages envoyer ? "))
        message = input("Message : ")
    except ValueError:
        print("Entrée invalide.")
        return

    try:
        user = await client.fetch_user(user_id)
        for i in range(count):
            await user.send(message)
            print(f"[{i+1}/{count}] DM envoyé à {user.name}")
            await asyncio.sleep(0.4) 
    except Exception as e:
        print(f"Erreur : {e}")

async def dm_all():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable.")
        return

    message = input("Message à envoyer à tous les membres : ")

    sent = 0
    for member in guild.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            sent += 1
            print(f"[{sent}] DM envoyé à {member.name}")
            await asyncio.sleep(0.4)
        except:
            continue

async def main_menu():
    while True:
        print("""
╔═══════════════════════╗
║     MENU DM-BOT       ║
╠═══════════════════════╣
║ [1] DM un utilisateur ║
║ [2] DM tout le serveur║
║ [3] Quitter           ║
╚═══════════════════════╝
""")
        choice = input("Choix > ").strip()
        if choice == "1":
            await dm_user()
        elif choice == "2":
            await dm_all()
        elif choice == "3":
            await client.close()
            break
        else:
            print("Choix invalide.")
        await asyncio.sleep(1)
        clear()

if __name__ == "__main__":
    clear()
    token = input("Token du bot : ").strip()
    try:
        guild_id_global = int(input("ID du serveur : ").strip())
        client.run(token)
    except ValueError:
        print("ID de serveur invalide.")
