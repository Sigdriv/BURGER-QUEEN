import sqlite3 as sql
import os
from colorama import Fore

current_user = None
error = None
info = None

def logInnInterface():
    global error
    
    clear_terminal()
    print("1. Logg inn")
    print("2. Opprett bruker")
    print("3. Tilbake")
    choice = input("Velg en handling: ")
    
    if choice == "1": 
        if logInn():
            clear_terminal()
            pass
        else:
            logInnInterface()

    elif choice == "2":
        if signUp():
            clear_terminal()
            pass
        else:
            signUp()
    
    elif choice == "3":
        return False
    
    else:
        error = "Ugyldig valg. Prøv igjen."
        logInnInterface()
    
def logInn():
    global current_user
    global error
    clear_terminal()
    
    print("1. Logg inn")
    print("Please enter your username and password")
    print()
    username = input("Username: ")
    password = input("Password: ")

    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password))
    if c.fetchone() is not None:
        current_user = username
        return True
    else:
        error = "Ugyldig brukernavn eller passord \nVenligst prøv igjen"
        return False

def signUp():
    global current_user
    global error
    global info
    clear_terminal()
    
    print("2. Opprett bruker")
    print()
    print("Skriv inn ønsket brukernavn og passord")
    username = input("Brukernavn: ")
    password = input("Passord: ")
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password))
    if c.fetchone() is not None:
        error = "Brukernavnet eksisterer allerede \nVennligst velg et annet"
        logInnInterface()
    else:
        c.execute("INSERT INTO User VALUES (?, ?, 0)", (username, password))
        conn.commit()
        conn.close()
        info = username + " er nå registrert og er logget inn"
        current_user = username
        return True
    

def clear_terminal():
    global current_user
    global error
    global info
    if current_user is not None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print("Logget inn som " + current_user)
    else:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print("Ikke logget inn")
    print("Velkommen til Burger Queen")
    
    if error is not None:
        print(f'{Fore.RED}En feil oppsto: {error} {Fore.WHITE}')
        error = None
    if info is not None:
        print(f'{Fore.GREEN}{info} {Fore.WHITE}')
        info = None

def connect_database():
    return sql.connect("BurgerQueen.db")

# Hovedfunksjon
def main():
    global current_user
    global error
    
    clear_terminal()

    while True:
        if current_user is None:
            print("1. Logg inn")
            # print("2. Registrer ordre")
            print("2. Avslutt")

            choice = input("Velg en handling: ")

            if choice == "1":
                
                logInnInterface()

            # elif choice == "2":
            #     pass

            elif choice == "2":
                print("Avslutter programmet.")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()
        
        else:
            print("1. Logg ut")
            print("2. Registrer ordre")
            print("3. Avslutt")

            choice = input("Velg en handling: ")

            if choice == "1":
                current_user = None
                clear_terminal()

            elif choice == "2":
                pass

            elif choice == "3":
                print("Avslutter programmet.")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()

if __name__ == "__main__":
    main()