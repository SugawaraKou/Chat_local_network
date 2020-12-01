import socket
import sys
import select

import sys
from PyQt5 import QtWidgets
from Chat_local_network import gui

class connect():
    def __init__(self, app_window):
        self.window = app_window

    def connect(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if len(sys.argv) != 3:
            self.plainTextEdit.appendPlainText("Please enter: scriptname,")

        IP = "192.168.88.8"
        port = "8080"
        name = str(self.lineEdit.text())
        # connect to server
        try:
            server_sock.connect((IP, port))
            self.pconnectlainTextEdit.appendPlainText("Trying to connect...")
        except:
            self.plainTextEdit.appendPlainText("Can't connect to server")
            sys.exit()

        server_sock.send(name.encode("utf8"))
        connected = True
        data = server_sock.recv(2048).decode("utf8")  # welcome message
        self.plainTextEdit.appendPlainText("<" + IP + ">: " + data)

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
        self.init_handlers()

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_list = [sys.stdin, server_sock]
        try:
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            for sock in read_sockets:
                if sock == server_sock:
                    data = server_sock.recv(2048).decode("utf8")  # чужие сообщения
                    self.plainTextEdit.appendPlainText(data)
                    if len(data) == 0:
                        self.plainTextEdit.appendPlainText("You have disconnected.")
                        sys.exit()
                else:
                    message = self.lineEdit.text()
                    #my_msg = sys.stdin.readline()  # мои сообщения
                    server_sock.send(message.encode("utf8"))
                    self.plainTextEdit.appendPlainText(message)
                    self.lineEdit.clear()
        except:
            self.plainTextEdit.appendPlainText("You have disconnected manually")
            connected = False
            self.closeEvent()

def main():

    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    connect(window)
    app.exec_()


main()