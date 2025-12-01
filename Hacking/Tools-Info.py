from colorama import Fore

cyan = Fore.CYAN

def Tools(serv, version, serv_invite, date, name, Telegram):
    print(f'{cyan}X-VDP-X : ')
    print(f'Tools Crée Par : {name}')
    print(f'Création Le : {date}')
    print(f'X-VDP-X Version: {version}')
    print(f'Server : {serv_invite}')
    print(f'Contact Discord : {name}')
    print(f'Nom Tu Server : {serv}')
    print(f'Telegram : {Telegram}')

Tools('X-VDP-X', '1.5', 'https://discord.gg/vdp', '2024-07-30', 'guetteur93', 'https://t.me/xvdpx')

input("\nAppuyez sur Entrée pour quitter...")
