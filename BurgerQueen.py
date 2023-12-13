import sqlite3 as sql
import os
from colorama import Fore

current_user = None
error = None
info = None

def logInnInterface():
    global error
    
    clear_terminal()
    print()
    
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
            pass
        else:
            signUp()
    
    elif choice == "3":
        clear_terminal()
        return False
    
    else:
        error = "Ugyldig valg. Prøv igjen."
        logInnInterface()
    
def logInn():
    global current_user
    global error
    clear_terminal()
    print()
    
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
    print()
    
    print("2. Opprett bruker")
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

def get_burger_names():
    conn = connect_database()
    c = conn.cursor()

    c.execute("SELECT NameID FROM Burgers")
    burger_names = [row[0] for row in c.fetchall()]

    conn.close()
    return burger_names

def orderInterface():
    global error
    
    clear_terminal()
    print("2. Ordre")
    print()
    print("1. Vis ordre")
    print("2. Registrer ordre")
    print("3. Tilbake")
    choice = input("Velg en handling: ")
    
    if choice == "1":
        display_user_orders()
    elif choice == "2":
        place_order()
    elif choice == "3":
        main()
    else:
        error = "Ugyldig valg. Prøv igjen."
        orderInterface()


def place_order():
    global current_user
    global error
    global info
    clear_terminal()
    print("2. Registrer ordre")
    print()
    
    burger_names = get_burger_names()
    
    print("Available Burgers:")
    for i, burger_name in enumerate(burger_names, start=1):
        print(f"{i}. {burger_name}")
    print()
        
    burger_name = input("Enter burger name: ")
    
    if burger_name not in burger_names:
        error = "Burgeren finnes ikke. Prøv igjen."
        place_order()
    
    print("Ordre lastes opp...")
    print("Vent litt")

    conn = connect_database()
    c = conn.cursor()

    c.execute("INSERT INTO Orders (Who, What, Produced) VALUES (?, ?, 0)",
              (current_user, burger_name))
    
    conn.commit()
    conn.close()

    info = f"Order placed successfully for {burger_name}!"
    main()
    
def display_user_orders():
    global current_user
    global error
    clear_terminal()
    print("1. Vis ordre")
    print()

    conn = connect_database()
    c = conn.cursor()

    c.execute("SELECT * FROM Orders WHERE Who = ?", (current_user,))
    orders = c.fetchall()

    if not orders:
        error = "No orders found for the current user."
    else:
        print("Dine Bestillinger:")
        for order in orders:
            print(f"BestillingsID: {order[0]}, Burger: {order[2]}, Produsert: {'Ja' if order[3] else 'Nei'}")
    
        print()
        input("Press enter for å fortsette... ")
    

    conn.close()


# Hovedfunksjon
def main():
    global current_user
    global error
    

    while True:
        clear_terminal()
        print()
        if current_user is None:
            print("1. Logg inn/opprett bruker")
            print("2. Avslutt")

            choice = input("Velg en handling: ")

            if choice == "1":
                
                logInnInterface()

            elif choice == "2":
                print("Avslutter programmet.")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()
        
        else:
            print("1. Logg ut")
            print("2. Ordre")
            print("3. Avslutt")

            choice = input("Velg en handling: ")

            if choice == "1":
                current_user = None
                clear_terminal()

            elif choice == "2":
                orderInterface()

            elif choice == "3":
                print("Avslutter programmet.")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()

if __name__ == "__main__":
    main()