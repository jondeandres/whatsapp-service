from Yowsup.connectionmanager import ReaderThread
from Yowsup.connectionmanager import YowsupConnectionManager
from feeder.zmq import sender
import tree_dump

ReaderThread.oldParseMessage = ReaderThread.parseMessage

def parseMessage(self, messageNode):
    messageNode.attributes['to'] = self.username
    ReaderThread.zmq_sender.send(tree_dump.dump(messageNode))
    self.oldParseMessage(messageNode)


def setUsername(self, username):
    self.readerThread.username = username

def patch(zmq_sender):
    ReaderThread.parseMessage = parseMessage
    ReaderThread.zmq_sender = zmq_sender
    YowsupConnectionManager.setUsername = setUsername
