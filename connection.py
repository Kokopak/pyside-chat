#!/usr/bin/env python
# -*- coding: utf-8 -*-

import client
import time
from PySide import QtCore, QtGui, QtNetwork

class Connexion(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Connexion, self).__init__(parent)

        serverLabel = QtGui.QLabel("Serveur : ")
        portLabel = QtGui.QLabel("Port : ")

        self.serverInput = QtGui.QLineEdit()
        self.serverInput.setText("localhost")
        self.portInput = QtGui.QLineEdit()
        self.portInput.setText("8080")
        self.pseudo = QtGui.QLineEdit()
        self.pseudo.setText("Coco")

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
        self.error = False

        self.setWindowTitle("Connexion")

    def connexion(self):
        self.tcpSocket.connectToHost(self.serverInput.text(), int(self.portInput.text()))
        #Attend jusqu'a ce que le socket soit connecté
        if self.tcpSocket.waitForConnected(1000):
            c = client.Client(self.tcpSocket, self.pseudo.text())
            self.close()
            c.exec_()

    def displayError(self, socketError):
        self.error = True
        QtGui.QMessageBox.information(self, "Connexion",
                "L'erreur suivant s'est produite : %s." % self.tcpSocket.errorString())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    connexion = Connexion()
    sys.exit(connexion.exec_())

