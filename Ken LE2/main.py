import time
from util.user_manager import UserManager

def main():
    while True:
        user = UserManager()
        print('-' * 50)
        print("           Welcome to Dice Roll Game!")
        print('-' * 50)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print('-' * 50)
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            user.register()
        elif choice == "2":
            user.login()
        elif choice == "3":
            print("Exiting...")
            time.sleep(0.5)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please Try Again.")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()