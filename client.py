#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtGui, QtNetwork

class Client(QtGui.QDialog):
    def __init__(self, socket, pseudo, parent=None):
        super(Client, self).__init__(parent)

        self.mainLayout = QtGui.QGridLayout()
        self.messages = QtGui.QTextEdit()
        self.messages.setReadOnly(True)
        self.messageLineEdit = QtGui.QLineEdit()

        self.sendMessage = QtGui.QPushButton("Envoyer le message")
        self.sendMessage.clicked.connect(self.sendClick)

        self.messageLayout = QtGui.QHBoxLayout()
        self.messageLayout.addWidget(QtGui.QLabel("Message : "))
        self.messageLayout.addWidget(self.messageLineEdit)
        self.messageLayout.addWidget(self.sendMessage)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addLayout(self.messageLayout)

        self.setLayout(self.mainLayout)

        #Network
        self.socket = socket
        self.socket.readyRead.connect(self.readData)
        self.blockSize = 0
        self.pseudo = pseudo
        self.send("<em>Connexion de %s</em>" % self.pseudo)

        self.setWindowTitle("<%s>" % self.pseudo)


    def readData(self):
        message = self.socket.readLine().data()
        self.messages.append(message.decode("utf-8"))

    def send(self, message):
        self.socket.write(message.encode("utf-8"))

    def sendClick(self):
        message = "<%s> : %s " % (self.pseudo, self.messageLineEdit.text())
        #self.socket.write(message.encode("utf-8"))
        self.send(message)
        self.messageLineEdit.clear()
        self.messageLineEdit.setFocus()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
