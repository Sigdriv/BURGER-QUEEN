import sqlite3 as sql
import os
import asyncio

current_user = None

def logInnInterface():
    
    clear_terminal()
    print("1. Logg inn")
    print("2. Opprett bruker")
    print("3. Tilbake")
    choice = input("Velg en handling: ")
    
    if choice == "1": 
        if logInn():
            pass
        else:
            logInnInterface()

    elif choice == "2":
        if signUp():
            pass
        else:
            signUp()
    
    elif choice == "3":
        return False
    
    else:
        print("Ugyldig valg. Prøv igjen.")
        return False
    
def logInn():
    global current_user
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
        print("Welcome " + username)
        current_user = username
        return True
    else:
        print("Ugyldig brukernavn eller passord")
        print("Venligst prøv igjen")
        return False

async def signUp():
    global current_user
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
        print("Brukernavn eksisterer allerede, vennligst velg et annet")
        await asyncio.sleep(5)
        return False
    else:
        c.execute("INSERT INTO User VALUES (?, ?, 0)", (username, password))
        conn.commit()
        conn.close()
        print(username + " er nå registrert og er logget inn")
        current_user = username
        return True
    

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def connect_database():
    return sql.connect("BurgerQueen.db")

# Hovedfunksjon
def main():
    
    clear_terminal()
    print("Velkommen til Burger Queen")

    while True:
        print("1. Logg inn")
        print("2. Registrer ordre")
        print("3. Avslutt")

        choice = input("Velg en handling: ")

        if choice == "1":
            
            logInnInterface()

        elif choice == "2":
            pass

        elif choice == "3":
            print("Avslutter programmet.")
            break

        else:
            print("Ugyldig valg. Prøv igjen.")

if __name__ == "__main__":
    main()