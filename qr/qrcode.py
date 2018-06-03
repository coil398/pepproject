from pyzbar.pyzbar import decode
from PIL import Image
import subprocess


image = './qrcode.png'

data = decode(Image.open(image))

url = data[0][0].decode('utf-8')

data = subprocess.check_output(['python3', 'crawl.py', url])
data = subprocess.check_output(['python3', 'guide.py', data])
print(data.decode('utf-8'))
