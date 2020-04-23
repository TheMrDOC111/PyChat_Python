import mysql.connector
from mysql.connector import Error
import string
import random


class SQL:
    config = {
        'host': 'localhost',
        'database': 'PyChat',
        'user': 'root',
        'password': ''
    }

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.config['host'],
                                                      database=self.config['database'],
                                                      user=self.config['user'],
                                                      password=self.config['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("Your connected to - ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

    def dissconnect(self):
        if (self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

    def show_all_table(self, table: str):
        try:
            request = "SELECT * FROM {}".format(table)
            self.cursor.execute(request)
            return self.cursor.fetchall()
        except Error:
            self.connect(self)
            request = "SELECT * FROM {}".format(table)
            self.cursor.execute(request)
            return self.cursor.fetchall()

    def add_in_table(self, table: str, params: dict):
        try:
            params.update({"token": self.token_generator(self)})
            request = "INSERT INTO {}(`name`, `password`, `token`) VALUES ('{login}', '{password}, {token}')".format(
                table, **params)
            self.cursor.execute(request)
            self.connection.commit()
            return self.connection.rollback(), params.get("token")
        except Error:
            self.connect(self)
            params.update({"token": self.token_generator(self)})
            request = "INSERT INTO {}(`name`, `password`, `token`) VALUES ('{login}', '{password}', '{token}')".format(
                table, **params)
            self.cursor.execute(request)
            self.connection.commit()
            return self.connection.rollback(), params.get("token")

    def get_name_by_token(self, token):
        users = self.show_all_table(self, "users")
        for user in users:
            if token == user[3]:
                return user[1]
        return "NULL"

    def token_generator(self, size=20, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def __init__(self, host='localhost', database='PyChat', user='root', password=''):
        self.config['host'] = host
        self.config['database'] = database
        self.config['user'] = user
        self.config['password'] = password
