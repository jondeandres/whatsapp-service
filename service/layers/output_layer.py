from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_receipts.protocolentities    import *
from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.protocol_presence.protocolentities    import *
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_acks.protocolentities        import *
from yowsup.layers.protocol_ib.protocolentities          import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_contacts.protocolentities    import *
from yowsup.layers.protocol_profiles.protocolentities    import *
from yowsup.layers.protocol_chatstate.protocolentities   import *
from yowsup.layers.protocol_privacy.protocolentities     import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_profiles.protocolentities    import *

from service.zeromq.sender import Sender
from service import tree_dump

class OutputLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        import pdb;pdb.set_trace()

        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        import pdb;pdb.set_trace()

        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        self.toLower(receipt)

    def receive(self, tree_node):
        from service.daemon import zmq_sender

        print tree_node.toString()
        zmq_sender.send(tree_dump.dump(tree_node))

        self.toUpper(tree_node)
        import pdb;pdb.set_trace()

