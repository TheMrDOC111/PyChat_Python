import json
from SQL import SQL

mysql = SQL


def parse(message):
    message = json.loads(message)
    broadcast = False
    if message["type"] == "auth":
        login = message["login"]
        password = message["password"]

        status, token = authorize(login, password)

        if status:
            message = {"type": "auth", "status": "True", "text": "Login successfully", "token": token}
        else:
            message = {"type": "auth", "status": "False", "text": "Invalid login or password"}

    if message["type"] == "registration":
        login = message["login"]
        password = message["password"]
        status, token = registration(login, password)
        if status:
            message = {"type": "registration", "status": "True", "text": "Registration successfully", "token": token}
        else:
            message = {"type": "registration", "status": "False", "text": "This login was be used"}

    if message["type"] == "message":
        broadcast = True
        token = message["token"]
        message = {"type": "message", "status": "True", "user": mysql.get_name_by_token(mysql, token),
                   "text": message["text"]}
    return json.dumps(message), broadcast


def authorize(login: str, password: str):
    users = mysql.show_all_table(mysql, "users")
    for user in users:
        if user[1] == login and user[2] == password:
            return True, user[3]
    return False, None


def registration(login: str, password: str):
    users = mysql.show_all_table(mysql, "users")
    for user in users:
        if user[1] == login:
            return False, None

    status, token = mysql.add_in_table(mysql, "users", {"login": login, "password": password})
    if status is None:
        return True, token
