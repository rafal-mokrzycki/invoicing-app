#!/usr/bin/env python
def main():
    update_credentials()
    create_database()
    feed_database()


def update_credentials():
    print("update_credentials")


def create_database():
    print("create_database")


def feed_database():
    print("feed_database")


if __name__ == "__main__":
    # create credentials.json file with default settings for a DB
    update_credentials()
    # create a database (database.db file with all the required tables, yet empty)
    create_database()
    # feed tables with sample data
    feed_database()
    # final ver
    main()
