import zmq
import threading
import json
import os, fnmatch
import random
import hashlib
import base64

class Receiver:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.hashes = whatsapp.hashes
        self.urls = whatsapp.urls
        self.context = whatsapp.context
        self.socket = self.context.socket(zmq.REP)

        self.thread = None

    def bind(self):
        self.socket.bind('tcp://*:5556')
        self.spawn_thread()

    def spawn_thread(self):
        self.thread = threading.Thread(target=self.recv)
        self.thread.start()
        self.thread.join

    def recv(self):
        while True:
            msg = json.loads(self.socket.recv())

            self.socket.send('received!')

            if msg['type'] == 'text':
                self.sendText(msg)
            elif msg['type'] == 'image':
                self.sendImage(msg)

    def sendText(self, msg):
        self.whatsapp.methodsInterface.call("message_send", (str(msg['jid']), str(msg['body'])))

    def find(self, path, glob):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, glob):
                matches.append(os.path.join(root, filename))
        return matches

    def sendImage(self, msg):
        files = self.find('/home/jon/wuaki/web/app/assets/images', '*.png')
        jid = msg['jid']
        path = files[random.randrange(len(files) -1) ]
        print path
        hsh, mtype, size = self.pictureData(path)
        self.hashes[hsh] = { 'jid': jid, 'path': path } # Redis

        # self.whatsapp.methodsInterface.call("typing_send",(jid,))
        print("Requesting Upload: hash %s mime_type %s size %d" %(hsh, mtype, size))
        self.whatsapp.methodsInterface.call("media_requestUpload", (hsh, mtype, size))

    def pictureData(self, path):
        if not os.path.isfile(path):
            print('File %s does not exists' % path)
            return 1

        mtype = 'image'
        sha1 = hashlib.sha256()
        fp = open(path, 'rb')

        try:
            sha1.update(fp.read())
            hsh = base64.b64encode(sha1.digest())
            size = os.path.getsize(path)

        finally:
            fp.close()
            return (hsh, mtype, size)
