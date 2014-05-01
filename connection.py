#!/usr/bin/env python
# -*- coding: utf-8 -*-

import client
from PySide import QtCore, QtGui, QtNetwork

class Connexion(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Connexion, self).__init__(parent)

        serverLabel = QtGui.QLabel("Serveur : ")
        portLabel = QtGui.QLabel("Port : ")

        self.serverInput = QtGui.QLineEdit()
        self.portInput = QtGui.QLineEdit()
        self.pseudo = QtGui.QLineEdit()

        quitButton = QtGui.QPushButton("Quitter")
        quitButton.setAutoDefault(False)
        connectButton = QtGui.QPushButton("Connexion")

        quitButton.clicked.connect(self.close)

        connectButton.clicked.connect(self.connexion)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(connectButton)
        buttonLayout.addWidget(quitButton)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(serverLabel, 0, 0)
        mainLayout.addWidget(self.serverInput, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portInput, 1, 1)
        mainLayout.addWidget(QtGui.QLabel("Pseudo : "), 2, 0)
        mainLayout.addWidget(self.pseudo, 2, 1)
        mainLayout.addLayout(buttonLayout, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        #Network
        self.tcpSocket = QtNetwork.QTcpSocket(self)
        self.tcpSocket.error.connect(self.displayError)

        self.setWindowTitle("Connexion")

    def connexion(self):
        self.tcpSocket.connectToHost(self.serverInput.text(), int(self.portInput.text()))
        c = client.Client(self.tcpSocket, self.pseudo.text())
        self.close()
        c.exec_()

    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    connexion = Connexion()
    sys.exit(connexion.exec_())

