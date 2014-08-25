import urllib2
import tempfile
import time

class UrlImage:
    def __init__(self, whatsapp, msg):
        self.jid = msg['jid']
        self.url = msg['url']
        self.whatsapp = whatsapp
        self.interface = whatsapp.methodsInterface
        self.temp_file = None

    def prepare(self):
        self.temp_file = tempfile.NamedTemporaryFile('wb')
        image = urllib2.urlopen(self.url)
        print self.temp_file.name
        self.temp_file.write(image.read())


    def send(self):
        print('About to send %s to %s' % (self.url, self.jid))
