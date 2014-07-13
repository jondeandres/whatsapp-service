from Yowsup.connectionmanager import ReaderThread
from feeder.zmq import sender

ReaderThread.oldParseMessage = ReaderThread.parseMessage

def parseMessage(self, messageNode):
    ReaderThread.zmq_sender.send(messageNode.toString())
    self.oldParseMessage(messageNode)

def patch(zmq_sender):
    ReaderThread.parseMessage = parseMessage
    ReaderThread.zmq_sender = zmq_sender

