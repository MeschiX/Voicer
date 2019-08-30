#!/usr/bin/python

import math
from math import pi
import cairo
import gi
from WaitValue import cv
from FunctionButtons import FunctionButton
from TimeoutHandlers import placeholder_timeout_callback
from TimeoutHandlers import button_timeout_callback
from TimeoutHandlers import button_disappear_timeout_callback
from TimeoutHandlers import button_appear_timeout_callback
from TimeoutHandlers import timer_timeout_callback
from TimeoutHandlers import scrollbutton_appear_callback
from TimeoutHandlers import scrollbutton_desappear_callback
from TimeoutHandlers import wait_timeout_callback
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


# CLASS FOR MASTER BUTTON
class ButtonWidget():

    def __init__(self, par):
        self.colorA = [0.0, 0.55, 0.83, 1.0]
        self.position = [250, 250]
        self.inAnimation = False
        self.RecPlay = False
        self.message = "REC"
        self.parent = par
        self.radius = 60
        self.alfa = 1
        self.source_id = 0
        self.disappeared = False

    # DRAW BUTTON
    def on_expose(self, lcr):

        # GETTING POSITION
        self.position[0] = self.parent.get_size()[0] / 2
        self.position[1] = self.parent.get_size()[1] / 2

        RGBA = self.colorA

        # DRAW BUTTON SURFACE
        lcr.translate(self.position[0], self.position[1])
        lcr.arc(0, 0, self.radius, 0, 2 * math.pi)
        lcr.set_source_rgba(RGBA[0], RGBA[1], RGBA[2], self.alfa)
        lcr.fill()

        # CHOOSING BUTTON MESSAGE

        # DRAW BUTTTON MESSAGE
        lcr.set_source_rgb(0.21, 0.24, 0.31)
        lcr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
        lcr.set_font_size(40)
        (x, y, width, height, dx, dy) = lcr.text_extents(self.message)
        lcr.move_to(0 - width / 2, 0 + height / 2)
        lcr.show_text(self.message)

        # RESTORE CONTEXT POSITION
        lcr.translate(-self.position[0], -self.position[1])

    # BUTTON'S CLICK EVENT HANDLER
    def on_click(self, lcr, x, y):

        # GETTING DISTANCE FROM BUTTON
        distance = math.sqrt(math.pow((self.parent.get_size()[0] / 2 - x), 2) +
                             math.pow((self.parent.get_size()[1] / 2 - y), 2))

        # IF NOT IN ANIMATION PERFORMING HIT-TEST
        # -- if true --> START/STOP PARENT.TIMER
        # AND START/STOP RECORDING
        if self.inAnimation is False and distance <= self.radius:


            self.RecPlay = not self.RecPlay
            
            if self.RecPlay is True:
                self.inAnimation = True                
                self.source_id = GObject.timeout_add(
                3, button_timeout_callback, self)
                self.parent.Timer.on_rec()
                self.parent.main.OnRec()
            else:
                self.parent.Timer.stop_rec()
                self.desappear()                
                self.parent.main.OnStop()

            self.parent.hitsomething = True

    def desappear(self):
        if not self.inAnimation:
            self.inAnimation = True
            self.source_id = GObject.timeout_add(
                2, button_disappear_timeout_callback, self)

    def appear(self):
        if not self.inAnimation:
            self.inAnimation = True
            self.source_id = GObject.timeout_add(
                4, button_appear_timeout_callback, self)


