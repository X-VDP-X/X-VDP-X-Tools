import os
import time

RESET = "\033[0m"
WHITE = "\033[37m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

class TitleCommand:
    def __init__(self, title):
        self.title = title

    def set_title(self):
        os.system(f"title {self.title}")

class SlowPrinter:
    def __init__(self, text, delay=0.001):
        self.text = text
        self.delay = delay

    def print(self):
        for char in self.text:
            print(char, end='', flush=True)
            time.sleep(self.delay)
        print()

class DarkWebMenu:
    def __init__(self):
        self.menu = {
            "Wiki Dark Web": [
                {"name": "Torch", "url": "https://thehiddenwiki.com/"},
            ],
            "Search Engine": [
                {"name": "Torch", "url": "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"},
                {"name": "Danex", "url": "http://danexio627wiswvlpt6ejyhpxl5gla5nt2tgvgm2apj2ofrgm44vbeyd.onion"},
                {"name": "Sentor", "url": "http://e27slbec2ykiyo26gfuovaehuzsydffbit5nlxid53kigw3pvz6uosqd.onion"},
            ],
            "Bitcoin Anonymity": [
                {"name": "Dark Mixer", "url": "http://y22arit74fqnnc2pbieq3wqqvkfub6gnlegx3cl6thclos4f7ya7rvad.onion"},
                {"name": "Mixabit", "url": "http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion"},
                {"name": "EasyCoin", "url": "http://mp3fpv6xbrwka4skqliiifoizghfbjy5uyu77wwnfruwub5s4hly2oid.onion"},
                {"name": "Onionwallet", "url": "http://p2qzxkca42e3wccvqgby7jrcbzlf6g7pnkvybnau4szl5ykdydzmvbid.onion"},
                {"name": "VirginBitcoin", "url": "http://ovai7wvp4yj6jl3wbzihypbq657vpape7lggrlah4pl34utwjrpetwid.onion"},
            ],
            "Stresser / Ddos": [
                {"name": "Stresser", "url": "http://ecwvi3cd6h27r2kjx6ur6gdi4udrh66omvqeawp3dzqrtfwo432s7myd.onion"},
            ],
            "Market": [
                {"name": "Deep Market", "url": "http://deepmar4ai3iff7akeuos3u3727lvuutm4l5takh3dmo3pziznl5ywqd.onion"},
                {"name": "DrChronic", "url": "http://iwggpyxn6qv3b2twpwtyhi2sfvgnby2albbcotcysd5f7obrlwbdbkyd.onion"},
                {"name": "TomAndJerry", "url": "http://rfyb5tlhiqtiavwhikdlvb3fumxgqwtg2naanxtiqibidqlox5vispqd.onion"},
                {"name": "420prime", "url": "http://ajlu6mrc7lwulwakojrgvvtarotvkvxqosb4psxljgobjhureve4kdqd.onion"},
                {"name": "Can*abisUK", "url": "http://7mejofwihleuugda5kfnr7tupvfbaqntjqnfxc4hwmozlcmj2cey3hqd.onion"},
                {"name": "DeDope", "url": "http://sga5n7zx6qjty7uwvkxpwstyoh73shst6mx3okouv53uks7ks47msayd.onion"},
                {"name": "AccMarket", "url": "http://55niksbd22qqaedkw36qw4cpofmbxdtbwonxam7ov2ga62zqbhgty3yd.onion"},
                {"name": "Cardshop", "url": "http://s57divisqlcjtsyutxjz2ww77vlbwpxgodtijcsrgsuts4js5hnxkhqd.onion"},
                {"name": "Darkmining", "url": "http://jbtb75gqlr57qurikzy2bxxjftzkmanynesmoxbzzcp7qf5t46u7ekqd.onion"},
                {"name": "MobileStore", "url": "http://rxmyl3izgquew65nicavsk6loyyblztng6puq42firpvbe32sefvnbad.onion"},
                {"name": "EuroGuns", "url": "http://t43fsf65omvf7grt46wlt2eo5jbj3hafyvbdb7jtr2biyre5v24pebad.onion"},
                {"name": "UKpassports", "url": "http://3bp7szl6ehbrnitmbyxzvcm3ieu7ba2kys64oecf4g2b65mcgbafzgqd.onion"},
                {"name": "ccPal", "url": "http://xykxv6fmblogxgmzjm5wt6akdhm4wewiarjzcngev4tupgjlyugmc7qd.onion"},
                {"name": "Webuybitcoins", "url": "http://wk3mtlvp2ej64nuytqm3mjrm6gpulix623abum6ewp64444oreysz7qd.onion"},
                {"name": "Shop", "url": "http://darknetlidvrsli6iso7my54rjayjursyw637aypb6qambkoepmyq2yd.onion/"},
            ],
            "DataBase": [
                {"name": "Database", "url": "http://breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd.onion"},
            ],
            "Reseaux Social": [
                {"name": "Facebook", "url": "https://www.facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion/"},
                {"name": "Reddit", "url": "https://www.reddittorjg6rue252oqsxryoxengawnmo46qy4kyii5wtqnwfj4ooad.onion/?rdt=41078"},
            ],
            "Horreur": [
                {"name": "bestgore", "url": "https://bestgore.fun/videos/trending"},
                {"name": "kaotic", "url": "https://www.kaotic.com/"},
                {"name": "krudplug", "url": "https://www.krudplug.net/m/index.php"},
                {"name": "crazyshit", "url": "https://crazyshit.com/"},
                {"name": "livegore", "url": "https://www.livegore.com/"},
                {"name": "vidmax", "url": "https://vidmax.com/"},
                {"name": "pr0gramm", "url": "https://pr0gramm.com/"},
                {"name": "itemfix", "url": "https://www.itemfix.com/"},
                {"name": "goregrish", "url": "https://goregrish.com/"},
                {"name": "runthegauntlet", "url": "https://runthegauntlet.org"},
            ],
        }

    def format_menu(self):
        border_len = 97
        border = "━" * border_len
        lines = [f"{WHITE}┏{border}┓"]
        for cat, entries in self.menu.items():
            lines.append(f"{WHITE}┃ {YELLOW}{cat.ljust(border_len - 2)}{WHITE}┃")
            for e in entries:
                name = e['name'].ljust(25)
                url = e['url'].ljust(border_len - 28)
                lines.append(f"{WHITE}┃ {RED}{name}{WHITE}: {CYAN}{url}{WHITE}┃")
        lines.append(f"{WHITE}┗{border}┛")
        return "\n".join(lines)

    def print_menu(self):
        SlowPrinter(self.format_menu(), delay=0.001).print()

def main():
    TitleCommand("Dark Web Menu").set_title()
    DarkWebMenu().print_menu()
    input("\nAppuie sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
