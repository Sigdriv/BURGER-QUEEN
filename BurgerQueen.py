import sqlite3 as sql
import os
from colorama import Fore

current_user = None
error = None
info = None
employed = False

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
    global employed
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
        if is_employee():
            employed = True
        return True
    else:
        error = "Ugyldig brukernavn eller passord \nVenligst prøv igjen"
        return False

def signUp():
    global current_user
    global error
    global info
    global employed
    clear_terminal()
    print()
    
    print("2. Opprett bruker")
    print("Skriv inn ønsket brukernavn og passord")
    username = input("Brukernavn: ")
    password = input("Passord: ")
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password))
    if c.fetchone() is None:
        error = "Brukernavnet eksisterer allerede \nVennligst velg et annet"
        logInnInterface()
    else:
        c.execute("INSERT INTO User VALUES (?, ?, 0)", (username, password))
        conn.commit()
        conn.close()
        info = username + " er nå registrert og er logget inn"
        current_user = username
        if is_employee():
            employed = True
        return True
    
def is_employee():
    global current_user
    global employed

    conn = connect_database()
    c = conn.cursor()

    c.execute("SELECT Hired FROM User WHERE UsernameID = ?", (current_user,))
    is_employee = c.fetchone()[0]

    conn.close()
    employed = bool(is_employee)
    

def clear_terminal():
    global current_user
    global error
    global info
    if current_user is not None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        if employed:
            print("Logget inn som " + current_user + " (Ansatt)")
        else:
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

def get_burger():
    conn = connect_database()
    c = conn.cursor()

    c.execute("SELECT * FROM Burgers")
    burger_data = c.fetchall()
    burger_names = [row[0] for row in burger_data]
    burger_IDs = [row[1] for row in burger_data]
    print(burger_names)
    print(burger_IDs)
    input('Press enter to continue... ')

    conn.close()
    return burger_names, burger_IDs

def orderInterface():
    global error
    
    clear_terminal()
    print("1. Ordre")
    print()
    if employed:
        print("1. Vis ordre")
        print("2. Registrer ordre")
        print("3. Produser ordre")
        print("4. Tilbake")
        choice = input("Velg en handling: ")
        
        if choice == "1":
            display_user_orders()
        elif choice == "2":
            place_order()
        elif choice == "3":
            # produce_order()
            pass
        elif choice == "4":
            main()
        else:
            error = "Ugyldig valg. Prøv igjen."
            orderInterface()
    else:
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
    print("1. Registrer ordre")
    print()
    
    burger_names_ID = get_burger()
    
    print("Available Burgers:")
    print('BurgerID: Burger navn')
    for burger_ID, burger_name in enumerate(burger_names_ID, start=1):
        print(f"{burger_ID}. {burger_name}")
    print()
        
    burger_ID = input("Skriv inn burgerID-en: ")
    
    if burger_name not in burger_names_ID:
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

def displayProducedOrders():
    count = 0
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Produced = 1")
    orders = c.fetchall()
    print()
    print("Alle produserte ordre:")
    print()
    for order in orders:
        count += 1
        print(f"{count}. BestillingsID: {order[0]}, Bruker: {order[1]}, Burger: {order[2]}, Produsert: {'Ja' if order[3] else 'Nei'}")
        
    conn.close()

def displayNotProducedOrders():
    count = 0
        
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Produced = 0")
    orders = c.fetchall()
    print()
    print("Alle ikke-produserte ordre:")
    print()
    for order in orders:
        count += 1
        print(f"{count}. BestillingsID: {order[0]}, Bruker: {order[1]}, Burger: {order[2]}, Produsert: {'Ja' if order[3] else 'Nei'}")

    conn.close()

def displayUserOrders():
    global error
    count = 0
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Who = ?", (current_user,))
    orders = c.fetchall()
    
    if not orders:
        error = "No orders found for the current user."
        clear_terminal()
        print('1. Vis ordre')
        print()
    else:
        print("Dine Bestillinger:")
        print()
        for order in orders:
            count += 1
            print(f"{count}. BestillingsID: {order[0]}, Burger: {order[2]}, Produsert: {'Ja' if order[3] else 'Nei'}")
    
    conn.close()
    
def display_user_orders():
    global error
    clear_terminal()
    print("1. Vis ordre")
    print()
    
    if employed:
        
        print("1. Alle ordre")
        print("2. Produserte ordre")
        print("3. Ikke-produserte ordre")
        print("4. Tilbake")
        choice = input("Velg en handling: ")
        
        if choice == "1":
            clear_terminal()
            print("1. Alle ordre")
            displayProducedOrders()
            
            displayNotProducedOrders()
            print()
            
            input("Press enter for å fortsette... ")
            display_user_orders()
        
        elif choice == "2":
            clear_terminal()
            print("2. Produserte ordre")
            displayProducedOrders()
            print()
            
            input("Press enter for å fortsette... ")
            display_user_orders()
        
        elif choice == "3":
            clear_terminal()
            print("3. Ikke-produserte ordre")
            displayNotProducedOrders()
            print()
            
            input("Press enter for å fortsette... ")
            display_user_orders()
        
        elif choice == "4":
            orderInterface()
        
        else:
            error = "Ugyldig valg. Prøv igjen."
            display_user_orders()
    
    else:
        displayUserOrders()
        
        print()
        input("Press enter for å fortsette... ")
        orderInterface()


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
            print("1. Ordre")
            print("2. Logg ut")
            print("3. Avslutt")

            choice = input("Velg en handling: ")

            if choice == "2":
                current_user = None
                clear_terminal()

            elif choice == "1":
                orderInterface()

            elif choice == "3":
                print("Avslutter programmet.")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()

if __name__ == "__main__":
    main()