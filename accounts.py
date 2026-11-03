import csv
from datetime import datetime
from transactions import Transaction
import hashlib
import random
import os

"""Line 31 I used the "except" rule so the program doesn't crash if .csv file is not found."""
class Rude:
    def __init__(self):
        self.user_name = None
        self.user_surname = None
        self.freestyle = None
        self.cript = None
        self.cript2 = None
        self.account_number = None
        self.readable_account_number = None

    """Created a method that checks if the number already exists.
       Since the account registered are saved in the
       'account_balances.csv' file, we read through the file
       to check if the phone number already exists."""
    
    def phone_exists(self, freestyle):
        self.freestyle = freestyle
        try:
            with open('account_balances.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Phone number"] == self.freestyle:
                        return True
        except FileNotFoundError:
            return False

        return False
    
    """Here is all the code for accounts registrations."""
       
    def cript_hash(self):
        while True:
            self.user_name = input("Enter your name: ").capitalize()
            if self.user_name.isalpha() == False:
                print(f"Name: {self.user_name} is invalid.")
                continue
            else:
                break
        while True:
            self.user_surname = input("Enter your surname: ").capitalize()
            
            """Making sure the name only contains alphabets
            and if not, the user will be prompted to enter name again."""
            
            if self.user_surname.isalpha() == False:
                print(f"Surname: {self.user_surname} is invalid.")
                continue
            else:
                break

            """The user will be prompted to enter a phone number"""
        while True:
            self.freestyle = input("Enter your phone number"
                                " (10 digits): ")
            
            """Making sure the phone number is contains only digits"""
            if (not self.freestyle.isdigit() or len(self.freestyle) != 10
                    or not self.freestyle.startswith("0")):
                print("Invalid phone number")
                continue
            elif self.phone_exists(self.freestyle):
                print("This phone number is already registered.")
                while True:
                    
                    """Created a variable that will hold the select option
                        if the phone is already registered."""
                        
                    selec = int(input("Select 1 to login or 2 to try again: "))
                    if selec == 1:
                        """If the user chooses to option 1,
                        log in sequence will be executed."""
                        transactions = Transaction()
                        if transactions.cloud():
                            transactions.welcome()
                            return
                    elif selec == 2:
                        """If the user chooses to option 2,
                        the registration sequence will be executed."""
                        register = Rude()
                        register.cript_hash()                            
                        break
                    elif selec != 1 or selec != 2:
                        print("Invalid option.")
                        continue
                    else:
                        break
            else:
                break

        while True:
            """User prompted to create a pin, 
            checking the number is only
            numbers and the length is 4 or 5."""
            
            self.cript = input("Create a pin: ")
            
            """Check if it's invalid first"""
            if not self.cript.isdigit() or len(self.cript) not in (4, 5):
                print("Pin is invalid, use numbers only and must be between 4 and 5 numbers")
                continue
            
            """If it IS valid, immediately ask for confirmation"""
            self.cript2 = input("Confirm your pin: ")
            if self.cript2 != self.cript:
                print("Pin does not match.")
                continue  # Starts the loop over if they don't match
            
            """If both match, hash it and break out of the loop safely"""
            digest = hashlib.sha256(self.cript.encode()).hexdigest()
            print("Pin is valid and confirmed.")
            break                            
            
        balance = 0

        """The user details will be saved in the 
        'account_balances.csv' file"""    
        user_headers = ["Phone number", "Name", 
                        "Surname", "Password",
                        "Account number", "Balance",
                        "Read_Acc",
                        "Date and time created"]
        
        """The user details will be saved in the 
        'logs.csv' file"""        
        users_headers = ["Phone number", "Event type",
                            "Date and time created"]
        
       
        self.account_number = random.randint(10000000, 99999999)
        self.readable_account_number = self.account_number
        digest1 = hashlib.sha256(str(self.account_number).
                                    encode()).hexdigest()
        right_now = datetime.now().replace(microsecond=0)

                 
        """Once the account is successfully created, 
        the details are saved and displayed."""
        
        print(f"Welcome {self.user_name} {self.user_surname}!")
        print(f"{self.freestyle} is now logged in.")
        print(f"This is your account number: {self.account_number}")
        print("NB!! Please take note of your account number")
        
        file_exists = os.path.isfile("account_balances.csv")
        
        with open("account_balances.csv", "a", newline="") as files:
            writer = csv.DictWriter(files, fieldnames=user_headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Phone number": self.freestyle,
                "Name": self.user_name,
                "Surname": self.user_surname,
                "Password": digest,
                "Account number": digest1,
                "Balance": balance,
                "Read_Acc": self.readable_account_number,
                "Date and time created": right_now
            })
            
        file_exists = os.path.isfile("log.csv")
        with open("log.csv", "a", newline="") as files:
            writer = csv.DictWriter(files, fieldnames=users_headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Phone number": self.freestyle,
                "Event type": "REGISTERED",
                "Date and time created": right_now
                })
if __name__ == "__main__":
    user = Rude()
    user.cript_hash()