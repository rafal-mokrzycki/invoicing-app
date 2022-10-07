#!/usr/bin/env python
import re
import sys


def main():
    mail = get_and_check_email()
    password = get_and_check_password()
    return mail, password


def get_and_check_email():
    while True:
        email = input("Type in your email (or [q] to quit): ")
        if (
            re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)
            is not None
        ):
            return email
        elif email == "q":
            break
        else:
            print("Wrong email format. Try again.")
            continue


def get_and_check_password():
    while True:
        password1 = input("Type in your email password (or [q] to quit): ")
        if password1 == "q":
            break
        password2 = input("Type in your email password again (or [q] to quit): ")
        if password2 == "q":
            break
        elif password1 == password2:
            return password1
        else:
            print("Your passwords don't match. Try again.")
            continue


def update_credentials(email):
    print(f"Your email is: {email}")


def create_database():
    print("create_database")


def feed_database():
    print("feed_database")


if __name__ == "__main__":
    # create credentials.json file with default settings for a DB
    # update_credentials()

    # create a database (database.db file with all the required tables, yet empty)
    # create_database()

    # feed tables with sample data
    # feed_database()

    # final ver
    print(sys.argv)
    # print(len(sys.argv))
    main()
    # update_credentials()
