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

    def disconnectClient(self):
        socket = self.sender()
        self.sendAll(u"<em>Déconnexion de %s</em>" % self.clients[socket]["pseudo"])
        self.clients.pop(socket)

    def readData(self):
        socket = self.sender()
        line = socket.readLine().data()
        cmd, value = line.split(" ", 1)
        if cmd == "login":
            self.sendAll(u"<em>Connexion de %s</em>" % value.decode("utf-8"))
            self.clients[socket]["pseudo"] = value.decode("utf-8")
        elif cmd == "say":
            message = "<%s> : %s" % (self.clients[socket]["pseudo"], value.decode("utf-8"))
            self.sendAll(message)

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
