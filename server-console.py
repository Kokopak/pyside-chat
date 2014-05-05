#!/usr/bin/env python
#-*-coding: utf-8-*-

import random
from PySide import QtCore, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.newConnection.connect(self.newClient)

        self.clients = {}

    def newClient(self):
        client = self.nextPendingConnection()
        client.readyRead.connect(self.readData)
        client.disconnected.connect(self.disconnectClient)
        self.clients[client] = {}
        self.clients[client]["pseudo"] = u"guest-%d" % random.randint(1, 1000)

    def disconnectClient(self):
        socket = self.sender()
        self.sendAll(u"<em>Déconnexion de %s</em>" % self.clients[socket]["pseudo"])
        self.clients.pop(socket)

    def readData(self):
        socket = self.sender()
        line = socket.readLine().data()
        cmd, value = line.split(" ", 1)
        value = value.decode("utf-8")
        if cmd == "login":
            if self.pseudoExist(value):
                pseudo = self.clients[socket]["pseudo"]
                socket.write(u"<em>Pseudo déja pris. Assignement automatique...</em>".encode("utf-8"))
            else:
                pseudo = value
                self.clients[socket]["pseudo"] = pseudo
            self.sendAll(u"<em>Connexion de %s</em>" % pseudo)
        elif cmd == "say":
            message = "<%s> : %s" % (self.clients[socket]["pseudo"], value)
            self.sendAll(message)

    def sendAll(self, message):
        for c in self.clients:
            c.write(message.encode("utf-8"))

    def pseudoExist(self, pseudo):
        for c in self.clients:
            if pseudo == self.clients[c]["pseudo"]:
                return True

if __name__ == '__main__':

    import sys
    app = QtCore.QCoreApplication(sys.argv)
    serv = Server()
    port = 8080
    serv.listen(port=port)
    print "Le serveur tourne sur le port %d" % port
    sys.exit(app.exec_())
