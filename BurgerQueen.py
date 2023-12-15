import sqlite3 as sql
import os
from colorama import Fore

current_user = None
error = None
info = None
employed = False

# Function to clear the terminal and display error/info and welcome message
def clear_terminal():
    global current_user
    global error
    global info
    
    # Clear the terminal if their is a user logged in
    if current_user is not None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
            
        # Display current user and if they are an employee
        if employed:
            print("Logget inn som " + current_user + " (Ansatt)")
        else:
            print("Logget inn som " + current_user)
            
    # Clear the terminal if their is no user logged in
    else:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        
        print(f"{Fore.YELLOW}Du er ikke logget inn, \nVennligst logg inn eller opprett bruker{Fore.RESET}") # Display that the user is not logged in and need to log in or sign up
        
    print("Velkommen til Burger Queen") # Display welcome message
    
    # Display error/info if there is any
    if error is not None:
        print(f'{Fore.RED}En feil oppsto: {error} {Fore.RESET}')
        error = None
    if info is not None:
        print(f'{Fore.GREEN}{info} {Fore.RESET}')
        info = None

# Function to connect to the database
def connect_database():
    return sql.connect("BurgerQueen.db")

# Function to the log in interface
def logInnInterface():
    global error
    
    clear_terminal() # Clear the terminal
    print()
    
    # Display the log in interface and what the user can do
    print("1. Logg inn")
    print("2. Opprett bruker")
    print("3. Tilbake")
    choice = input("Velg en handling: ") # Ask the user to choose what they want to do
    
    # Check what the user chose and call the corresponding function
    if choice == "1": # If the user chose to log in
        if logInn(): # If the user successfully logged in
            clear_terminal()
            pass
        else: # If the user failed to log in
            logInnInterface()

    elif choice == "2": # If the user chose to sign up
        if signUp(): # If the user successfully signed up
            pass # Do nothing
        else: # If the user failed to sign up
            signUp() # Call the sign up function again
    
    elif choice == "3": # If the user chose to go back
        clear_terminal() # Clear the terminal
        return False # Return False to indicate that the user chose to go back
    
    else: # If the user chose an invalid option
        error = "Ugyldig valg. Prøv igjen." # Display an error message
        logInnInterface() # Call the log in interface again
    
# Function to log in
def logInn():
    global current_user
    global error
    global employed
    global info
    clear_terminal()
    
    # Display that the user is at the logging in page
    print("1. Logg inn")
    print()
    print("Please enter your username and password") # Ask the user to enter their username and password
    print()
    username = input("Username: ") # Ask the user to enter their username
    password = input("Password: ") # Ask the user to enter their password

    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password)) # Execute a SQL statement to check if the username and password is correct
    if c.fetchone() is not None: # If the username and password is correct
        current_user = username # Set the current user to the username
        if is_employee(): # Check if the user is an employee
            employed = True # Set employed to True
        info = "Innlogging vellykket for " + username # Set the info variable to that the user successfully logged in and what their username is and display it when the terminal gets cleared
        main() # Call the main function
    else: # If the username and password is incorrect
        error = "Ugyldig brukernavn eller passord \nVenligst prøv igjen" # Display an error message
        return False # Return False to indicate that the user failed to log in

# Function to sign up
def signUp():
    global current_user
    global error
    global info
    global employed
    clear_terminal() # Clear the terminal
    
    # Display that the user is at the sign up page
    print("2. Opprett bruker")
    print()
    print("Skriv inn ønsket brukernavn og passord") # Ask the user to enter their desired username and password
    username = input("Brukernavn: ") # Ask the user to enter their desired username
    password = input("Passord: ") # Ask the user to enter their desired password
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password)) # Execute a SQL statement to check if the username is already taken
    if c.fetchone() is not None: # If the username is already taken
        error = "Brukernavnet eksisterer allerede \nVennligst velg et annet" # Display an error message
        logInnInterface() # Call the log in interface
    else: # If the username is not taken
        c.execute("INSERT INTO User VALUES (?, ?, 0)", (username, password)) # Execute a SQL statement to insert the username and password into the database
        conn.commit() # Commit the changes to the database
        conn.close() # Close the connection to the database
        info = username + " er nå registrert og er logget inn" # Set the info variable to the user successfully signed up and what their username is and display it when the terminal gets cleared
        current_user = username # Set the current user to the username
        if is_employee(): # Check if the user is an employee
            employed = True # Set employed to True
        return True # Return True to indicate that the user successfully signed up

