import time
import io
import os
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
def create_qrcode(data):
    timestamp = int(time.time())
    img = qrcode.make(data)
    file_path = os.path.join("/root/pho",f"{timestamp}.PNG")
    img.save(file_path)
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        photo_data = output.getvalue()
    return photo_data
def read_qrcode(photo):
    result = decode(photo)
    return result