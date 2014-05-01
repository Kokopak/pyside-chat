#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtNetwork

class Client(QtGui.QDialog):
    def __init__(self, socket, pseudo, parent=None):
        super(Client, self).__init__(parent)

        self.mainLayout = QtGui.QGridLayout()
        self.messages = QtGui.QTextEdit()
        self.messages.setReadOnly(True)
        self.message = QtGui.QLineEdit()

        self.sendMessage = QtGui.QPushButton("Envoyer le message")
        self.sendMessage.clicked.connect(self.send)

        self.messageLayout = QtGui.QHBoxLayout()
        self.messageLayout.addWidget(QtGui.QLabel("Message : "))
        self.messageLayout.addWidget(self.message)
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
        instr = QtCore.QDataStream(self.socket)
        if self.blockSize == 0:
            if self.socket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()
        if self.socket.bytesAvailable() < self.blockSize:
            return

        message = instr.readString()
        self.messages.append(message)
        self.blockSize = 0


    def send(self, message=None):
        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.writeUInt16(0)
        if message == None:
            outstr.writeString("<%s>: %s" % (self.pseudo, self.message.text()))
        else:
            outstr.writeString("%s" % message)
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)

        self.socket.write(block)

        self.message.clear()
        self.message.setFocus()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
