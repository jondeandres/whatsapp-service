#!/usr/bin/env python

import sys, os, base64
import time, random
from  feeder import yowsup_patch
from feeder.zmq import receiver
from feeder.zmq import sender

from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.debugger import Debugger as YowsupDebugger

class Daemon:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connectionManager = YowsupConnectionManager()
        self.methodsInterface = self.connectionManager.getMethodsInterface()
        self.signalsInterface = self.connectionManager.getSignalsInterface()
        self.zmq_sender = sender.Sender()
        self.zmq_receiver = receiver.Receiver(self.methodsInterface)

        self.setup()

    def setup(self):
        yowsup_patch.patch(self.zmq_sender)
        YowsupDebugger.enabled=False

        self.connectionManager.setAutoPong(True)
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)
        self.signalsInterface.registerListener("receipt_messageDelivered", self.onMessageDelivered)
        self.signalsInterface.registerListener("message_received", self.onMessageReceived)
        self.signalsInterface.registerListener("group_messageReceived", self.onGroupMessageReceived)

    def run(self):
        self.login()
        self.zmq_receiver.bind()
        self.zmq_sender.connect()

    def login(self):
        password = base64.b64decode(bytes(self.password.encode('utf-8')))
        self.methodsInterface.call("auth_login", (self.username, password))
        self.methodsInterface.call("presence_sendAvailable",)

    def onMessageDelivered(self, jid, messageId):
        print "Message was delivered successfully to %s" %jid
        self.methodsInterface.call("delivered_ack", (jid, messageId))

    def messageACK(self, jid, messageId):
        print 'Sending ACK'
        self.methodsInterface.call('message_ack', (jid, messageId))

    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
        self.messageACK(jid, messageId)

    def onGroupMessageReceived(self, messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
        self.messageACK(jid, messageId)

    def onAuthSuccess(self, username):
        print "Authed %s" % username
        self.methodsInterface.call("ready")

    def onAuthFailed(self, username, err):
        print "Auth Failed!"

    def onDisconnected(self, reason):
        print "Disconnected because %s" %reason
        if reason=="dns": time.sleep(30)
        time.sleep(1)
        self.run()

    def sendMessage(self, text):
        self.methodsInterface.call("message_send", ("34635730544@s.whatsapp.net", "Hello World!"))


def run(username, password):
    daemon = Daemon(username, password)
    daemon.run()
