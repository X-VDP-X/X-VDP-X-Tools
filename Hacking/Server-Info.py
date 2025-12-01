import os
import colorama
import requests

colorama.init()

titre = "Serveur Info"
os.system(f"title {titre}")

red = colorama.Fore.RED
white = colorama.Fore.WHITE
reset = colorama.Fore.RESET

INPUT = f'{red}[{white}>{red}] |'

def get_invite_info(invite):
    try:
        invite_code = invite.split("/")[-1]
    except Exception:
        invite_code = invite

    url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"{red}[x] Erreur : invitation invalide ou inaccessible.{reset}")
            return None

        return response.json()
    except Exception as e:
        print(f"{red}[x] Une erreur est survenue : {e}{reset}")
        return None

def print_info(data, invite):
    guild = data.get('guild', {})
    inviter = data.get('inviter', {})

    print(f"""{red}
Invitation Information:
{white}[{red}+{white}]{red} Invitation        : {white}{invite}{red}
{white}[{red}+{white}]{red} Code              : {white}{data.get('code')}{red}
{white}[{red}+{white}]{red} Expired           : {white}{data.get('expires_at')}{red}

Server Information:
{white}[{red}+{white}]{red} Server ID         : {white}{guild.get('id')}{red}
{white}[{red}+{white}]{red} Server Name       : {white}{guild.get('name')}{red}
{white}[{red}+{white}]{red} Server Icon       : {white}{guild.get('icon')}{red}
{white}[{red}+{white}]{red} Server Features   : {white}{guild.get('features')}{red}
{white}[{red}+{white}]{red} Verification Level: {white}{guild.get('verification_level')}{red}
{white}[{red}+{white}]{red} NSFW Level        : {white}{guild.get('nsfw_level')}{red}
{white}[{red}+{white}]{red} NSFW              : {white}{guild.get('nsfw')}{red}
{white}[{red}+{white}]{red} Premium Subs      : {white}{guild.get('premium_subscription_count')}{red}

Inviter Information:
{white}[{red}+{white}]{red} ID                : {white}{inviter.get('id')}{red}
{white}[{red}+{white}]{red} Username          : {white}{inviter.get('username')}{red}
{white}[{red}+{white}]{red} Global Name       : {white}{inviter.get('global_name')}{red}
{white}[{red}+{white}]{red} Avatar            : {white}{inviter.get('avatar')}{red}
{white}[{red}+{white}]{red} Discriminator     : {white}{inviter.get('discriminator')}{red}
{white}[{red}+{white}]{red} Public Flags      : {white}{inviter.get('public_flags')}{red}
{white}[{red}+{white}]{red} Banner            : {white}{inviter.get('banner')}{red}
{white}[{red}+{white}]{red} Accent Color      : {white}{inviter.get('accent_color')}{red}
{white}[{red}+{white}]{red} Banner Color      : {white}{inviter.get('banner_color')}{reset}
""")

def main():
    while True:
        invite = input(f"\n{INPUT} Server Invitation -> {reset}").strip()
        data = get_invite_info(invite)
        if data:
            print_info(data, invite)

        choice = input(f"{red}\nVoulez-vous refaire une recherche ? (o/n) -> {reset}").strip().lower()
        if choice != 'o':
            print(f"{red}Au revoir !{reset}")
            break

if __name__ == "__main__":
    main()
