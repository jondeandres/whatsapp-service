#!/usr/bin/env python

import sys, os, base64
import time, random
from  feeder import yowsup_patch
from feeder import callbacks
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
        self.callbacks = callbacks.Callbacks(self)

        self.setup()

    def setup(self):
        yowsup_patch.patch(self.zmq_sender)

        YowsupDebugger.enabled=False
        self.connectionManager.setAutoPong(True)
        self.signalsInterface.registerListener("auth_success", self.callbacks.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.callbacks.onAuthFailed)
        self.signalsInterface.registerListener("disconnected", self.callbacks.onDisconnected)
        self.signalsInterface.registerListener("receipt_messageDelivered", self.callbacks.onMessageDelivered)
        self.signalsInterface.registerListener("message_received", self.callbacks.onMessageReceived)
        self.signalsInterface.registerListener("group_messageReceived", self.callbacks.onGroupMessageReceived)

    def run(self):
        self.login()
        self.zmq_receiver.bind()
        self.zmq_sender.connect()

    def login(self):
        password = base64.b64decode(bytes(self.password.encode('utf-8')))
        self.methodsInterface.call("auth_login", (self.username, password))
        self.methodsInterface.call("presence_sendAvailable",)
        self.connectionManager.setUsername(self.username)

def run(username, password):
    daemon = Daemon(username, password)
    daemon.run()
