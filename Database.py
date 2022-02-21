import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from datetime import datetime
import os


# TODO: check that the queries and database stuff works
# TODO: function descriptors
class DatabaseWrapper:
    conn = None

    def close(self):
        print("Closing database...")

        self.cursor.close()
        self.conn.close()

        print("Successfully closed connection to database!")

    def new_user(self, username: str, passwd: str, is_admin=False, admin_passwd=""):
        if is_admin and not self.verify_admin(admin_passwd):
            return False

        query = "INSERT INTO users (username, password, isAdmin) VALUES ( %s, crypt(%s, gen_salt('bf')), %s )"
        salted_passwd = username[:len(username) // 2] + passwd + username[len(username) // 2:]
        data = (username, salted_passwd, str(is_admin).lower())

        self.cursor.execute(query, data)
        self.conn.commit()

        return True

    def check_user(self, username: str, passwd: str):
        query = "SELECT (password=crypt(%s, password)) AS pwd_match from users where username = %s"
        salted_passwd = username[:len(username) // 2] + passwd + username[len(username) // 2:]
        data = (salted_passwd, username)

        self.cursor.execute(query, data)

        res = self.cursor.fetchone()

        if res is None:
            return False
        else:
            return res[0]

    def is_admin(self, username: str):
        query = "SELECT isadmin from users where username = %s"
        data = (username,)

        self.cursor.execute(query, data)

        res = self.cursor.fetchone()

        return res[0]

    def user_exists(self, username: str):
        query = "SELECT username from users where username = %s"
        data = (username,)

        self.cursor.execute(query, data)

        res = self.cursor.fetchone()

        if res is None:
            return False
        else:
            return len(res) > 0

    def verify_admin(self, key: str):
        query = "SELECT (password=crypt(%s, password)) AS pwd_match from users where username = 'admin_key'"
        data = (key,)

        self.cursor.execute(query, data)
        return self.cursor.fetchone()[0]

    def __init__(self, db_name: str, db_passwd: str, db_user='postgres', db_port='5432', db_host='localhost'):
        try:
            # Establishing the connection
            self.conn = psycopg2.connect(
                database=db_name, user=db_user, password=db_passwd, host=db_host, port=db_port
            )

            # TODO: Check if all the required tables are present
            print("Successfully connected to database %s" % db_name)

            # Creating a cursor object
            self.cursor = self.conn.cursor()
        except BaseException as e1:
            print("Database %s does not exist" % db_name)
            ans = input("Do you want to create the database now? ([yes]/no): ")

            if ans == "no":
                sys.exit(1)

            print("Connecting to PostgreSQL...")

            try:
                # Connect to the default database (we need a cursor to create the database, and we need a connection
                # to create a cursor so...)
                conn = psycopg2.connect(database=db_name, user=db_user, password=db_passwd, host=db_host, port=db_port)
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            except BaseException as e2:
                # Password might be wrong, but I do not want to ask again. Just exit with an error

                print("Something went wrong...")
                print(e2)
                sys.exit(1)

            print("Connected!")
            print("Creating database...")

            # Creating a cursor object
            cursor = conn.cursor()

            # Inserting the order to create the database
            cursor.execute("CREATE DATABASE " + db_name + ";")

            # Execute the order
            conn.commit()

            print("Database created successfully!")

            # Close the temporary connection to the default database
            # Notice that these are **local** variables
            cursor.close()
            conn.close()

            print("Connecting to the newly created database...")

            # TODO: error handling (the password might be wrong)
            self.conn = psycopg2.connect(
                database=db_name, user=db_user, password=db_passwd, host=db_host, port=db_port
            )

            self.cursor = self.conn.cursor()

            print("Importing the pgcrypto to encode passwords...")

            self.cursor.execute('create extension pgcrypto')
            self.conn.commit()

            print("Creating users' table...")

            # Create the table to store the data for the users
            self.cursor.execute(
                'create table users (username text primary key, password text not null, isAdmin boolean DEFAULT FALSE)')

            # Execute the changes
            self.conn.commit()

            print("Creating admin verification key...")
            admnkey = ""
            while admnkey == "":
                admnkey = input("Admin key: ")

            query = "INSERT INTO users (username, password) VALUES ( 'admin_key', crypt(%s, gen_salt('bf')) )"
            data = (admnkey,)

            self.cursor.execute(query, data)
            self.conn.commit()

            print("Done! Database is ready to use")
