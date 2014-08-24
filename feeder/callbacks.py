import time
import daemon

class Callbacks:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.signalsInterface = whatsapp.signalsInterface

    def register(self):
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)
        self.signalsInterface.registerListener("receipt_messageDelivered", self.onMessageDelivered)
        self.signalsInterface.registerListener("message_received", self.onMessageReceived)
        self.signalsInterface.registerListener("group_messageReceived", self.onGroupMessageReceived)

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
        daemon.Daemon.instance().run()
