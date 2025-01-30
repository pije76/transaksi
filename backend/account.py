

class Account:
    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

        def deposit(self, amount):
            if amount > 0:
                self.balance += amount
                print(f"{amount} deposited successfully.")
            else:
                print("Deposit amount must be positive.")

        def withdraw(self, amount):
            if amount > self.balance:
                print("Insufficient balance.")
            elif amount <= 0:
                print("Withdrawal amount must be positive.")
            else:
                self.balance -= amount
                print(f"{amount} withdrawn successfully.")

        def get_balance(self):
            return self.balance


        def display(self):
            print(f"Account Number: {self.account_number}")
            print(f"Account Holder: {self.name}")
            print(f"Balance: {self.balance}")


# Define the Bank class
class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, name, initial_deposit=0.0):
        if account_number in self.accounts:
            print("Account number already exists.")
        else:
            account = Account(account_number, name, initial_deposit)
            self.accounts[account_number] = account
            print("Account created successfully.")

    def get_account(self, account_number):
        account = self.accounts.get(account_number)
        if account:
            return account
        else:
            print("Account not found.")
            return None

    def display_all_accounts(self):
        if not self.accounts:
            print("No accounts in the bank.")
        else:
            for account in self.accounts.values():
                account.display()
                print("-" * 20)

# User Interaction
def main():
    bank = Bank()

    while True:
        print("\n--- Welcome to the Python Bank ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Display All Accounts")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter account number: ")
            name = input("Enter account holder name: ")
            initial_deposit = float(input("Enter initial deposit (default 0): "))
            bank.create_account(account_number, name, initial_deposit)

        elif choice == '2':
            account_number = input("Enter account number: ")
            account = bank.get_account(account_number)

            if account:
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)

        elif choice == '3':
            account_number = input("Enter account number: ")
            account = bank.get_account(account_number)

            if account:
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)

        elif choice == '4':
            account_number = input("Enter account number: ")
            account = bank.get_account(account_number)

            if account:
                print(f"Account Balance: {account.get_balance()}")

        elif choice == '5':
            bank.display_all_accounts()

        elif choice == '6':
            print("Thank you for using Python Bank!")
        break

    else:
        print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
