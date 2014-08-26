from Yowsup.Media.uploader import MediaUploader 
import os
import Image
import StringIO
import base64
from sys import stdout

class Media:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.hashes = whatsapp.hashes
        self.urls = whatsapp.urls

    def onmedia_uploadRequestSuccess(self, hsh, url, resumeFrom):
        print("Request Succ: hash: %s url: %s resume: %s"%(hsh, url, resumeFrom))

        data = self.whatsapp.hashes[hsh]
        self.whatsapp.urls[os.path.basename(url)] = hsh
        self.uploadImage(data, url)

    def onmedia_uploadRequestDuplicate(self, hsh, url):
        print("Request Dublicate: hash: %s url: %s "%(hsh, url))

        data = self.whatsapp.hashes[hsh]
        self.whatsapp.urls[url] = hsh
        self.uploadImage(data, url)

    def onmedia_uploadRequestFailed(self, _hash):
        print("Request Fail: hash: %s"%(_hash))

    def onUploadSuccess(self, url):
        print("Upload Succ: url: %s "%( url))

        os.path.basename(url).split('.')[0]
        hsh = self.whatsapp.urls[os.path.basename(url).split('.')[0]]

        data = self.whatsapp.hashes[hsh]
        jid = data['jid']
        path = data['path']

        statinfo = os.stat(path)
        name = os.path.basename(path)
        self.whatsapp.methodsInterface.call("message_imageSend", (jid, url, name, str(statinfo.st_size), self.createThumb(path)))
        # os.remove(path)

    def createThumb(self, path):
        try:
            size = 100, 100
            im = Image.open(path)
            im.thumbnail(size, Image.ANTIALIAS)
            output = StringIO.StringIO()
            im.save(output,"JPEG")
            contents = output.getvalue()
            output.close()
            return base64.b64encode(contents)
        except IOError:
            print "cannot create thumbnail for '%s'" % path

    def onError(self):
        print("Upload Fail:")

    def onProgressUpdated(self, progress):
        stdout.write("\r Progress: %s" % progress)

    def uploadImage(self, data, url):
        path = data['path']
        jid = data['jid']
        uploader = MediaUploader(jid, self.whatsapp.username, self.onUploadSuccess, self.onError, self.onProgressUpdated)

        print 'Sending %s to %s' % (path, jid)
        uploader.upload(path, url)