# CLASS FOR RECORDING TIMER
class RecTimer():

    def __init__(self, par):
        self.parent = par
        self.position = [400, 400]
        self.colorA = [0.0, 0.55, 0.83, 1.0]
        self.Play = False
        self.seconds = 0
        self.message = ""
        self.source_id = 0

    # DRAW TIMER
    def on_expose(self, lcr):

        if self.Play is True:

            RGBA = self.colorA
            self.position[0] = (self.parent.get_size()[0])
            self.position[1] = (self.parent.get_size()[1])

            self.message = self.get_minutes() + ":" + self.get_seconds()

            lcr.set_source_rgba(RGBA[0], RGBA[1], RGBA[2], 0.5)
            lcr.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            lcr.set_font_size(40)
            lcr.move_to(self.position[0] - 115, self.position[1] - 10)
            lcr.show_text(self.message)

    # STARTING TIMER
    def on_rec(self):

        self.Play = True
        self.source_id = GObject.timeout_add(
            1000, timer_timeout_callback, self)

    # STOPPING TIMER
    def stop_rec(self):

        self.Play = False
        self.seconds = 0
        GObject.source_remove(self.source_id)

    # DO NOTHING ON CLICK
    def on_click(self, lcr, x, y):
        pass

    # GETTER METHOD FOR SECONDS
    def get_seconds(self):
        if self.seconds < 10:
            return "0" + str(self.seconds)
        else:
            return str(self.seconds % 60)

    # GETTER METHOD FOR MINUTES
    def get_minutes(self):
        if int(self.seconds / 60) < 10:
            return "0" + str(int(self.seconds / 60))
        else:
            return str(int(self.seconds / 60))


class FilePlaceHolder():

    def __init__(self, par):

        self.parent = par
        self.Nid = len(self.parent.FilesPlaceHolders)
        self.filename = "TAKE" + str(self.Nid + 1)
        self.position_request = []
        if self.Nid == 0:
            self.position_request = [10, 10]
        else:
            prcd = self.parent.FilesPlaceHolders[self.Nid - 1]
            marginabove = prcd.position_request[1]
            marginabove += prcd.dimension_request[1]
            marginabove += prcd.margin + 10
            self.position_request.append(10)
            self.position_request.append(marginabove)

        self.dimension_request = [50, 50]
        self.real_position = [
            self.position_request[0] + self.dimension_request[0] / 2,
            self.position_request[1] + self.dimension_request[1] / 2]
        self.real_dimension = [0, 0]
        self.colorA = [0.0, 0.55, 0.83, 1.0]
        self.fontsize = 0.0
        self.margin = 0
        self.appeared = False
        self.inAnimation = False
        self.clicked = False
        self.source_id = 0
        self.alfa = 0

    def on_expose(self, lcr):

        if self.appeared is False and self.inAnimation is False:
            self.inAnimation = True
            self.source_id = GObject.timeout_add(
                10, placeholder_timeout_callback, self)

        else:

            w = self.real_dimension[0]
            h = self.real_dimension[1]

            px = self.real_position[0]
            py = self.real_position[1]

            if self.clicked:
                # DRAW ITEM'S BACKGROUND
                lcr.translate(self.real_position[0] +
                              self.real_dimension[0] / 2,
                              self.real_position[1] +
                              self.real_dimension[1] / 2)

                lcr.arc(0, 0, self.real_dimension[0] / 2, 0, 2 * math.pi)
                lcr.set_source_rgb(0.0, 0.55, 0.83)
                lcr.fill()
                # RESTORE CONTEXT REAL_POSITION
                lcr.translate(-(self.real_position[0] +
                                self.real_dimension[0] / 2),
                              -(self.real_position[1] +
                                self.real_dimension[1] / 2))
                lcr.set_source_rgb(0.21, 0.24, 0.31)
            else:
                lcr.set_source_rgba(0.0, 0.55, 0.83, self.alfa)

            # DRAW ITEM'S SYMBOL
            lcr.set_line_width((self.real_dimension[0] / 100) * 3)

            gap = w / 15
            # POPORTIONAL VALUES FOR DRAWING SYMBOL
            incrValues = [33.3, 16.66, 10.0, 5.55, 3.84,
                          2.94, 2.17, 3.84, 5.55, 7.55,
                          10, 13, 19, 40]
            for i in range(len(incrValues)):
                lcr.move_to(px + gap * (i + 1), py + h / 2 - h / incrValues[i])
                lcr.line_to(px + gap * (i + 1), py + h / 2 + h / incrValues[i])
                lcr.stroke()

            # DRAW FILE NAME
            lcr.set_source_rgba(0.0, 0.55, 0.83, 1.0)
            lcr.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
            lcr.set_font_size(self.fontsize)
            (x, y, width, height, dx, dy) = lcr.text_extents(self.filename)
            self.margin = height
            lcr.move_to(px + 5, py + h + height)
            lcr.show_text(self.filename)

    # PLACEHOLDER'S CLICK EVENT HANDLER
    def on_click(self, lcr, x, y):

        if not self.inAnimation:
            centx = self.real_position[0] + self.real_dimension[0] / 2
            centy = self.real_position[1] + self.real_dimension[1] / 2

            distance = math.sqrt(math.pow((centx - x), 2) +
                                 math.pow((centy - y), 2))

            if distance <= self.real_dimension[0] / 2:

                for i in range(0, len(self.parent.FilesPlaceHolders)):
                    if i != self.Nid:
                        self.parent.FilesPlaceHolders[i].clicked = False

                if self.clicked:
                    self.clicked = False
                    self.parent.RecStopButton.appear()
                    self.parent.FunctionElements.desappear_all()
                    self.parent.ScrollButtons.desappear()
                else:
                    self.clicked = True
                    self.parent.RecStopButton.desappear()
                    self.parent.FunctionElements.appear_all()
                    self.parent.ScrollButtons.appear()

                self.parent.queue_draw()
                self.parent.hitsomething = True


