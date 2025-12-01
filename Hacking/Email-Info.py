import os
import colorama
import dns.resolver
import requests
import re

titre = "Email info"

os.system(f"title {titre}")

colorama.init()


color = colorama.Fore
red = color.RED
white = color.WHITE
reset = color.RESET

INFO = f'{red}[{white}!{red}] |'
INPUT = f'{red}[{white}>{red}] |'
WAIT = f'{color.GREEN}[{color.WHITE}~{color.GREEN}] |'


def Continue():
    input(color.RED + f"{INFO} Press Enter to continue -> " + color.RESET)


def email_info(email):
    info = {}
    domain_all = domain = None

    try:
        domain_all = email.split('@')[-1]
        domain = re.search(r"@([^@.]+)\.", email).group(1)
    except Exception as e:
        print(f"{WAIT} Error extracting domain information: {e}")

    try:
        mx_records = dns.resolver.resolve(domain_all, 'MX')
        info["mx_servers"] = [str(record.exchange) for record in mx_records]
    except Exception as e:
        print(f"{WAIT} Error retrieving MX records: {e}")
        info["mx_servers"] = None

    try:
        spf_records = dns.resolver.resolve(domain_all, 'SPF')
        info["spf_records"] = [str(record) for record in spf_records]
    except Exception as e:
        print(f"{WAIT} Error retrieving SPF records: {e}")
        info["spf_records"] = None

    try:
        dmarc_records = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
        info["dmarc_records"] = [str(record) for record in dmarc_records]
    except Exception as e:
        print(f"{WAIT} Error retrieving DMARC records: {e}")
        info["dmarc_records"] = None

    try:
        response = requests.get(
            f"https://api.mailgun.net/v4/address/validate?address={email}",
            auth=("api", "YOUR_MAILGUN_API_KEY")
        )
        data = response.json()
        info["mailgun_validation"] = data
    except Exception as e:
        print(f"{WAIT} Error validating with Mailgun: {e}")
        info["mailgun_validation"] = None

   
    if info.get("mx_servers"):
        for server in info["mx_servers"]:
            if "google.com" in server:
                info["google_workspace"] = True
            elif "outlook.com" in server:
                info["microsoft_365"] = True

    return info, domain_all, domain


email = input(f"\n{INPUT} Enter Email -> {reset}")
print(f"{red}{WAIT} Retrieving Information...{reset}")


info, domain_all, domain = email_info(email)


print(f"""
{white}[{red}+{white}]{red} Email          : {white}{email}
{white}[{red}+{white}]{red} Domain         : {white}{domain}
{white}[{red}+{white}]{red} Domain (Full)  : {white}{domain_all}
{white}[{red}+{white}]{red} MX Servers     : {white}{info.get("mx_servers")}
{white}[{red}+{white}]{red} SPF Records    : {white}{info.get("spf_records")}
{white}[{red}+{white}]{red} DMARC Records  : {white}{info.get("dmarc_records")}
{white}[{red}+{white}]{red} Google Workspace: {white}{info.get("google_workspace")}
{white}[{red}+{white}]{red} Microsoft 365  : {white}{info.get("microsoft_365")}
{white}[{red}+{white}]{red} Mailgun Data   : {white}{info.get("mailgun_validation")}
{reset}
""")


Continue()