# Function to check if the user is an employee
def is_employee(): 
    global current_user # Get the current user
    global employed # Get the employed variable

    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements

    c.execute("SELECT Hired FROM User WHERE UsernameID = ?", (current_user,)) # Execute a SQL statement to check if the user is an employee
    is_employee = c.fetchone()[0] # Get the result of the SQL statement

    conn.close() # Close the connection to the database
    employed = bool(is_employee) # Set employed to the result of the SQL statement

# a function to get the burger names and IDs from the database
def get_burger():
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements

    c.execute("SELECT * FROM Burgers") # Execute a SQL statement to get all the burgers
    burger_data = c.fetchall() # Get the result of the SQL statement

    conn.close() # Close the connection to the database
    return burger_data # Return the result of the SQL statement

# Function to the order interface
def InventarInterface():
    global error
    
    clear_terminal() # Clear the terminal
    print("3. Inventar") # Display that the user is at the Inventar page
    print()
    # Displays the options the user can choose
    print("1. Vis inventar")
    print("2. Oppdater ingrediens mengde")
    print("3. Tilbake")
    choice = input("Velg en handling: ")
    
    # Check what the user chose and call the corresponding function
    if choice == "1":
        display_inventory() # Call the display inventory function
    elif choice == "2":
        updateIngredientCount() # Call the update ingredient count function
    elif choice == "3":
        orderInterface() 
    else:
        error = "Ugyldig valg. Prøv igjen."
        InventarInterface()

def display_inventory():
    global error
    global info
    
    clear_terminal()
    print("1. Vis inventar")
    print()
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Ingredients")
    ingredients = c.fetchall()
    
    print("Ingredienser:")
    print()
    for ingredient in ingredients:
        print(f"Ingrediensnavn: {ingredient[0]}, Mengde: {ingredient[1]}")
    
    conn.close()
    
    print()
    input("Press enter for å fortsette... ")
    InventarInterface()