class ScrollButtons(object):

    def __init__(self, par):

        self.parent = par
        self.dimension = 0
        self.alfa = 0
        self.enabled = False
        self.source_id = 0
        self.inAnimation = False


    def on_expose(self, lcr):

        if self.enabled:

            w = self.dimension

            px = self.parent.get_size()[0]
            py = self.parent.get_size()[1]

            lcr.set_source_rgba(0.0, 0.55, 0.83, self.alfa)
            lcr.arc(px, 0, self.dimension, 0, 2*pi)
            lcr.fill()

            lcr.arc(px, py, self.dimension, 0, 2*pi)
            lcr.fill()

            lcr.set_source_rgb(0.21, 0.24, 0.31)
            lcr.set_line_width(3)
            lcr.set_line_cap(cairo.LINE_CAP_ROUND)
            lcr.set_line_join(cairo.LINE_JOIN_ROUND)

            lcr.move_to(px - w / 1.35, w / 2)
            lcr.line_to(px - w / 2.63, w / 10)
            lcr.line_to(px - w / 16.66, w / 2)
            lcr.stroke()

            lcr.move_to(px - w / 1.35, py - w / 2)
            lcr.line_to(px - w / 2.63, py - w / 10)
            lcr.line_to(px - w / 16.66, py - w / 2)
            lcr.stroke()

    def appear(self):
        if not self.inAnimation:
            self.enabled = True
            self.inAnimation = True
            self.source_id = GObject.timeout_add(
                1, scrollbutton_appear_callback, self)
            self.parent.queue_draw()
            self.scrollcount = 0

    def desappear(self):
        if not self.inAnimation:
            self.inAnimation = True
            self.source_id = GObject.timeout_add(
                1, scrollbutton_desappear_callback, self)
            self.parent.queue_draw()

    def on_click(self, lcr, x, y):

        if self.enabled:

            px = self.parent.get_size()[0]
            py = self.parent.get_size()[1]

            distanceUP = math.sqrt(math.pow((px - x), 2) +
                                   math.pow((0 - y), 2))

            distanceDOWN = math.sqrt(math.pow((px - x), 2) +
                                     math.pow((py - y), 2))

            if distanceUP <= self.dimension:

                self.parent.hitsomething = True

                if not self.inAnimation:

                    pH = self.parent.get_size()[1]
                
                    FI = self.parent.FunctionElements.get_by_index(0)
                    (_, y) = self.parent.transform.transform_point(
                        FI.Position_request[0], FI.Position_request[1])
                    if y < pH / 20:
                        self.parent.transform.translate(0, 20)
                        self.parent.transform_inverse.translate(0, -20)
                        self.scrollcount -= 1                
                        self.parent.queue_draw()
                    else:
                        self.parent.ScrollLimits.pulseTop()

            elif distanceDOWN <= self.dimension:

                self.parent.hitsomething = True

                if not self.inAnimation:

                    pH = self.parent.get_size()[1]

                    LL = self.parent.FunctionElements.get_len() - 1
                    FI = self.parent.FunctionElements.get_by_index(LL)
                    (_, y) = self.parent.transform.transform_point(
                        FI.Position_request[0], FI.Position_request[1])

                    if y + FI.Request_dimension > (pH - pH / 25):
                        self.parent.transform.translate(0, -20)
                        self.parent.transform_inverse.translate(0, 20)
                        self.scrollcount -= 1
                        self.parent.queue_draw()
                    else:
                        self.parent.ScrollLimits.pulseBottom()


