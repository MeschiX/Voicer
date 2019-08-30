#!/usr/bin/python

import cairo
from Widgets import ButtonWidget
from Widgets import RecTimer
from Widgets import PlayButton
from Widgets import MelodyButton
from Widgets import ScrollButtons
from Widgets import SlowButton
from Widgets import FastButton
from Widgets import RobotButton
from Widgets import WaitWidjet
from Widgets import ScrollLimits
from FunctionButtonsList import FunctionButtonList
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


# CLASS FOR ROOT WINDOW
class MasterWindow(Gtk.Window):

    def __init__(self, MAIN):
        super(MasterWindow, self).__init__()

        # REFERENCE AT MAIN PARENT CLASS
        self.main = MAIN

        # CREATE WINDOW
        self.set_title("Voicer")
        self.set_size_request(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.transform = cairo.Matrix()
        self.transform_inverse = cairo.Matrix()
        
        # CREATE SUB-WINDOW ELEMENTS
        self.Ebox = Gtk.EventBox()
        self.Darea = Gtk.DrawingArea()
        self.Components = []
        self.FilesPlaceHolders = []
        self.FunctionElements = FunctionButtonList()

        self.PlayFlag = True
        self.MelodyFlag = True
        self.SlowFlag = True
        self.FastFlag = True
        self.RobotFlag = True
        self.waitingFlag = False

        self.WaitWidjet = WaitWidjet(self)

        # DEFINING WIDGETS AND APPENDING AT COMPONENTS LIST
        self.RecStopButton = ButtonWidget(self)
        self.Components.append(self.RecStopButton)
        self.Timer = RecTimer(self)
        self.Components.append(self.Timer)
        self.ScrollLimits = ScrollLimits(self)
        self.Components.append(self.ScrollLimits)
        self.ScrollButtons = ScrollButtons(self)
        self.Components.append(self.ScrollButtons)
        self.PlayButton = PlayButton(self, "./icons/play.png", 0, "PLAY")
        self.FunctionElements.append(self.PlayButton)
        self.MelodyButton = MelodyButton(self, "./icons/note.png", 1, "MELODY")
        self.FunctionElements.append(self.MelodyButton)
        self.SlowButton = SlowButton(self, "./icons/slow.png", 2, "SLOW")
        self.FunctionElements.append(self.SlowButton)        
        self.FastButton = FastButton(self, "./icons/fast.png", 3, "FAST")
        self.FunctionElements.append(self.FastButton)        
        self.RobotButton = RobotButton(self, "./icons/robot.png", 4, "ROBOT")
        self.FunctionElements.append(self.RobotButton)        
        
        # EVENT LINKING
        self.Darea.connect("draw", self.on_expose)
        self.Ebox.connect("button-press-event", self.on_click)
        self.connect("key-press-event",self.on_keypress)        
        self.connect("destroy", self.main.OnQuit)

        # PACKING ELEMENTS IN THE WINDOW
        self.Ebox.add(self.Darea)
        self.add(self.Ebox)


    # DRAW WINDOW
    def on_expose(self, ww, crr):

        self.cr = crr

        # GETTING WINDOW DIMENSION
        w = self.get_size()[0]
        h = self.get_size()[1]

        # COLORING BACKGROUND
        self.cr.set_antialias(cairo.ANTIALIAS_DEFAULT)
        self.cr.set_source_rgb(0.21, 0.24, 0.31)
        self.cr.rectangle(0, 0, w, h)
        self.cr.fill()

        if not self.waitingFlag or not self.RecStopButton.disappeared:
            # DRAW ALL SUB-WINDOW ELEMENTS
            for i in range(0, len(self.Components)):
                self.Components[i].on_expose(self.cr)
            for i in range(0, len(self.FilesPlaceHolders)):
                self.FilesPlaceHolders[i].on_expose(self.cr)

            self.cr.save()

            self.cr.transform(self.transform)
            for i in range(0,self.FunctionElements.get_len()):
                self.FunctionElements.get_by_index(i).on_expose(self.cr)

            self.cr.restore()
        else:

            self.WaitWidjet.on_expose(self.cr)
            
            

    # WINDOW CLICK EVENT HANDLER
    def on_click(self, widget, event):

        if not self.waitingFlag:
            
            self.hitsomething = False

            # DISPATCH CLICK EVENT TO ALL SUB-WINDOW ELEMENTS
            for i in range(0, len(self.Components)):
                self.Components[i].on_click(self.cr, event.x, event.y)
            for i in range(0, len(self.FilesPlaceHolders)):
                self.FilesPlaceHolders[i].on_click(self.cr, event.x, event.y)

            x, y = self.transform_inverse.transform_point(event.x, event.y)
            
            for i in range(0, self.FunctionElements.get_len()):
                self.FunctionElements.get_by_index(i).on_click(self.cr, x, y)

            if self.hitsomething is False and self.RecStopButton.disappeared:
                for i in range(0, len(self.FilesPlaceHolders)):
                    self.FilesPlaceHolders[i].clicked = False
                self.FunctionElements.desappear_all()
                self.ScrollButtons.desappear()            
                self.RecStopButton.appear()

    def on_keypress(self, widget, event):


        if not self.waitingFlag:

            keyval = event.keyval
            keyvalname = Gdk.keyval_name(keyval)

            
        
            for i in range(0, len(self.FilesPlaceHolders)):
                if self.FilesPlaceHolders[i].clicked is True:

                    pH = self.get_size()[1]                        
                    
                    if keyvalname == "Up":
                
                        FI = self.FunctionElements.get_by_index(0)
                        (_, y) = self.transform.transform_point(
                            FI.Position_request[0], FI.Position_request[1])
                        if y < pH / 20:
                            self.transform.translate(0, 20)
                            self.transform_inverse.translate(0, -20)
                            self.ScrollButtons.scrollcount -= 1                
                            self.queue_draw()
                        else:
                            self.ScrollLimits.pulseTop()

                    if keyvalname == "Down":
                        LL = self.FunctionElements.get_len() - 1
                        FI = self.FunctionElements.get_by_index(LL)
                        (_, y) = self.transform.transform_point(
                            FI.Position_request[0], FI.Position_request[1])

                        if y + FI.Request_dimension > (pH - pH / 25):
                            self.transform.translate(0, -20)
                            self.transform_inverse.translate(0, 20)
                            self.ScrollButtons.scrollcount -= 1
                            self.queue_draw()
                        else:
                            self.ScrollLimits.pulseBottom()

