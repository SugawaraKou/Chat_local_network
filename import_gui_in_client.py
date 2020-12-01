import socket
import select
import sys
from PyQt5 import QtWidgets
from Chat_local_network import gui


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.build_handlers()

    def client(self):
        # establish socket
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.plainTextEdit.appendPlainText("Hello Word")

        if len(sys.argv) != 3:
            self.plainTextEdit.appendPlainText("Please enter: scriptname, IP address, port number")

        IP = str(input("IP server: "))
        self.plainTextEdit.appendPlainText("IP server: ")
        port = int(input("PORT server: "))
        self.plainTextEdit.appendPlainText("PORT server: ")

        name = str(input("Please enter your name: "))
        self.plainTextEdit.appendPlainText("Please enter your name: ")

        # connect to server
        try:
            server_sock.connect((IP, port))
            self.plainTextEdit.appendPlainText("Trying to connect...")
        except:
            self.plainTextEdit.appendPlainText("Can't connect to server")
            sys.exit()

        server_sock.send(name.encode("utf8"))
        connected = True
        data = server_sock.recv(2048).decode("utf8")  # welcome message
        self.plainTextEdit.appendPlainText("<" + IP + ">: " + data)
        while connected:
            socket_list = [sys.stdin, server_sock]
            try:

                read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
                for sock in read_sockets:
                    if sock == server_sock:
                        data = server_sock.recv(2048).decode("utf8")  # чужие сообщения
                        self.plainTextEdit.appendPlainText(data)
                        if len(data) == 0:
                            # self.plainTextEdit.appendPlainText()
                            print("You have disconnected.")
                            sys.exit()
                    else:
                        my_msg = sys.stdin.readline()  # мои сообщения
                        self.plainTextEdit.appendPlainText(my_msg)
                        server_sock.send(my_msg.encode("utf8"))
            except:
                self.plainTextEdit.appendPlainText("You have disconnected manually")
                connected = False

        self.plainTextEdit.appendPlainText("You have disconnected ")

    def build_handlers(self):
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.lineEdit.clear()
        self.client()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


main()