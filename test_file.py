
import sys
from PyQt5 import QtWidgets
from Chat_local_network import gui


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.build_handlers()

    def build_handlers(self):
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.lineEdit.clear()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


main()