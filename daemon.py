#!/usr/bin/env python

import sys, os, base64
import time, random
import threading

path = os.path.abspath(os.path.dirname(__file__))
if not path in sys.path:
    sys.path.append(path)

yowsuppath=os.path.join(path,'./yowsup/src/')

if not yowsuppath in sys.path:
    sys.path.append(os.path.join(path,'./yowsup/src/'))

from Yowsup.connectionmanager import YowsupConnectionManager

DEFAULT_CONFIG = os.path.join(path,'config')


class Daemon:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connectionManager = YowsupConnectionManager()
        self.methodsInterface = self.connectionManager.getMethodsInterface()
        self.signalsInterface = self.connectionManager.getSignalsInterface()

        self.setup()

    def setup(self):
        self.connectionManager.setAutoPong(True)
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)
        self.signalsInterface.registerListener("receipt_messageDelivered", self.onMessageDelivered)

    def run(self):
        self.login()
        threading.Thread(target=self.sender_function).start()

        while True:
            pass

    def sender_function(self):
        while True:
            time.sleep(random.randint(5, 15))
            self.sendMessage('foo')

    def login(self):
        password = base64.b64decode(bytes(self.password.encode('utf-8')))
        self.methodsInterface.call("auth_login", (self.username, password))
        self.methodsInterface.call("presence_sendAvailable",)

    def onMessageDelivered(self, jid, messageId):
        print "Message was delivered successfully to %s" %jid
        self.methodsInterface.call("delivered_ack", (jid, messageId))

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


d = Daemon("34684070575", "xDkWCwXBOVcCLWpOM5I0oI1nu7w=")
d.run()
