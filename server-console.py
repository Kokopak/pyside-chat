#!/usr/bin/env python
#-*-coding: utf-8-*-

import random

from PySide import QtCore, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.newConnection.connect(self.newClient)

        self.clients = []

    def newClient(self):
        client = self.nextPendingConnection()
        client.readyRead.connect(self.readData)
        client.disconnected.connect(self.disconnectClient)
        self.clients.append(client)
        print "Y'a dun nouveau"

    def disconnectClient(self):
        self.sendAll(u"<em>Déconnexion d'un client</em>")

    def readData(self):
        print "Recu !!!"
        socket = self.sender()
        line = socket.readLine().data()
        self.sendAll(line.decode("utf-8"))

    def sendAll(self, message):
        for c in self.clients:
            c.write(message.encode("utf-8"))

if __name__ == '__main__':

    import sys
    app = QtCore.QCoreApplication(sys.argv)
    serv = Server()
    port = 8080
    serv.listen(port=port)
    print "Le serveur tourne sur le port %d" % port
    sys.exit(app.exec_())