class PlayButton(FunctionButton):

    def __init__(self, par, img, nitem, message):
        super(PlayButton, self).__init__(par, img, nitem, message)

    def on_click(self, lcr, x, y):

        if super(PlayButton, self).on_click(lcr, x, y):
            fileid = None
            for item in self.Parent.FilesPlaceHolders:
                if item.clicked:
                    fileid = item.Nid
                    break
            filename = "take" + str(fileid + 1) + ".wav"
            self.Parent.main.OnPlay(filename)


class MelodyButton(FunctionButton):

    def __init__(self, par, img, nitem, message):
        super(MelodyButton, self).__init__(par, img, nitem, message)

    def on_click(self, lcr, x, y):
        if super(MelodyButton, self).on_click(lcr, x, y):
            fileid = None
            for item in self.Parent.FilesPlaceHolders:
                if item.clicked:
                    fileid = item.Nid
                    break
            filename = "take" + str(fileid + 1) + "-melody.wav"
            self.Parent.main.OnPlay(filename)


class SlowButton(FunctionButton):

    def __init__(self, par, img, nitem, message):
        super(SlowButton, self).__init__(par, img, nitem, message)

    def on_click(self, lcr, x, y):

        if super(SlowButton, self).on_click(lcr, x, y):
            fileid = None
            for item in self.Parent.FilesPlaceHolders:
                if item.clicked:
                    fileid = item.Nid
                    break
            filename = "take" + str(fileid + 1) + "-slower.wav"
            self.Parent.main.OnPlay(filename)


class FastButton(FunctionButton):
    
    def __init__(self, par, img, nitem, message):
        super(FastButton, self).__init__(par, img, nitem, message)

    def on_click(self, lcr, x, y):

        if super(FastButton, self).on_click(lcr, x, y):
            fileid = None
            for item in self.Parent.FilesPlaceHolders:
                if item.clicked:
                    fileid = item.Nid
                    break
            filename = "take" + str(fileid + 1) + "-faster.wav"
            self.Parent.main.OnPlay(filename)


class RobotButton(FunctionButton):

    def __init__(self, par, img, nitem, message):
        super(RobotButton, self).__init__(par, img, nitem, message)

    def on_click(self, lcr, x, y):

        if super(RobotButton, self).on_click(lcr, x, y):
            fileid = None
            for item in self.Parent.FilesPlaceHolders:
                if item.clicked:
                    fileid = item.Nid
                    break
            filename = "take" + str(fileid + 1) + "-robot.wav"
            self.Parent.main.OnPlay(filename)


