import random
import string

first_names = [
    "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace",
    "Hugo", "Ivy", "Jack", "Laura", "Mike", "Nina", "Oscar", "Paul"
]

last_names = [
    "Dupont", "Moreau", "Lemoine", "Rousseau", "Martin", "Bernard",
    "Petit", "Durand", "Leroy", "Faure", "Girard", "Michel", "Blanc"
]

email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]

def fake_discord_token():
    first_char = random.choice(['M', 'O'])
    part1 = first_char + ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=23))
    part2 = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=6))
    part3 = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=27))
    return f"{part1}.{part2}.{part3}"

def fake_email():
    first = random.choice(first_names).lower()
    last = random.choice(last_names).lower()
    separator = random.choice([".", "_", ""])
    number = str(random.randint(1, 99)) if random.random() < 0.5 else ""
    domain = random.choice(email_domains)
    return f"{first}{separator}{last}{number}@{domain}"

def fake_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))

def fake_job():
    jobs = [
        "Développeur", "Ingénieur", "Artiste", "Médecin", "Professeur",
        "Chef de projet", "Designer", "Consultant", "Écrivain", "Musicien"
    ]
    return random.choice(jobs)

def fake_credit_card():
    number = "4" + ''.join(random.choices(string.digits, k=15))
    exp_month = random.randint(1, 12)
    exp_year = random.randint(24, 30)
    cvc = ''.join(random.choices(string.digits, k=3))
    return f"{number} | Exp: {exp_month:02d}/{exp_year} | CVC: {cvc}"

def fake_phone():
    return "+33 " + ' '.join(''.join(random.choices(string.digits, k=2)) for _ in range(5))

def generate_fake_info():
    return {
        "Discord Token": fake_discord_token(),
        "Email": fake_email(),
        "Password": fake_password(),
        "Job": fake_job(),
        "Credit Card": fake_credit_card(),
        "Phone": fake_phone(),
    }

def main():
    while True:
        for i in range(10):
            info = generate_fake_info()
            print(f"--- Fake Info #{i+1} ---")
            for key, value in info.items():
                print(f"{key}: {value}")
            print()
        choice = input("Générer à nouveau ? (o/n) : ").strip().lower()
        if choice != 'o':
            print("Bye !")
            break

if __name__ == "__main__":
    main()
