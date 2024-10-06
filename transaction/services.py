import qrcode
import hashlib
import json
import datetime
import base64
import os
path = os.path.join(os.getcwd() + "\\transaction\\client_qr_code")


def generate_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def generateQRImage(data, token):
    # print(qrcode.__version__)
    # print(dir(qrcode))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image()

    # print(os.listdir())
    img.save(f"{path}\\{token}.png")


def convert_image_to_base64(image_path="./client_qr_code"):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string


def convert_base64_to_image(base64_string, output_file):
    image_data = base64.b64decode(base64_string)
    with open(output_file, "wb") as file:
        file.write(image_data)


# convert_base64_to_image(base64_string, "output_image.png")

def generateQrCode(data, seconds=40):
    data["secret_code"] = datetime.datetime.now()
    token = generate_hash(str(data))
    info = {
        "token": token,
        "expire": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    }
    generateQRImage(token, token)
    return info, convert_image_to_base64(f"{path}\\{token}.png")
