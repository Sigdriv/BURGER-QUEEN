import sqlite3 as sql
import os
from colorama import Fore

current_user = 'test'
error = None
info = None
employed = True

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
    global info
    clear_terminal()
    
    print("1. Logg inn")
    print()
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
        info = f'Innlogging vellykket for {username}'
        main()
    else:
        error = "Ugyldig brukernavn eller passord \nVenligst prøv igjen"
        return False

def signUp():
    global current_user
    global error
    global info
    global employed
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
        print(f"{Fore.RED}Du er ikke logget inn, \nVennligst logg inn eller opprett bruker{Fore.WHITE}")
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

    conn.close()
    return burger_data

def orderInterface():
    global error
    
    clear_terminal()
    print("1. Ordre")
    print()
    if employed:
        print("1. Vis ordre")
        print("2. Produser ordre")
        print("3. Tilbake")
        choice = input("Velg en handling: ")
        
        if choice == "1":
            display_user_orders()
        elif choice == "2":
            error = "Denne funksjonen er under implementert enda."
            produce_order()
            pass
        elif choice == "3":
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
            

def produce_order():
    global error
    global info
    clear_terminal()
    print('2. Produser ordre')
    print()
    
    displayNotProducedOrders()
    print()
    
    burger_produser = input("Hvilken burger vil du produsere? Skriv inn bestillingsID-en eller trykk enter for å avbryte: ")
    
    if burger_produser == "":
        orderInterface()
    
    try:
        burger_produser = int(burger_produser)
    except ValueError:
        error = "Ugyldig input. BestillingsID må være et tall. Prøv igjen."
        produce_order()
        return
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE OrderID = ?", (burger_produser,))
    order = c.fetchone()
    
    if order is None:
        error = "Ugyldig bestillingsID. Prøv igjen."
        produce_order()
        return
    
    if order[3] == 1:
        error = "Denne ordren er allerede produsert."
        produce_order()
        return
    
    c.execute("UPDATE Orders SET Produced = 1 WHERE OrderID = ?", (burger_produser,))
    conn.commit()
    conn.close()
    
    info = f"Order {burger_produser} has been produced."
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
    for burger_name, burger_ID in burger_names_ID:
        print(f"{burger_ID}. {burger_name}")
    print()
        
    burger_ID_input = input("Skriv inn burgerID-en: eller enter for å avbryte: ")
    
    if burger_ID_input == "":
        orderInterface()
        return
    
    try:
        burger_ID = int(burger_ID_input)
    except ValueError:
        error = "Ugyldig input. BurgerID må være et tall. Prøv igjen."
        place_order()
        return
    
    # Check if the entered burger_ID is valid
    valid_burger_ids = [burger_ID for _, burger_ID in burger_names_ID]
    print(valid_burger_ids)
    if burger_ID not in valid_burger_ids:
        error = "Ugyldig BurgerID. Prøv igjen."
        place_order()
        return

    # Get the corresponding burger_name
    burger_name = next(name for name, id in burger_names_ID if id == burger_ID)
    
    print("Ordre lastes opp...")
    print("Vent litt")

    conn = connect_database()
    c = conn.cursor()

    c.execute("INSERT INTO Orders (Who, What, Produced) VALUES (?, ?, 0)",
              (current_user, burger_name))
    
    conn.commit()
    conn.close()

    info = f"Order placed successfully for {burger_name} Burger!"
    orderInterface()



def displayProducedOrders():
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Produced = 1")
    orders = c.fetchall()
    print()
    print("Alle produserte ordre:")
    print()
    for order in orders:
        print(f"BestillingsID: {order[0]}, Produkt: {order[2]}")
        
    conn.close()

def displayNotProducedOrders():
        
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Produced = 0")
    orders = c.fetchall()
    print()
    print("Alle ikke-produserte ordre:")
    print()
    for order in orders:
        print(f"BestillingsID: {order[0]}, Produkt: {order[2]}")

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
                print("Avslutter programmet")
                break

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()

if __name__ == "__main__":
    main()