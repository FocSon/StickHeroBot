import numpy
import time
from ppadb.client import Client
from PIL import Image


def nb_pix_btw(last_line):
    flag = False
    nb_col = 0
    nb_pix = 0

    for rgb in last_line[2:]:
        if nb_col < 2:
            if rgb[0] == 0 and rgb[1] == 0 and rgb[2] == 0:
                if flag:
                    continue
                else:
                    flag = not flag
                    nb_col += 1

            elif nb_col != 0:
                nb_pix += 1
                if flag:
                    flag = not flag
        else:
            break

    return nb_pix


adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices)==0:
    print("Pas d'appareil connecté")
    quit()

device = devices[0]

while True :
    image = device.screencap()
    print("capture")
    with open('screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('screen.png')
    image = numpy.array(image, dtype=numpy.uint8)

    nb_px = nb_pix_btw(image[-600])
    if nb_px < 50:
        nb_px = 50

    print(nb_px)
    nb_px = (nb_px*0.77)+1
    print(nb_px)

    device.shell("{}{}".format('input touchscreen swipe 500 500 500 500 ', int(nb_px)))
    time.sleep(3)

image = device.screencap()

with open('screen.png', 'wb') as f:
    f.write(image)



