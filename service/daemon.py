import zmq
from service.stack import Stack
from service.zeromq.sender import Sender

zmq_context = zmq.Context()
zmq_sender = None

def run(number, password):
    global zmq_context, zmq_sender

    zmq_sender = Sender(zmq_context)
    zmq_sender.connect()

    stack = Stack((number, password))
    stack.start()

