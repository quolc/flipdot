import cv2
from PIL import Image
from demo import animations
from flipdot import client, display

d = display.Display(56, 7,
                    panels={
                        1: ((0, 0), (28, 7)),
                        2: ((28, 0), (28, 7)),
                    },
                    upsidedown=True)
d.connect(client.SerialClient('/dev/tty.usbserial-14110'))

capture = cv2.VideoCapture(0)

while(True):
    ret, frame = capture.read() # (720, 1280, 3)

    img = cv2.resize(frame[:,100:1100,2], (56, 32))

    threshold = 64
    img[img >= threshold] = 255
    img[img < threshold] = 0

    d.reset()
    d.im.paste(Image.fromarray(img[10:17]), (0, 0))
    d.send()
    
    windowsize = (56*10, 32*10)
    img = cv2.resize(img, windowsize)
    cv2.imshow('title', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()