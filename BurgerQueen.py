import sqlite3

username = ""

def loginnInterface():
    
    emptyLinesUpper()
    print("1. Logg inn")
    print("2. Opprett bruker")
    choice = input("Velg en handling: ")
    emptyLinesUpper()
    
    if choice == "1": 
        if loggInn():
            pass
        else:
            loggInn()

    elif choice == "2":
        if signUp():
            pass
        else:
            signUp()

    
    else:
        print("Ugyldig valg. Prøv igjen.")
        return False
    
def loggInn():
        print("Please enter your username and password")
        username = input("Username: ")
        password = input("Password: ")
        emptyLinesUpper()
        conn = connect_database()
        c = conn.cursor()
        c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password))
        if c.fetchone() is not None:
            print("Welcome " + username)
            return True, username
        else:
            print("Ugyldig brukernavn eller passord")
            print("Venligst prøv igjen")
            return False

def signUp():
        print("Skriv inn ønsket brukernavn og passord")
        username = input("Brukernavn: ")
        password = input("Passord: ")
        conn = connect_database()
        c = conn.cursor()
        c.execute("SELECT * FROM User WHERE UsernameID = ? AND Password = ?", (username, password))
        if c.fetchone() is not None:
            print("Brukernavn eksisterer allerede, vennligst velg et annet")
            return False
        else:
            c.execute("INSERT INTO User VALUES (?, ?, 0)", (username, password))
            conn.commit()
            conn.close()
            print(username + " created")
            return True


def emptyLinesUpper(count = 2):
    print('---------------')
    for i in range(count):
        print("")
        
def emptyLines(count = 1):
    for i in range(count):
        print("")

def connect_database():
    return sqlite3.connect("BurgerQueen.db")

# Hovedfunksjon
def main():
    
    emptyLines(2)
    print('------------------------')
    print("Welcome to Burger Queen")
    print('------------------------')

    while True:
        emptyLines(2)
        print("1. Logg inn")
        print("2. Registrer ordre")
        print("3. Avslutt")

        choice = input("Velg en handling: ")

        if choice == "1":
            
            loginnInterface()
            
            if True:
                pass
            else:
                pass
                

        elif choice == "2":
            pass

        elif choice == "3":
            print("Avslutter programmet.")
            break

        else:
            print("Ugyldig valg. Prøv igjen.")

if __name__ == "__main__":
    main()
