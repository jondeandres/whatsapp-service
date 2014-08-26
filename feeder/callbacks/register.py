from feeder.callbacks import signals
from feeder.callbacks import media

def register(whatsapp):
  signalsInterface = whatsapp.signalsInterface
  signalingCallbacks = signals.Signals(whatsapp)
  mediaCallbacks = media.Media(whatsapp)

  signalsInterface.registerListener("auth_success", signalingCallbacks.onAuthSuccess)
  signalsInterface.registerListener("auth_fail", signalingCallbacks.onAuthFailed)
  signalsInterface.registerListener("disconnected", signalingCallbacks.onDisconnected)
  signalsInterface.registerListener("receipt_messageDelivered", signalingCallbacks.onMessageDelivered)
  signalsInterface.registerListener("message_received", signalingCallbacks.onMessageReceived)
  signalsInterface.registerListener("group_messageReceived", signalingCallbacks.onGroupMessageReceived)

  signalsInterface.registerListener("media_uploadRequestSuccess", mediaCallbacks.onmedia_uploadRequestSuccess)
  signalsInterface.registerListener("media_uploadRequestFailed", mediaCallbacks.onmedia_uploadRequestFailed)
  signalsInterface.registerListener("media_uploadRequestDuplicate", mediaCallbacks.onmedia_uploadRequestDuplicate)

