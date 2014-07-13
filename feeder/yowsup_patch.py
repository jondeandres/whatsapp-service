from Yowsup.connectionmanager import ReaderThread
from feeder.zmq import sender

ReaderThread.oldParseMessage = ReaderThread.parseMessage

def parseMessage(self, messageNode):
    s = sender.Sender()
    s.deliver(messageNode)
    self.oldParseMessage(messageNode)

def patch():
    ReaderThread.parseMessage = parseMessage

