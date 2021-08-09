#! /usr/bin/env python

import sys
import time

from demo import animations
from flipdot import client, display


d = display.Display(56, 7,
                    panels={
                        1: ((0, 0), (28, 7)),
                        2: ((28, 0), (28, 7)),
                    },
                    upsidedown=True)


def transition(d):
    animations.rand(d)


def mainloop(d):
    # animations.display_text(d, "100%")
    # animations.tqdm(d)

    animations.alien_1(d)

    # animations.wipe_right(d)
    time.sleep(4)
    # time.sleep(2)
    # transition(d)
    # animations.blink_text(d, "HI!")
    # time.sleep(1)
    # transition(d)
    # animations.scroll_text(d, "This is scrolled text.", font=animations.SmallFont)
    # time.sleep(0.5)
    # transition(d)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "udp":
        d.connect(client.UDPClient("localhost", 9999))
    else:
        #d.connect(client.SerialClient('/dev/ttyUSB1'))
        d.connect(client.SerialClient('/dev/tty.usbserial-14110'))
    try:
        # intro(d)
        while True:
            mainloop(d)
    finally:
        d.disconnect()


if __name__ == "__main__":
    main()