def updateIngredientCount():
    global error
    global info
    
    clear_terminal()
    print("2. Oppdater ingrediens mengde")
    print()
    
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM Ingredients")
    
    ingredients = c.fetchall()
    
    count = 0
    for ingredient in ingredients:
        count += 1
        print(f"{count}. Ingrediensnavn: {ingredient[0]}, Mengde: {ingredient[1]}")
    print()
    
    ingredientID = input("Skriv inn ingrediensID eller press enter for å avbryte: ")
    
    if ingredientID == "":
        InventarInterface()
    
    try:
        ingredientID = int(ingredientID)
    except ValueError:
        error = "Ugyldig input. IngredientID må være et tall. Prøv igjen."
        updateIngredientCount()
        return
    
    match ingredientID:
        case 1:
            ingredient_name = "Burgerbrød topp og bunn"
        case 2:
            ingredient_name = "Burgerkjøtt"
        case 3:
            ingredient_name = "Salat"
        case 4:
            ingredient_name = "Tomat"
        case 5:
            ingredient_name = "Ost"
        case 6:
            ingredient_name = "Agurk"
        case 7:
            ingredient_name = "Potet"
        case _:
            error = "Ugyldig valg. Prøv igjen."
            updateIngredientCount()
    
    c.execute("SELECT * FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,))
    ingredient = c.fetchone()

    if ingredient is None:
        error = "Ugyldig ingrediensNavn. Prøv igjen. Må rettes opp i koden"
        updateIngredientCount()
        return
    
    print()
    validate = input(f'Er det "{ingredient_name}" du vil legge til mer av? (y/n): ')
    
    if validate.lower() == "n":
        updateIngredientCount()
        return
        
    print()
        
    print('\nEksempel på å legge til 10: \n10 \n\nEksempel på å fjerne 10: \n-10 \n\n')
    IngredientCount = input("Hvor mye vil du legge til eller fjerne? Skriv inn antall eller trykk enter for å avbryte: ")
    
    if IngredientCount == "":
        InventarInterface()
    
    c.execute("UPDATE Ingredients SET Much = Much + ? WHERE IngrediensID = ?", (IngredientCount, ingredient_name,))
        
    c.execute("SELECT Much FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,))
    IngredientCountTotal = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    info = f'Oppdatert ingredient "{ingredient_name}" med {IngredientCount} stk. Totalt antall for "{ingredient_name}" er nå: {IngredientCountTotal}'
    InventarInterface()

def orderInterface():
    global error
    
    clear_terminal()

    if employed:
        print("1. Ansatt handlinger")
        print()
        
        print("1. Vis ordre")
        print("2. Produser ordre")
        print('3. Inventar')
        print("4. Tilbake")
        choice = input("Velg en handling: ")
        
        if choice == "1":
            display_user_orders()
        elif choice == "2":
            produce_order()
            pass
        elif choice == "3":
            InventarInterface()
        elif choice == "4":
            main()
        else:
            error = "Ugyldig valg. Prøv igjen."
            orderInterface()
    else:
        print("1. Ordre")
        print()
        print("1. Vis dine ordre")
        print("2. Registrer ordre")
        print("3. Slett ordre")
        print("4. Tilbake")
        choice = input("Velg en handling: ")
        
        if choice == "1":
            display_user_orders()
        elif choice == "2":
            place_order()
        elif choice == "3":
            delete_order()
        elif choice == "4":
            main()
        else:
            error = "Ugyldig valg. Prøv igjen."
            orderInterface()


def delete_order():
    global error
    global info
    clear_terminal()
    print("3. Slett ordre")
    print()
    
    displayUserOrders()
    
    print()
    
    order_to_delete = input("Hvilken ordre vil du slette? Skriv inn bestillingsID-en eller trykk enter for å avbryte: ")
    
    if order_to_delete == "":
        orderInterface()
    
    try:
        order_to_delete = int(order_to_delete)
    except ValueError:
        error = "Ugyldig input. BestillingsID må være et tall. Prøv igjen."
        delete_order()
        return
    
    conn = connect_database()
    c = conn.cursor()
    
    # Retrieve order details
    c.execute("SELECT * FROM Orders WHERE OrderID = ?", (order_to_delete,))
    order = c.fetchone()
    
    if order is None:
        error = "Ugyldig bestillingsID. Prøv igjen."
        delete_order()
        return
    
    if order[1] != current_user:
        error = "Du kan bare slette dine egne ordre."
        delete_order()
        return
    
    # Delete the order
    c.execute("DELETE FROM Orders WHERE OrderID = ?", (order_to_delete,))
    conn.commit()
    conn.close()
    
    info = f"Ordre {order_to_delete} har blitt slettet."
    orderInterface()
            

def produce_order():
    global error
    global info
    clear_terminal()
    print('2. Produser ordre')
    
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
    
    # Retrieve order details
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
    
    # Retrieve ingredients for the burger from BurgerIngredients table
    burger_id = order[2]
    c.execute("SELECT IngredientsID FROM BurgerIngredients WHERE BurgerID = ?", (burger_id,))
    ingredients_names = [row[0] for row in c.fetchall()]
    
    # Check if there are enough ingredients in stock
    for ingredient_name in ingredients_names:
        c.execute("SELECT Much FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,))
        quantity = c.fetchone()[0]
        if quantity <= 0:
            error = f'Ikke nok av ingrediensen "{ingredient_name}" på lager. Kan ikke produsere ordren.'
            orderInterface()
    
    auth = input(f"Er det denne ordren du vil produsere:\n  BestillingsID: {order[0]} \n  Opprettet av: {order[1]} \n  Produkt: {order[2]} \n(y/n): ")
    
    if auth.lower() == "n":
        produce_order()
        return
    
    # Print the ingredients
    print()
    print(f"Ingredienser for {order[2]}: \n{', '.join(ingredients_names)}")
    print()
    
    
    input("Trykk enter for å produsere ordren... ")
    
    
    # Update the ingredient quantities in the IngredientQuantities table
    for ingredient_name in ingredients_names:
        c.execute("UPDATE Ingredients SET Much = Much - 1 WHERE IngrediensID = ?", (ingredient_name,))
        
    # Update the order status to indicate it has been produced
    c.execute("UPDATE Orders SET Produced = 1 WHERE OrderID = ?", (burger_produser,))
    conn.commit()
    conn.close()
    
    info = f"Ordre {burger_produser} har blitt laget. Ingredienser trekt fra ingredienser."
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

    info = f'Ordre med "{burger_name}" ble velykket opprettet!'
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
        error = f"Ingen ordre funnet for {current_user}"
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
    if not employed:
        print("1. Vis dine ordre")
    else:
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
                exit()

            else:
                error = "Ugyldig valg. Prøv igjen."
                main()
        
        else:
            if employed:
                print("1. Ansatt handlinger")
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
                    exit()

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
                    exit()

                else:
                    error = "Ugyldig valg. Prøv igjen."
                    main()

if __name__ == "__main__":
    main()