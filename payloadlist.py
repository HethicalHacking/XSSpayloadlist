import requests
from termcolor import colored
import os

def get_xss_payloads():
    url = "https://raw.githubusercontent.com/HethicalHacking/XSSpayloadlist/main/listXSS.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        payloads = response.text.splitlines()
        return payloads
    except requests.RequestException as e:
        print(colored(f"Errore nel recupero della lista: {e}", "red"))
        return []

def display_menu():
    print(colored("=== Menu XSS Payload ===", "cyan"))
    print(colored("1. Visualizza tutti i payload", "yellow"))
    print(colored("2. Visualizza un payload specifico", "yellow"))
    print(colored("3. Esci", "yellow"))
    choice = input(colored("Inserisci la tua scelta (1-3): ", "green"))
    return choice

def save_payloads(payloads):
    save_choice = input(colored("Vuoi salvare la lista in un file? (s/n): ", "green")).lower()
    if save_choice == 's':
        filename = input(colored("Inserisci il nome del file (es. payloads.txt): ", "green"))
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for payload in payloads:
                    f.write(payload + '\n')
            print(colored(f"Lista salvata con successo in {filename}", "cyan"))
        except Exception as e:
            print(colored(f"Errore nel salvataggio del file: {e}", "red"))

def main():
    payloads = get_xss_payloads()
    if not payloads:
        print(colored("Nessun payload trovato. Uscita.", "red"))
        return

    while True:
        choice = display_menu()

        if choice == '1':
            print(colored("Lista dei payload XSS:", "cyan"))
            for i, payload in enumerate(payloads, 1):
                print(colored(f"{i}. {payload}", "yellow"))
            save_payloads(payloads)

        elif choice == '2':
            try:
                index = int(input(colored(f"Inserisci il numero del payload (1-{len(payloads)}): ", "green")))
                if 1 <= index <= len(payloads):
                    print(colored(f"{index}. {payloads[index-1]}", "yellow"))
                else:
                    print(colored(f"Numero non valido. Deve essere tra 1 e {len(payloads)}.", "red"))
            except ValueError:
                print(colored("Inserisci un numero valido.", "red"))
            save_payloads(payloads)

        elif choice == '3':
            print(colored("Uscita dal programma.", "cyan"))
            break

        else:
            print(colored("Scelta non valida. Riprova.", "red"))

if __name__ == "__main__":
    main()
