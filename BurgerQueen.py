import sqlite3 as sql
import os
from colorama import Fore

current_user = None
error = None
info = None
employed = False
ordersForThisUser = False

# Function to clear the terminal and display error/info and welcome message
def clear_terminal():
    global current_user
    global error
    global info
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
    if current_user is not None:
        # Display current user and if they are an employee
        if employed:
            print("Logget inn som " + current_user + " (Ansatt)")
        else:
            print("Logget inn som " + current_user)
            
    # Clear the terminal if their is no user logged in
    else:
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
    
    if username == "" or password == "":
        error = 'Brukernavn eller passord kan ikke stå tomt'
        return
    
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
        orderInterface() # Call the order interface function
    else:
        error = "Ugyldig valg. Prøv igjen."  # Sets an error message if the user chose an invalid option
        InventarInterface() # Call the Inventar interface function again

def display_inventory(): # Function to display the inventory
    global error # Get the error variable
    global info # Get the info variable
    
    clear_terminal() # Clear the terminal
    print("1. Vis inventar") # Display that the user is at the display inventory page
    print() 
    
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    
    c.execute("SELECT * FROM Ingredients") # Execute a SQL statement to get all the ingredients
    ingredients = c.fetchall() # Get the result of the SQL statement
    
    print("Ingredienser:") 
    print()
    for ingredient in ingredients: # Loop through all the ingredients
        print(f"Ingrediensnavn: {ingredient[0]}, Mengde: {ingredient[1]}") # Display the ingredient name and quantity
    
    conn.close() # Close the connection to the database
    
    print()
    input("Press enter for å fortsette... ")
    InventarInterface() # Call the Inventar interface function

