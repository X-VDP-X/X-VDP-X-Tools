import hashlib
import os

HASH_TYPES = {
    'md5': 32,
    'sha1': 40,
    'sha224': 56,
    'sha256': 64,
    'sha384': 96,
    'sha512': 128,
}

def detect_hash_type(hash_str):
    length = len(hash_str)
    for hash_name, hash_len in HASH_TYPES.items():
        if length == hash_len:
            return hash_name
    return None

def hash_word(word, hash_type):
    h = hashlib.new(hash_type)
    h.update(word.encode('utf-8'))
    return h.hexdigest()

def crack_hash(hash_to_crack, wordlist_path, hash_type):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if hash_word(word, hash_type) == hash_to_crack:
                    return word
    except FileNotFoundError:
        print(f"[!] Fichier wordlist introuvable : {wordlist_path}")
    return None

def valid_hash(hash_str):
    allowed_chars = "0123456789abcdef"
    return all(c in allowed_chars for c in hash_str.lower())

def main():
    while True:
        print("\n[ Menu Dehash Multi-Hash ]")
        print("1) Utiliser la wordlist intégrée (wordlist.txt)")
        print("2) Indiquer un chemin vers une autre wordlist")
        choice = input("Votre choix (1 ou 2) : ").strip()

        if choice == "1":
            wordlist_path = "Hacking/wordlist.txt"
        elif choice == "2":
            wordlist_path = input("Chemin vers la wordlist : ").strip()
        else:
            print("[!] Choix invalide.")
            continue

        if not os.path.isfile(wordlist_path):
            print(f"[!] Fichier introuvable : {wordlist_path}")
            continue

        hash_to_crack = input("Hash à déhasher : ").strip().lower()

        if not valid_hash(hash_to_crack):
            print("[!] Le hash fourni contient des caractères invalides (doit être hexadécimal).")
            continue

        detected_hash_type = detect_hash_type(hash_to_crack)

        if detected_hash_type is None:
            print("[!] Impossible de détecter automatiquement le type de hash.")
            print("Hash supportés : md5, sha1, sha224, sha256, sha384, sha512")
            detected_hash_type = input("Merci d'indiquer le type de hash manuellement : ").strip().lower()
            if detected_hash_type not in HASH_TYPES:
                print("[!] Type de hash non supporté.")
                continue
        else:
            print(f"[i] Type de hash détecté automatiquement : {detected_hash_type}")

        print(f"\n[•] Lancement du cracking sur {hash_to_crack} avec la wordlist : {wordlist_path} en utilisant {detected_hash_type}...\n")
        result = crack_hash(hash_to_crack, wordlist_path, detected_hash_type)

        if result:
            print(f"\n[✔] Mot de passe trouvé : {result}")
        else:
            print("\n[✘] Mot de passe non trouvé dans la wordlist.")

        retry = input("\nSouhaitez-vous déhasher un autre hash ? (o/n) : ").strip().lower()
        if retry != 'o':
            break

if __name__ == "__main__":
    main()
