#!/usr/bin/python

import cairo
import math
from math import pi
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


class FunctionButtonList(object):

    def __init__(self):  
        self.ButtonList = []
        self.source_id = 0
        self.verticalLength = 0
        
    def append(self, item):
        self.ButtonList.append(item)
        self.verticalLength += 145

    def get_by_index(self, index):
        return self.ButtonList[index]

    def get_len(self):
        return len(self.ButtonList)

    def in_animation(self):
        for i in range(0, len(self.ButtonList)):
            if self.ButtonList[i].InAnimation:
                return True
        return False

    def appear_all(self):

        def appear_all_callback(Blist):
            exbt = Blist.ButtonList[0]
            flag = exbt.Real_dimension < exbt.Request_dimension
            if flag:
                for i in range(0, len(Blist.ButtonList)):
                    Blist.ButtonList[i].Gap -= 1
                    Blist.ButtonList[i].Real_dimension += 2
                    Blist.ButtonList[i].Alfa += 1 / 57
                exbt.Parent.queue_draw()
            else:
                for i in range(0, len(Blist.ButtonList)):
                    Blist.ButtonList[i].InAnimation = False
                GObject.source_remove(Blist.source_id)
            return True

        if not self.in_animation():
            for i in range(0, len(self.ButtonList)):
                self.ButtonList[i].Enabled = True
                self.ButtonList[i].InAnimation = True
            self.source_id = GObject.timeout_add(
                2, appear_all_callback, self)

    def desappear_all(self):

        def desappear_all_callback(Blist):
            exbt = Blist.ButtonList[0]
            flag = exbt.Real_dimension > 1
            if flag:
                for i in range(0, len(Blist.ButtonList)):
                    Blist.ButtonList[i].Gap += 1
                    Blist.ButtonList[i].Real_dimension -= 2
                    Blist.ButtonList[i].Alfa -= 1 / 57
                exbt.Parent.queue_draw()
            else:
                for i in range(0, len(Blist.ButtonList)):
                    Blist.ButtonList[i].InAnimation = False
                    Blist.ButtonList[i].Enabled = False
                GObject.source_remove(Blist.source_id)
            return True

        if not self.in_animation():
            for i in range(0, len(self.ButtonList)):
                self.ButtonList[i].InAnimation = True
            self.source_id = GObject.timeout_add(
                2, desappear_all_callback, self)
