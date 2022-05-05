import json
import base64


def dummy_fun():
    data = {}
    with open('C:/Users/Ana/Desktop/Ana/Dodatno/Lumen/pic.jpg', mode='rb') as file:
        img = file.read()
    data['img'] = base64.encodebytes(img).decode('utf-8')
    image_json = json.dumps(data)

    result = {"state": {"coordinates": (70, 50), "image": image_json}}
    print(result)


