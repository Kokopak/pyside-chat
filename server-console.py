#!/usr/bin/env python
#-*-coding: utf-8-*-

import random

from PySide import QtCore, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        self.clients = []
        self.newConnection.connect(self.newClient)
        self.blockSize = 0

    def newClient(self):
        client = self.nextPendingConnection()
        self.clients.append(client)
        client.readyRead.connect(self.readData)

    def readData(self):
        socket = self.sender()
        print "Reçu paquet de {0} :".format(socket)

        instr = QtCore.QDataStream(socket)
        if self.blockSize == 0:
            if socket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()
        if socket.bytesAvailable() < self.blockSize:
            return

        message = instr.readString()
        print message
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

if __name__ == '__main__':

    import sys
    app = QtCore.QCoreApplication(sys.argv)
    serv = Server()
    port = 8080
    serv.listen(port=port)
    print "Le serveur tourne sur le port %d" % port
    sys.exit(app.exec_())

