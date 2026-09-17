from bank import (
    create_customer,
    get_account,
    deposit,
    withdraw,
    transaction_history
)


def display_menu():
    print("\n==============================")
    print("     ONLINE BANKING SYSTEM")
    print("==============================")
    print("1. Create Account")
    print("2. View Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transaction History")
    print("6. Exit")


while True:

    display_menu()

    choice = input("Enter your choice: ")

    try:

        if choice == "1":

            name = input("Enter customer name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")

            account_number = create_customer(
                name,
                email,
                phone
            )

            print("\nAccount created successfully!")
            print("Your account number:", account_number)


        elif choice == "2":

            account_number = input(
                "Enter account number: "
            )

            account = get_account(account_number)

            if account:

                print("\n----- ACCOUNT DETAILS -----")
                print("Customer ID:", account["customer_id"])
                print("Name:", account["name"])
                print("Email:", account["email"])
                print("Phone:", account["phone"])
                print("Account Number:", account["account_number"])
                print("Balance:", account["balance"])

            else:

                print("Account not found.")


        elif choice == "3":

            account_number = input(
                "Enter account number: "
            )

            amount = float(
                input("Enter deposit amount: ")
            )

            deposit(account_number, amount)

            print("Deposit successful.")


        elif choice == "4":

            account_number = input(
                "Enter account number: "
            )

            amount = float(
                input("Enter withdrawal amount: ")
            )

            withdraw(account_number, amount)

            print("Withdrawal successful.")


        elif choice == "5":

            account_number = input(
                "Enter account number: "
            )

            transactions = transaction_history(
                account_number
            )

            if transactions:

                print("\n----- TRANSACTION HISTORY -----")

                for transaction in transactions:

                    print(
                        "Type:", transaction[0],
                        "| Amount:", transaction[1],
                        "| Description:", transaction[2],
                        "| Date:", transaction[3]
                    )

            else:

                print("No transactions found.")


        elif choice == "6":

            print("\nThank you for using Online Banking System.")
            break


        else:

            print("Invalid choice. Please try again.")


    except ValueError as error:

        print("Error:", error)


    except Exception as error:

        print("Something went wrong:", error)
