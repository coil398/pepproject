# coding=utf-8
import sys
import time
sys.path.append('./../pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages')
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from optparse import OptionParser
import subprocess
import multiprocessing


class QRCodeReaderModule(ALModule):

    def __init__(self, name):
        ALModule.__init__(self, name)

        self.tts = ALProxy('ALTextToSpeech')

        global memory
        memory = ALProxy('ALMemory')
        memory.subscribeToEvent('BarcodeReader/BarcodeDetected', 'QRCodeReader', 'onQRCodeDetected')
        time.sleep(5)
        print('QRCodeReaderModule is ready.')

    def crawl_doorkeeper(self, url):
        output = subprocess.check_output(['python3', 'crawl.py', url])
        return output

    def guide_guest(self, data):
        output = subprocess.check_output(['python3', 'guide.py', data])
        print(output.decode('utf-8'))
        self.tts.say(output)
        return output

    def onQRCodeDetected(self, *args):
        print('A QR code is detected.')
        memory.unsubscribeToEvent('BarcodeReader/BarcodeDetected', 'QRCodeReader')
        data = memory.getData('BarcodeReader/BarcodeDetected')
        url = data[0][0] # get the url from the data.
        data = self.crawl_doorkeeper(url)
        self.guide_guest(data)
        time.sleep(5)
        memory.subscribeToEvent('BarcodeReader/BarcodeDetected', 'QRCodeReader', 'onQRCodeDetected')


class TakeAndShowPics:

    def __init__(self, ip, port):
        self._recordFolder = '/home/nao/recordings/cameras/'
        self._fileName = 'image'
        self._photo = './photo/image.jpg'
        self._camera = ALProxy('ALPhotoCapture')
        self._tablet = ALProxy('ALTabletService')
        self._ip = ip
        self._port= port
        self.setParameters()

    def setParameters(self):
        self._camera.setResolution(2)
        self._camera.setCameraID(0)
        self._camera.setPictureFormat('jpg')

    def start(self):
        while True:
            self._camera.takePicture(self._recordFolder, self._fileName)
            self._tablet.showImage(self._photo)
            time.sleep(1)


def main():
    parser = OptionParser()
    parser.add_option('--ip', help='IP address of pepper.', dest='ip')
    parser.add_option('--port', help='port.', dest='port', type='int')
    parser.set_defaults(port=9559)

    opts, args = parser.parse_args()
    ip = opts.ip
    port = opts.port

    myBroker = ALBroker('myBroker', '0.0.0.0', 0, ip, port)

    global QRCodeReader
    QRCodeReader = QRCodeReaderModule('QRCodeReader')

    # takeAndShowPics = TakeAndShowPics()
    # p = multiprocessing.Process(target=takeAndShowPics.start)
    # p.start()
    takeAndShowPics = TakeAndShowPics(ip, port)
    takeAndShowPics.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print('Interrupted.')
        myBroker.shutdown()
        sys.exit()


if __name__ == '__main__':
    main()