class WaitWidjet(object):

    def __init__(self, par):

        self.parent = par
        self.dimension = 120
        self.position = [190, 190]
        self.count = 0                
        self.source_id = 0

    def on_expose(self, lcr):

        if self.parent.waitingFlag:

            w, h = self.parent.get_size()
            lcr.translate(w/2, h/2)

            
            lcr.set_line_cap(cairo.LINE_CAP_ROUND)

            lcr.set_line_width(10)
            
            for i in range(cv.NLINES):
                lcr.set_source_rgba(0.0, 0.55, 0.83, cv.trs[self.count % 8][i])
                lcr.move_to(0.0, -20.0)
                lcr.line_to(0.0, -100.0)
                lcr.rotate(math.pi/4)
                lcr.stroke()


    def active(self):
        self.parent.waitingFlag = True
        self.parent.RecStopButton.desappear()
        self.source_id = GObject.timeout_add(cv.SPEED, wait_timeout_callback, self)

    def PLAppend(self):
        newplaceholder = FilePlaceHolder(self.parent)
        self.parent.FilesPlaceHolders.append(newplaceholder)


class ScrollLimits(object):

    def __init__(self, par):
        self.parent = par
        self.alfaTop = 0
        self.alfaBottom = 0
        self.PulseStepTop = 0
        self.PulseStepBottom = 0
        self.source_id_top = 0
        self.source_id_botttom = 0
        self.inAnimationTop = False
        self.inAnimationBottom = False
        
        
    def on_expose(self, lcr):

        w = self.parent.get_size()[0]
        h = self.parent.get_size()[1]

        if self.inAnimationTop:
            lg = cairo.LinearGradient(0.0, 0-200.0, 0.0, 100.0)
            lg.add_color_stop_rgba(0.0, 0, 0.55, 0.83, self.alfaTop) 
            lg.add_color_stop_rgba(1.0, 0.21, 0.24, 0.31, self.alfaTop) 

            lcr.rectangle(0, 0, w, 100)
            lcr.set_source(lg)
            lcr.fill()

        if self.inAnimationBottom:
            lg2 = cairo.LinearGradient(0.0, h+200, 0.0, h-100)
            lg2.add_color_stop_rgba(0.0, 0, 0.55, 0.83, self.alfaBottom)
            lg2.add_color_stop_rgba(1.0, 0.21, 0.24, 0.31, self.alfaBottom) 

            lcr.rectangle(0, h-100, w, 100)
            lcr.set_source(lg2)
            lcr.fill()
        
    def pulseTop(self):

        if not self.inAnimationTop:

            def callback(sl):

                if sl.PulseStepTop == 0:
                    sl.alfaTop += 0.06
                    if sl.alfaTop >= 1:
                        sl.PulseStepTop = 1
                    sl.parent.queue_draw()
                elif sl.PulseStepTop == 1:
                    sl.alfaTop -= 0.03
                    if sl.alfaTop <= 0:
                        sl.PulseStepTop = 2
                    sl.parent.queue_draw()                        
                else:
                    sl.source_id_top = 0
                    sl.PulseStepTop = 0
                    sl.inAnimationTop = False
                    return False
                return True
                    
                    
            self.inAnimationTop = True
            self.source_id_top = GObject.timeout_add(1, callback, self)

    def pulseBottom(self):

        if not self.inAnimationBottom:

            def callback(sl):

                if sl.PulseStepBottom == 0:
                    sl.alfaBottom += 0.06
                    if sl.alfaBottom >= 1:
                        sl.PulseStepBottom = 1
                    sl.parent.queue_draw()
                elif sl.PulseStepBottom == 1:
                    sl.alfaBottom -= 0.03
                    if sl.alfaBottom <= 0:
                        sl.PulseStepBottom = 2
                    sl.parent.queue_draw()                        
                else:
                    sl.source_id_botttom = 0
                    sl.PulseStepBottom = 0
                    sl.inAnimationBottom = False
                    return False
                return True
                    
                    
            self.inAnimationBottom = True
            self.source_id_botttom = GObject.timeout_add(1, callback, self)


    def on_click(self, lcr, x, y):
        pass
