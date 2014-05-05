#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtGui, QtNetwork

class Client(QtGui.QDialog):
    def __init__(self, parent=None):
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

        self.serverInput = QtGui.QLineEdit()
        self.serverInput.setText("localhost")
        self.portInput = QtGui.QLineEdit()
        self.portInput.setText("8080")
        self.pseudoInput = QtGui.QLineEdit()
        self.pseudoInput.setText("Coco")
        self.connectButton = QtGui.QPushButton("Connexion")
        self.connectButton.clicked.connect(self.connection)

        self.connectionLayout = QtGui.QGridLayout()
        self.connectionLayout.addWidget(QtGui.QLabel("Serveur :"), 0, 0)
        self.connectionLayout.addWidget(self.serverInput, 0, 1)
        self.connectionLayout.addWidget(QtGui.QLabel("Port : "), 0, 2)
        self.connectionLayout.addWidget(self.portInput, 0, 2)
        self.connectionLayout.addWidget(QtGui.QLabel("Pseudo : "), 1, 0)
        self.connectionLayout.addWidget(self.pseudoInput, 1, 1)
        self.connectionLayout.addWidget(self.connectButton, 1, 2)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addLayout(self.messageLayout)
        self.mainLayout.addLayout(self.connectionLayout)

        self.setLayout(self.mainLayout)

        #Network
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.readyRead.connect(self.readData)
        self.socket.error.connect(self.displayError)

    def closeEvent(self, event):
        self.socket.disconnectFromHost()

    def connection(self):
        self.socket.connectToHost(self.serverInput.text(), int(self.portInput.text()))
        if self.socket.waitForConnected(1000):
            self.pseudo = self.pseudoInput.text()
            self.send("<em>Connexion de %s</em>" % self.pseudo)
            self.connectButton.setEnabled(False)
            self.setWindowTitle("<%s>" % self.pseudo)

    def readData(self):
        message = self.socket.readLine().data()
        self.messages.append(message.decode("utf-8"))

    def send(self, message):
        self.socket.write(message.encode("utf-8"))

    def sendClick(self):
        message = "<%s> : %s " % (self.pseudo, self.messageLineEdit.text())
        print type(message)
        self.send(message)
        self.messageLineEdit.clear()
        self.messageLineEdit.setFocus()

    def displayError(self):
        QtGui.QMessageBox.information(self, "Connexion", "Erreur de connexion")


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
