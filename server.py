import socket
import threading

host = socket.gethostbyname(socket.gethostname())
port = 8080  # закомитеть эту строчку для ввода порта
# port = input("Введите порт: ")  # Разкомитеть строчку для ввода порта
address = (host, port)
socket_list = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET ожидает кортеж
byt = 2048
FORMAT = "utf8"
list_of_clients = []
members = {}
name = ""

socket_list.append(server)

log = open("log", "a")

# bind socket

try:
    server.bind((host, port))
    print("Server has been binded")
except socket.error as message:
    print(message)


def handle_client(conn, addr):  # создает клиентский поток
    user_connect = ("[NEW CONNECTION] {} - {} connected.".format(addr[0], members[addr]))
    print("[NEW CONNECTION] {} - {} connected.".format(addr[0], members[addr]))
    conn.send('Welcome to the Server!'.encode(FORMAT))
    broadcast(user_connect, conn)  # Отправить один раз, когда пользователь присоединяется
    connected = True
    try:

        while connected:
            msg = conn.recv(byt).decode(FORMAT)  # получить сообщение
            if msg:
                print(f"<{addr[0]} - {members[addr]}> {msg}")
                log.write(f"<{addr[0]} - {members[addr]}> {msg}")
                user_msg = f"<{addr[0]} - {members[addr]}> {msg}"
                broadcast(user_msg, conn)
            else:
                print("<" + str(members[addr]) + "> " + "--HAS DISCONNECTED--")
                remove(conn)
                print("List of clients length: " + str(len(list_of_clients)))
                break

    except:
        print("Some connection error")


def broadcast(msg, conn):
    for client in list_of_clients:
        if client != conn:
            try:
                client.send(msg.encode(FORMAT))
            except:
                client.close()
                remove(client)


def start():
    server.listen()
    print(f"[LISTENING]Server is listening on {host}")
    accept_connections = True
    while accept_connections:
        conn, addr = server.accept()
        name = conn.recv(byt).decode(FORMAT)
        list_of_clients.append(conn)
        members[addr] = ""
        if name in members.values():
            conn.send("Username already taken!".encode(FORMAT))
            del members[addr]
            list_of_clients.remove(conn)
            conn.close()
            continue
        else:
            members[addr] = name
            print("List of clients length: " + str(len(list_of_clients)))
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


def remove(connection):
    if connection in list_of_clients:
        connection.close()
        list_of_clients.remove(connection)


print("[STARTING] Server is starting...")
start()