def updateIngredientCount(): # Function to update the ingredient count
    global error # Get the error variable
    global info # Get the info variable
    
    clear_terminal()  # Clear the terminal
    print("2. Oppdater ingrediens mengde") # Display that the user is at the update ingredient count page
    print()
    
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    c.execute("SELECT * FROM Ingredients") # Execute a SQL statement to get all the ingredients
    
    ingredients = c.fetchall() # Get the result of the SQL statement
    
    count = 0 # Set the count variable to 0
    for ingredient in ingredients: # Loop through all the ingredients
        count += 1 # Add 1 to the count variable
        print(f"IngredientID: {count}. Ingrediensnavn: {ingredient[0]}, Mengde: {ingredient[1]}") # Display the ingredientID, name and quantity
    print()
    
    ingredientID = input("Skriv inn ingrediensID eller press enter for å avbryte: ") # Ask the user to enter the ingredientID
    
    if ingredientID == "": # If the user chose to go back
        InventarInterface() # Call the Inventar interface function
    
    try: # Try to convert the ingredientID to an integer
        ingredientID = int(ingredientID)
    except ValueError: # If the ingredientID is not an integer
        error = "Ugyldig input. IngredientID må være et tall. Prøv igjen." # Sets the error message to that the ingredientID must be an integer
        updateIngredientCount() # Call the update ingredient count function again
        return 
    
    match ingredientID: # Check what the ingredientID is
        case 1: # If the ingredientID is 1
            ingredient_name = "Burgerbrød topp og bunn"
        case 2: # If the ingredientID is 2
            ingredient_name = "Burgerkjøtt"
        case 3: # If the ingredientID is 3
            ingredient_name = "Salat"
        case 4: # If the ingredientID is 4
            ingredient_name = "Tomat"
        case 5: # If the ingredientID is 5
            ingredient_name = "Ost"
        case 6: # If the ingredientID is 6
            ingredient_name = "Agurk"
        case 7: # If the ingredientID is 7
            ingredient_name = "Potet"
        case _: # If the ingredientID is not 1-7
            error = "Ugyldig valg. Prøv igjen." # Sets the error message to that the choice is invalid
            updateIngredientCount() # Call the update ingredient count function again
    
    c.execute("SELECT * FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,)) # Execute a SQL statement to get the ingredient
    ingredient = c.fetchone() # Get the result of the SQL statement

    if ingredient is None: # If the ingredient is None
        error = "Ugyldig ingrediensNavn. Dette må rettes opp i koden, ikke din feil som bruker" # Sets the error message to that the ingredient name is invalid
        updateIngredientCount() # Call the update ingredient count function again
        return
    
    print()
    validate = input(f'Er det "{ingredient_name}" du vil legge til mer av? (y/n): ') # Ask the user to validate their choice
    
    if validate.lower() == "n": # If the user chose to go back
        updateIngredientCount() # Call the update ingredient count function again
        return
        
    print()
        
    print('\nEksempel på å legge til 10: \n10 \n\nEksempel på å fjerne 10: \n-10 \n\n') # Display an example of how to add or remove ingredients
    IngredientCount = input("Hvor mye vil du legge til eller fjerne? Skriv inn antall eller trykk enter for å avbryte: ") # Ask the user to enter the amount of ingredients they want to add or remove
    
    if IngredientCount == "": # If the user chose to go back
        InventarInterface() # Call the Inventar interface function
    
    c.execute("UPDATE Ingredients SET Much = Much + ? WHERE IngrediensID = ?", (IngredientCount, ingredient_name,)) # Execute a SQL statement to update the ingredient quantity
        
    c.execute("SELECT Much FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,)) # Execute a SQL statement to get the ingredient quantity
    IngredientCountTotal = c.fetchone()[0] # Get the result of the SQL statement
    
    conn.commit() # Commit the changes to the database
    conn.close() # Close the connection to the database
    
    info = f'Oppdatert ingredient "{ingredient_name}" med {IngredientCount} stk. Totalt antall for "{ingredient_name}" er nå: {IngredientCountTotal}' # Set the info variable to that the ingredient quantity was successfully updated and display it when the terminal gets cleared
    InventarInterface() # Call the Inventar interface function

def orderInterface(): # Function to the order interface
    global error # Get the error variable
    
    clear_terminal() # Clear the terminal

    if employed: # If the user is an employee
        print("1. Ansatt handlinger") # Display that the user is at the employee actions page
        print()
        
        print("1. Vis ordre")
        print("2. Produser ordre")
        print('3. Inventar')
        print("4. Tilbake")
        choice = input("Velg en handling: ") # Ask the user to choose what they want to do
        
        if choice == "1": # If the user chose to display orders
            display_user_orders()
        elif choice == "2": # If the user chose to produce orders
            produce_order()
        elif choice == "3": # If the user chose to go to the inventory page
            InventarInterface()
        elif choice == "4": # If the user chose to go back
            main() 
        else: # If the user chose an invalid option
            error = "Ugyldig valg. Prøv igjen." # Sets the error message to that the choice is invalid
            orderInterface() # Call the order interface function again
    else: # If the user is not an employee
        print("1. Ordre")
        print()
        print("1. Vis dine ordre")
        print("2. Registrer ordre")
        print("3. Slett ordre")
        print("4. Tilbake")
        choice = input("Velg en handling: ") # Ask the user to choose what they want to do
        
        if choice == "1": # If the user chose to display orders
            display_user_orders()
        elif choice == "2": # If the user chose to place an order
            place_order()
        elif choice == "3": # If the user chose to delete an order
            delete_order()
        elif choice == "4": # If the user chose to go back
            main()
        else: # If the user chose an invalid option
            error = "Ugyldig valg. Prøv igjen." # Sets the error message to that the choice is invalid
            orderInterface() # Call the order interface function again


def delete_order(): # Function to delete an order
    global error # Get the error variable
    global info # Get the info variable
    clear_terminal() # Clear the terminal
    print("3. Slett ordre") 
    print()
    
    displayUserOrders() # Call the display user orders function
    
    print()
    
    if ordersForThisUser == False: # If there are no orders for the user
        orderInterface() # Call the order interface function
    
    order_to_delete = input("Hvilken ordre vil du slette? Skriv inn bestillingsID-en eller trykk enter for å avbryte: ") # Ask the user to enter the order they want to delete
    
    if order_to_delete == "": # If the user chose to go back
        orderInterface() # Call the order interface function
    
    try: # Try to convert the order to delete to an integer
        order_to_delete = int(order_to_delete)
    except ValueError: # If the order to delete is not an integer
        error = "Ugyldig input. BestillingsID må være et tall. Prøv igjen."
        delete_order()
        return
    
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    
    # Retrieve order details
    c.execute("SELECT * FROM Orders WHERE OrderID = ?", (order_to_delete,)) # Execute a SQL statement to get the order
    order = c.fetchone() # Get the result of the SQL statement
    
    if order is None: # If the order is None
        error = "Ugyldig bestillingsID. Prøv igjen." # Sets the error message to that the order is invalid
        delete_order() # Call the delete order function again
        return
    
    if order[1] != current_user: # If the order is not created by the current user
        error = "Du kan bare slette dine egne ordre." # Sets the error message to that the user can only delete their own orders
        delete_order() # Call the delete order function again
        return
    
    # Delete the order
    c.execute("DELETE FROM Orders WHERE OrderID = ?", (order_to_delete,)) # Execute a SQL statement to delete the order
    conn.commit() # Commit the changes to the database
    conn.close() # Close the connection to the database
    
    info = f"Ordre {order_to_delete} har blitt slettet." # Set the info variable to that the order was successfully deleted and display it when the terminal gets cleared
    orderInterface() # Call the order interface function
            

def produce_order(): # Function to produce an order
    global error # Get the error variable
    global info # Get the info variable
    clear_terminal() 
    print('2. Produser ordre') 
    
    anyBurger = displayNotProducedOrders() # Call the display not produced orders function
    print() 
    
    if anyBurger == False: # If there are no orders that can be produced
        error = "Ingen ordre som kan produseres." # Sets the error message to that there are no orders that can be produced
        orderInterface() # Call the order interface function
    
    burger_produser = input("Hvilken burger vil du produsere? Skriv inn bestillingsID-en eller trykk enter for å avbryte: ") # Ask the user to enter the order they want to produce
    
    if burger_produser == "": # If the user chose to go back
        orderInterface() # Call the order interface function
    
    try: # Try to convert the order to produce to an integer
        burger_produser = int(burger_produser)
    except ValueError: # If the order to produce is not an integer
        error = "Ugyldig input. BestillingsID må være et tall. Prøv igjen." # Sets the error message to that the order to produce must be an integer
        produce_order()
        return
    
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    
    # Retrieve order details
    c.execute("SELECT * FROM Orders WHERE OrderID = ?", (burger_produser,)) # Execute a SQL statement to get the order
    order = c.fetchone() # Get the result of the SQL statement
    
    if order is None: # If the order is None
        error = "Ugyldig bestillingsID. Prøv igjen." # Sets the error message to that the order is invalid
        produce_order() # Call the produce order function again
        return
    
    if order[3] == 1: # If the order has already been produced
        error = "Denne ordren er allerede produsert." # Sets the error message to that the order has already been produced
        produce_order() # Call the produce order function again
        return 
    
    burger_id = order[2] # Get the burgerID of the order
    c.execute("SELECT IngredientsID FROM BurgerIngredients WHERE BurgerID = ?", (burger_id,)) # Execute a SQL statement to get the ingredients of the burger
    ingredients_names = [row[0] for row in c.fetchall()] # Get the result of the SQL statement
    
    # Check if there are enough ingredients in stock
    for ingredient_name in ingredients_names:
        c.execute("SELECT Much FROM Ingredients WHERE IngrediensID = ?", (ingredient_name,))
        quantity = c.fetchone()[0]
        if quantity <= 0:
            error = f'Ikke nok av ingrediensen "{ingredient_name}" på lager. Kan ikke produsere ordren.'
            orderInterface()
    
    auth = input(f"Er det denne ordren du vil produsere:\n  BestillingsID: {order[0]} \n  Opprettet av: {order[1]} \n  Produkt: {order[2]} \n(y/n): ") # Ask the user to validate their choice
    
    if auth.lower() == "n": # If the user chose to go back
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
    
    info = f"Ordre {burger_produser} har blitt laget. Ingredienser trekt fra inventaret." # Set the info variable to that the order was successfully produced and display it when the terminal gets cleared
    orderInterface()

def place_order(): # Function to place an order
    global current_user # Get the current user
    global error # Get the error variable
    global info # Get the info variable
    clear_terminal()
    print("1. Registrer ordre")
    print()
    
    burger_names_ID = get_burger() # Call the get burger function
    
    print("Available Burgers:")
    for burger_name, burger_ID in burger_names_ID: # Loop through all the burgers
        print(f"{burger_ID}. {burger_name}") # Display the burger name and ID
    print()
        
    burger_ID_input = input("Skriv inn burgerID-en: eller enter for å avbryte: ") # Ask the user to enter the burgerID
    
    if burger_ID_input == "": # If the user chose to go back
        orderInterface() # Call the order interface function
        return
    
    try: # Try to convert the burgerID to an integer
        burger_ID = int(burger_ID_input)
    except ValueError: # If the burgerID is not an integer
        error = "Ugyldig input. BurgerID må være et tall. Prøv igjen." # Sets the error message to that the burgerID must be an integer
        place_order() # Call the place order function again
        return
    
    # Check if the entered burger_ID is valid
    valid_burger_ids = [burger_ID for _, burger_ID in burger_names_ID] # Get all the valid burgerIDs
    print(valid_burger_ids) 
    if burger_ID not in valid_burger_ids: # If the entered burgerID is not valid
        error = "Ugyldig BurgerID. Prøv igjen." # Sets the error message to that the burgerID is invalid
        place_order() # Call the place order function again
        return

    burger_name = next(name for name, id in burger_names_ID if id == burger_ID) # Get the burger name of the entered burgerID
    
    print("Ordre lastes opp...") 
    print("Vent litt")

    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements

    c.execute("INSERT INTO Orders (Who, What, Produced) VALUES (?, ?, 0)", (current_user, burger_name)) # Execute a SQL statement to insert the order into the database
    
    conn.commit() # Commit the changes to the database
    conn.close() # Close the connection to the database

    info = f'Ordre med "{burger_name}" ble velykket opprettet!' # Set the info variable to that the order was successfully placed and display it when the terminal gets cleared
    orderInterface() # Call the order interface function



def displayProducedOrders(All = True): # Function to display the produced orders
    global error # Get the error variable
    global ordersForThisUser # Get the ordersForThisUser variable
    
    conn = connect_database() # Connect to the database
    c = conn.cursor() # Create a cursor to execute SQL statements
    
    c.execute("SELECT * FROM Orders WHERE Produced = 1") # Execute a SQL statement to get all the produced orders
    orders = c.fetchall() # Get the result of the SQL statement
    
    print()
    print("Alle produserte ordre:")
    print()
    
    if All == False: # If the user chose to display all the orders
        if orders == []:
            error = "Ingen produserte ordre funnet."
            ordersForThisUser = False
            display_user_orders()
    
    else:
        if orders == []:
            print(f"{Fore.RED}Ingen produserte ordre funnet.{Fore.RESET}")
    
    for order in orders:
        print(f"BestillingsID: {order[0]}, Produkt: {order[2]}")
        
    conn.close()

def displayNotProducedOrders(All = True):
    global ordersForThisUser
    global error
        
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Produced = 0")
    orders = c.fetchall()
    
        
    print()
    print("Alle ikke-produserte ordre:")
    print()
    
    if All == False:
        if orders == []:
            error = "Ingen ikke-produserte ordre funnet."
            ordersForThisUser = False
            display_user_orders()
            
    else:
        if orders == []:
            print(f"{Fore.RED}Ingen ikke-produserte ordre funnet.{Fore.RESET}")
            return False
            
    for order in orders:
        print(f"BestillingsID: {order[0]}, Produkt: {order[2]}")

    conn.close()

def displayUserOrders():
    global error
    global ordersForThisUser
    count = 0
    
    conn = connect_database()
    c = conn.cursor()
    
    c.execute("SELECT * FROM Orders WHERE Who = ?", (current_user,))
    orders = c.fetchall()
    
    if not orders:
        error = f"Ingen ordre funnet for {current_user}"
        ordersForThisUser = False
        return
    else:
        print("Dine Bestillinger:")
        print()
        for order in orders:
            count += 1
            print(f"{count}. BestillingsID: {order[0]}, Burger: {order[2]}, Produsert: {'Ja' if order[3] else 'Nei'}")
        ordersForThisUser = True
    
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
            displayProducedOrders(True)
            
            displayNotProducedOrders(True)
            print()
            
            input("Press enter for å fortsette... ")
            display_user_orders()
        
        elif choice == "2":
            clear_terminal()
            print("2. Produserte ordre")
            displayProducedOrders(True)
            print()
            
            input("Press enter for å fortsette... ")
            display_user_orders()
        
        elif choice == "3":
            clear_terminal()
            print("3. Ikke-produserte ordre")
            displayNotProducedOrders(True)
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
        
        if ordersForThisUser == True:
            print()
            input("Press enter for å fortsette... ")
            orderInterface()
        else:
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