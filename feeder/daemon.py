#!/usr/bin/env python

import sys, os, base64
import time, random
import zmq as libzmq
from redis import Redis
from feeder import yowsup_patch
from feeder.contacts import Contacts
from feeder.callbacks import register as callbacks
from feeder.zeromq import receiver
from feeder.zeromq import sender
from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.debugger import Debugger as YowsupDebugger

_instance = None

class Daemon:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashes = {}
        self.urls = {}
        self.context = libzmq.Context()
        self.connectionManager = YowsupConnectionManager()
        self.methodsInterface = self.connectionManager.getMethodsInterface()
        self.signalsInterface = self.connectionManager.getSignalsInterface()
        self.zmq_connected = False
        self.redis = Redis()
        self.contacts = Contacts(self)
        self.zmq_sender = sender.Sender(self)
        self.zmq_receiver = receiver.Receiver(self)

        self.setup()

    @staticmethod
    def instance():
        global _instance
        return _instance

    def setup(self):
        yowsup_patch.patch(self.zmq_sender)

        YowsupDebugger.enabled=False
        self.connectionManager.setAutoPong(True)
        callbacks.register(self)

    def run(self):
        self.login()
        if self.zmq_connected is False:
            self.zmq_connected = True
            self.zmq_receiver.bind()
            self.zmq_sender.connect()

    def login(self):
        password = base64.b64decode(bytes(self.password.encode('utf-8')))
        self.methodsInterface.call("auth_login", (self.username, password))
        self.connectionManager.setUsername(self.username)



def run(username, password):
    global _instance

    if _instance is None:
        _instance = Daemon(username, password)

    _instance.run()

