import time

class Signals:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp

    def onMessageDelivered(self, jid, messageId):
        print "Message was delivered successfully to %s" %jid
        self.whatsapp.methodsInterface.call("delivered_ack", (jid, messageId))

    def messageACK(self, jid, messageId):
        self.whatsapp.methodsInterface.call('message_ack', (jid, messageId))

    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
        self.messageACK(jid, messageId)

    def onGroupMessageReceived(self, messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
        self.messageACK(jid, messageId)

    def onAuthSuccess(self, username):
        print "Authed %s" % username
        self.whatsapp.methodsInterface.call("ready")

    def onAuthFailed(self, username, err):
        print "Auth Failed!"

    def onDisconnected(self, reason):
        print "Disconnected because %s" %reason
        if reason=="dns": time.sleep(30)
        time.sleep(1)
        self.whatsapp.run()
