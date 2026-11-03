import hashlib
import csv
from datetime import datetime
import os


class Transaction:
    
    """Created a method that updates the balance(s)
    after a successful transaction"""
    
    def update_balance(self, new_balance):
        rows = []

        with open('account_balances.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Phone number"] == self.freestyle:
                    row["Balance"] = str(new_balance)
                rows.append(row)

        with open('account_balances.csv', 'w', newline='') as file:
            fieldnames = [
                "Phone number", "Name", "Surname", "Password",
                "Account number", "Balance","Read_Acc", "Date and time created"
            ]
            # 👇 ADD extrasaction='ignore' RIGHT HERE 👇
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)

    def __init__(self):
        self.freestyle = None
        self.cript = None
        self.amount = None
        self.account_number = None
        self.readable_account_number = None
        
    """This is where all the code is regarding all transactions,
       including viewing statements."""
       
    def cloud(self):
        user_headers = ["Phone number", "Event type", "Date and time created"]

        file_exists = os.path.isfile("log.csv")
        with open("log.csv", "a", newline="") as files:
            writer = csv.DictWriter(files, fieldnames=user_headers)
            if not file_exists:
                writer.writeheader()

        while True:
            freestyle = input("Please enter registered phone number: ")
            if not freestyle.isdigit() or len(freestyle) != 10 or not freestyle.startswith("0"):
                print("Invalid phone number")
                continue
            
            target_user_row = None
            try:
                with open('account_balances.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Phone number"] == freestyle:
                            target_user_row = row
                            break  
            except FileNotFoundError:
                print("No accounts database found.")
                return False

            if target_user_row is None:
                print("Phone number not registered. Please try again.")
                continue


            self.freestyle = freestyle

            num = 0
            while num < 3:
                cript = input("Please enter PIN: ")
                digest = hashlib.sha256(cript.encode()).hexdigest()

                if target_user_row["Password"] == digest:
                    print("Login successful. Welcome back.\n")
                    right_now = datetime.now().replace(microsecond=0)

                    file_exists = os.path.isfile("log.csv")
                    with open("log.csv", "a", newline="") as files:
                        writer = csv.DictWriter(files, fieldnames=user_headers)
                        if not file_exists:
                            writer.writeheader()
                        writer.writerow({
                            "Phone number": self.freestyle,
                            "Event type": "LOGIN_SUCCESS",
                            "Date and time created": right_now
                        })
                    
                    return True
                else:
                    num += 1
                    print("Incorrect PIN.")
                    
            print("You have exceeded your 3 attempts. Please try again later.")
            return False


    def welcome(self):

        balance = None
        users_headers = ["Phone number", 
                         "Event type", "Date and time created"]
        user_headers = ["Phone number", "Transaction type", "Amount",
                        "Balance", "Read_Acc", "Date and time created"]

        while True:
            print("--- Main Menu ---")
            print("1. Withdraw\n"
                  "2. Deposit\n"
                  "3. Transfer (EFT)\n"
                  "4. View Statement\n"
                  "5. Logout\n")

            try:
                option = int(input("Select an option: "))
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if option == 1:
                event = "Withdraw"
                amount = 0.0
                
                while True:
                    try:
                        amount = float(input("Enter amount you would like to withdraw: "))
                    except ValueError:
                        print("Invalid value. Please enter numbers only.")
                        continue
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                        continue
                    break 

  
                balance = None
                with open('account_balances.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                    
                        if row["Phone number"] == self.freestyle:
                            balance = float(row["Balance"])
                            break

                if balance is None:
                    print("Insufficient funds.")
                    continue

                if amount > balance:
                    print(f"You cannot withdraw more than available balance (Current: R{balance:.2f}).")
                    continue

                new_balance = balance - amount
                self.update_balance(new_balance)
                print(f"Withdrawal successful. New balance: R{new_balance:.2f}")
                
                right_now = datetime.now().replace(microsecond=0)
                file_exists = os.path.isfile("transactions.csv")
                
                with open("transactions.csv", "a", newline="") as files:
                    writer = csv.DictWriter(files, fieldnames=user_headers)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({
                        "Phone number": self.freestyle,
                        "Transaction type": event,
                        "Amount": "-" + str(amount),
                        "Balance": new_balance,
                        "Read_Acc":self.readable_account_number,
                        "Date and time created": right_now
                    })
                            
            elif option == 2:
                import os
                event = "Deposit"
                try:
                    amount = int(input("Amount to deposit: R"))
                except ValueError:
                    print("Invalid amount.")
                    continue

                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue


                with open('account_balances.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    balance = None

                    for row in reader:
                        if row["Phone number"] == self.freestyle:
                            balance = float(row["Balance"])
                            new_balance = balance + amount
                            # 1. Remove self.update_balance from here
                            # 2. Keep a reference to the active row data
                            matched_row = row 
                            break

                if balance is None:
                    print("Insufficient funds.") # (Or user not found)
                    continue

                # Move the update function OUTSIDE of the read loop:
                self.update_balance(new_balance)
                print(f"Deposit successful. New balance: R{new_balance:.2f}")
                right_now = datetime.now().replace(microsecond=0)

                file_exists = os.path.isfile("transactions.csv")
                with open("transactions.csv", "a", newline="") as files:
                    writer = csv.DictWriter(files, fieldnames=user_headers)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({
                        "Phone number": self.freestyle,
                        "Transaction type": event,
                        "Amount": "+" + str(amount),
                        "Balance": new_balance,
                        "Read_Acc": self.readable_account_number,
                        "Date and time created": right_now
                    })

            elif option == 3:
                import os
                event = "Transfer"

                while True:
                    self.account_number = input("Enter recipient account number (8 digits): ")

                    if not self.account_number.isdigit() or len(self.account_number) != 8:
                        print("Error: Account number must be exactly 8 digits.")
                        continue

                    digest = hashlib.sha256(self.account_number.encode()).hexdigest()

                    found = False
                    rows = []
                    recipient = None

                    with open('account_balances.csv', 'r') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            rows.append(row)
                            if row["Account number"] == digest and row["Phone number"] != self.freestyle:
                                found = True
                                recipient = row

                    if not found:
                        print("Error: Account not found, or you tried to transfer to your own account. Try again.")
                        continue
                    break

                try:
                    amount = int(input("Amount to transfer: R"))
                except ValueError:
                    print("Invalid amount.")
                    continue

                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue

                right_now = datetime.now().replace(microsecond=0)

                sender_balance = None
                recipient_balance = float(recipient["Balance"])

                for row in rows:
                    if row["Phone number"] == self.freestyle:
                        sender_balance = float(row["Balance"])

                if sender_balance is None or amount > sender_balance:
                    print("Insufficient funds.")
                    continue

                # ========================================================
                # STEP 1: PERFORM BALANCE MATH BEFORE WRITING TO CSV
                # ========================================================
                new_sender_balance = sender_balance - amount
                new_recipient_balance = recipient_balance + amount

                for row in rows:
                    if row["Phone number"] == self.freestyle:
                        row["Balance"] = str(new_sender_balance)
                    if row["Account number"] == digest:
                        row["Balance"] = str(new_recipient_balance)

                # ========================================================
                # STEP 2: WRITE THE UPDATED BALANCES LIST TO FILE
                # ========================================================
                with open('account_balances.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=rows[0].keys(), extrasaction='ignore')
                    writer.writeheader()
                    writer.writerows(rows)                

                print(f"Transfer successful. R{amount} sent to account {self.account_number}")

                # ========================================================
                # STEP 3: LOG THE EVENT (FIXED INDENTATION)
                # ========================================================
                file_exists = os.path.isfile("log.csv")
                with open("log.csv", "a", newline="") as files:
                    writer = csv.DictWriter(files, fieldnames=users_headers, extrasaction='ignore')
                    if not file_exists:
                        writer.writeheader()
                    # This row write must sit outside the file_exists check!
                    writer.writerow({
                        "Phone number": self.freestyle,
                        "Event type": event,
                        "Date and time created": right_now
                    })

                # ========================================================
                # STEP 4: RECORD THE SENDER TRANSACTION
                # ========================================================
                file_exists = os.path.isfile("transactions.csv")
                with open("transactions.csv", "a", newline="") as files:
                    writer = csv.DictWriter(files, fieldnames=user_headers, extrasaction='ignore')
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({
                        "Phone number": self.freestyle,
                        "Transaction type": event,
                        "Amount": "-" + str(amount),
                        "Balance": new_sender_balance,
                        "Read_Acc": self.readable_account_number,
                        "Date and time created": right_now
                    })
            elif option == 4:                
                
                """The user will be able to view their 
                   statement when choosing option 4."""
                   
                import os
                if os.path.isfile("transactions.csv"):
                    with open('transactions.csv', 'r') as file:
                        reader = csv.DictReader(file)
                        print("--- Statement ---")
                        
                        has_transactions = False
                        for row in reader:
                            if row["Phone number"] == self.freestyle:
                                print(f"{row['Date and time created']} | "
                                    f"{row['Transaction type']} | {row['Amount']} | "
                                    f"{row['Balance']}")
                                has_transactions = True
                        
                        if not has_transactions:
                            print("You have no transaction history yet.")
                else:
                    print("No transactions found.")
                    with open('transactions.csv', 'w', newline='') as file:
                        fieldnames = ["Phone number", "Transaction type", "Amount", "Balance",
                                       "Read_Acc", "Date and time created"]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        
                        writer.writeheader()
                        
                    print("You have no transaction history yet.")
                    
            elif option == 5:
                print("Logged out. Stay safe.")
                break

            else:
                print("Error: Invalid option. Please try again.")
                continue

if __name__ == "__main__":
    
    '''If a user successfully logs in, the welcome method will be run'''
    
    log = Transaction()
    if log.cloud():
        log.welcome()
    else: 
        """If the user misses their pin 3 times, 
           the session will be terminated."""
        print("Session terminated.")