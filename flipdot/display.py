#! /usr/bin/env python
#
# display.py

from __future__ import print_function
from PIL import Image, ImageDraw


#
# A flip-dot "display" is a set of individually addressable Panels
# arranged to form a single large virtual display
#

class Display(object):

    def __init__(self, w, h, panels=None, upsidedown=False):
        """
        Construct a display of given width and height, with the given ID.
        Note that we use and RGB backing image since some PIL implementations
        don't seem to support 1-bit (mode "1") images well.

        'panels' is a dictionary mapping:
        address (int) -> ((x, y), (w, h))

        If panels is empty, a default mapping of address 1 to the whole
        display is used.

        Only rectangular panel combinations are allowed.
        """
        self.client = None
        self.im = Image.new("RGB", (w, h))
        if panels:
            self.panels = panels
        else:
            self.panels = {
                1: ((0, 0), (w, h)),
            }
        self.upsidedown = upsidedown

    def connect(self, client):
        """
        Connect a display to a client
        """
        self.client = client
        self.client.open()

    def disconnect(self):
        """
        Disconnect the client from this display
        """
        if self.client:
            self.client.close()
        self.client = None

    def reset(self, address=None, white=False):
        """
        Reset a given panel to black. if no panel is given,
        reset the entire display. (optionally set to all white)
        """
        draw = ImageDraw.Draw(self.im)
        if address:
            xy, sz = self.panels[address]
        else:
            xy, sz = (0, 0), self.im.size
        c = (255, 255, 255) if white else (0, 0, 0)
        draw.rectangle([xy, sz], fill=c)
        del draw

    def send(self, refresh=True):
        if not self.client:
            return
        for address in self.panels.keys():
            self.client.send(address, self.to_bytes(address), refresh)

    def to_bytes(self, address):
        px = self.im.load()

        (xs, ys), (w, h) = self.panels[address]
        result = bytearray()

        if self.upsidedown:
            xrange = range(xs + w - 1, xs - 1, -1)
            yrange = range(0, h)
        else:
            xrange = range(xs, xs + w)
            yrange = range(h-1, -1, -1)

        for x in xrange:
            if h is not 7:
                print("H is not 7!!!!")
            b = 0
            for y in yrange:
                p = self.px_to_bit(px[x, ys + y])
                b = (b << 1) | p
            result.append(b)
        return result

    def px_to_bit(self, px):
        (r, g, b) = px
        p = 1 if (r+g+b) > 400 else 0
        return p
