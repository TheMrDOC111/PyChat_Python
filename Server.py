import socket
from threading import Thread
import threading
import RSA
from SQL import SQL
import API


class Server:

    def get_socket(self):
        while True:
            print("Ожидание пользователя...")
            client, addr = sock.accept()
            clients.append({"connection": client, "socket": addr})
            print("connected:", addr)
            Thread(target=self.check_messages, args=(client,)).start()


    def check_messages(self, client):
        while True:
            try:
                data = client.recv(2048)
                data = str(data.decode("utf-8"))
                print("Data is", data.strip())
                message, broadcast = API.parse(data)
                if broadcast:
                    self.broadcast(message)
                else:
                    self.cast(client, message)
            except Exception as ex:
                self.delete_user_socket(client)
                break


    def delete_user_socket(self, client):
        for user in clients:
            if user["connection"] == client:
                clients.remove(user)
                print("Пользователь удалён", client)
                break


    def broadcast(self, message: str):
        message += "\n"
        for user in clients:
            user["connection"].send(message.encode())


    def cast(self, client, message):
        message += "\n"
        client.send(message.encode())


    def __init__(self):
        sock.bind(('localhost', 9090))
        sock.listen(10)
        print("Сервер запущен на сокете:", sock)


if __name__ == "__main__":
    sock = socket.socket()
    clients = []
    server = Server()

    #mysql = SQL
    #mysql.connect(mysql)
    #API.mysql = mysql
    #print(mysql.show_all_table(mysql, "users"))

    thread = threading.Thread(target=server.get_socket())
    thread.start()
    thread.join()
    sock.close()
