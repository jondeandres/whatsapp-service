import urllib2
import tempfile
import time
import os, fnmatch
import random
import hashlib
import base64
from feeder.senders.base import Base

class UrlImage(Base):
    def __init__(self, whatsapp, msg):
        self.temp_file = None
        self.url = msg['url']
        super(UrlImage, self).__init__(whatsapp, msg)

    def prepare(self):
        n = random.randrange(1000000)
        self.temp_file = open('/tmp/' + str(n) + '.jpg', 'wb')
        image = urllib2.urlopen(self.url)
        self.temp_file.write(image.read())
        self.temp_file.close()

    def performSend(self):
        self.sendImage()


    def sendImage(self):
        path = self.temp_file.name.encode('latin1')
        hsh, mtype, size = self.pictureData(path)

        self.whatsapp.hashes[hsh] = { 'jid': self.jid, 'path': path } # Redis
        print("Requesting Upload: hash %s mime_type %s size %d" %(hsh, mtype, size))
        self.interface.call("media_requestUpload", (hsh, mtype, size))

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
