#!/usr/bin/env python
import re
import sys


def main(email):
    mail = get_and_check_email(email)
    return mail
    # match = None
    # while match is None:
    #     email = input("Pass your email: ")
    #     match = re.fullmatch(
    #         r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+asd\.[A-Z|a-z]{2,}\b", email
    #     )


def get_and_check_email(email):
    while True:
        email = input("Pass your email (or [q] to quit): ")
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
    main(sys.argv)
    # update_credentials()
