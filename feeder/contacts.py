from Yowsup.ConnectionIO.protocoltreenode import ProtocolTreeNode
from Yowsup.Contacts.contacts import WAContactsSyncRequest
from datetime import datetime

class Contacts:
    def __init__(self, whatsapp):
        self.username = whatsapp.username
        self.password = whatsapp.password
        self.connection = whatsapp.connectionManager
        self.redis = whatsapp.redis
        self.set = self.username + ':contacts'

    def addContact(self, number):
        if self.redis.sismember(self.set, number) is False:
            self.addContactRequest(number)
            self.redis.sadd(self.set, number)

    def addContactRequest(self, jid):
        the_id = self.connection.makeId("sync_")

        number = jid.split("@")[0]
        userNode = ProtocolTreeNode("user", {}, None, number.encode('latin1'))

        syncNode = ProtocolTreeNode("sync",
                                    {
                                        "context": "background",
                                        "index": "0",
                                        "mode": "delta",
                                        "last": "true",
                                        "sid": datetime.utcnow().strftime("%s").encode('latin1')
                                    },
                                    [userNode])

        iqNode = ProtocolTreeNode("iq",
                                {
                                    "id": the_id,
                                    "type": "get",
                                    "to": self.username,
                                    "xmlns": "urn:xmpp:whatsapp:sync"
                                },
                                [syncNode])

        self.connection._writeNode(iqNode)
