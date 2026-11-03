from accounts import Rude
from transactions import Transaction
class Trap(Transaction, Rude):

    def register(self):
        
        """The user will be on the welcome screen
           with the respective options that are available
           to choose from."""
           
        while True:
            print("============================")
            print("   Welcome to PyBank ATM")
            print("============================")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            option = input("Select an option: ")
            
            """Option '1', the user will be directed to the
               registration screen. The 'main.py' inherits
               from the 'accounts.py' (class Rude) file."""
               
            if option == "1":
                register = Rude()
                register.cript_hash()
                
                """Option '2', the user will be able to make
                   available transactions, including viewing his/her
                   statements. For this option the 'main'py' file
                   inherits from the 'transactions.py' file 
                   (class Transactions)."""
                   
            elif option == "2":
                transactions = Transaction()
                if transactions.cloud():
                    transactions.welcome()
                else:
                    print("Session terminated.")
                    return
                
                """The user will be logged out and the app will be
                   terminated."""
                   
            elif option == "3":
                print("Logged out. Stay safe.")
                break
                
            else:
                
                """If the user chooses an invalid option,
                   including the none digit characters, 
                   the respective message will be displayed."""
                   
                print("Invalid option.")
                continue
            
            """The 'if__name__' was used to prevent an inherited
               class from executing autimatically."""
               
if __name__ == "__main__":
    reg = Trap()
    reg.register()