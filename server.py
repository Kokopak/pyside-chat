#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtNetwork

class Server(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton("Quitter")
        quitButton.setAutoDefault(False)

        quitButton.clicked.connect(self.close)

        self.client = None
        self.clients = []

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        #Network
        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen(port=8080):
            QtGui.QMessageBox.critical(self, "Serveur", "Probleme")
            self.close()
            return
        self.blockSize = 0
        self.tcpServer.newConnection.connect(self.newClient)
        statusLabel.setText("Le serveur tourne sur le port : %d" % self.tcpServer.serverPort())

        self.setWindowTitle("Serveur")

    def newClient(self):
        self.client = self.tcpServer.nextPendingConnection()
        self.clients.append(self.client)
        self.client.readyRead.connect(self.readData)

    def readData(self):
        socket = self.sender()

        instr = QtCore.QDataStream(socket)
        if self.blockSize == 0:
            if socket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()
        if socket.bytesAvailable() < self.blockSize:
            return

        message = instr.readString()
        try:
            message = str(message, encoding='ascii')
        except TypeError:
            pass

        self.sendAll(message)
        self.blockSize = 0

    def sendAll(self, message):
        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.writeUInt16(0)
        outstr.writeString(message)
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)

        for c in self.clients:
            c.write(block)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())

