#!/usr/bin/python

import cairo
import math
from math import pi
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


class FunctionButton(object):

    

    def __init__(self, par, img, nitem, message):

        self.Parent = par

        self.Request_dimension = 115
        self.Real_dimension = 1
        self.Gap = 115 / 2
        self.InAnimation = False
        self.Enabled = False
        self.Alfa = 0
        self.Source_id = 0
        self.Parent = par
        
        self.Nitem = nitem
        self.Position_request = [self.Parent.get_size()[0] / 3 -
                                 self.Request_dimension / 2,
                                 self.Parent.get_size()[1] / 20 +
                                 (145) * self.Nitem]
        self.Real_Position = [self.Position_request[0] +
                              self.Gap,
                              self.Position_request[1] +
                              self.Gap]

        self.Image = cairo.ImageSurface.create_from_png(img)
        self.Fontsize = 25
        self.Message = message

    def on_expose(self, lcr):

        if self.Enabled:

            self.Position_request = [self.Parent.get_size()[0] / 3 -
                                     self.Request_dimension / 2,
                                     self.Parent.get_size()[1] / 20 +
                                     (145) * self.Nitem]

            self.Real_Position = [self.Position_request[0] + self.Gap,
                                  self.Position_request[1] + self.Gap]

            d = self.Real_dimension

            px = self.Real_Position[0]
            py = self.Real_Position[1]

            lcr.arc(px + d / 2, py + d / 2, d / 2, 0, 2 * pi)
            lcr.set_source_rgba(0.0, 0.55, 0.83, self.Alfa)
            lcr.fill()

            lcr.save()

            lcr.translate(px, py)
            scalefactor = d / 512
            lcr.scale(scalefactor, scalefactor)
            lcr.set_source_surface(self.Image, 0, 0)
            lcr.paint()

            lcr.restore()

            lcr.set_source_rgba(0.0, 0.55, 0.83, self.Alfa)
            lcr.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
            lcr.set_font_size(25)

            prx = self.Position_request[0]
            pry = self.Position_request[1]
            (x, y, width, height, dx, dy) = lcr.text_extents(self.Message)
            lcr.move_to(prx + d + 10, pry + height * 3)
            lcr.show_text(self.Message)

    def on_click(self, lcr, x, y):

        if self.Enabled:
            
            d = self.Real_dimension

            px = self.Real_Position[0]
            py = self.Real_Position[1]

            distance = math.sqrt(math.pow((px + d / 2 - x), 2) +
                                 math.pow((py + d / 2 - y), 2))

            if distance <= self.Real_dimension / 2:

                self.Parent.hitsomething = True

                if self.InAnimation:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def appear(self):

        def appear_callback():
            flag = self.Real_dimension < self.Request_dimension
            if flag:
                self.Gap -= 0.5
                self.Real_dimension += 1
                self.Alfa += 1 / 114
                self.Parent.queue_draw()
            else:
                self.InAnimation = False
                GObject.source_remove(self.Source_id)
            return True
        
        if not self.InAnimation:
            self.Enabled = True
            self.InAnimation = True
            self.Source_id = GObject.timeout_add(
                2, appear_callback)

    def desappear(self):

        def desappear_callback():
            flag = self.Real_dimension > 1
            if flag:
                self.Gap += 0.5
                self.Real_dimension -= 1
                self.Alfa -= 1 / 114
                self.Parent.queue_draw()
            else:
                self.InAnimation = False
                self.Enabled = False
                GObject.source_remove(self.Source_id)
            return True
        
        if not self.InAnimation:
            self.InAnimation = True
            self.Source_id = GObject.timeout_add(
                2, desappear_callback)

