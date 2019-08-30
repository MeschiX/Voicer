#!/usr/bin/python

from WaitValue import cv
from gi.repository import GObject

def scrollbutton_appear_callback(buttons):
    if buttons.dimension < 50:
        buttons.alfa += 0.02
        buttons.dimension += 1
        buttons.parent.queue_draw()
    else:
        GObject.source_remove(buttons.source_id)
        buttons.inAnimation = False
    return True

def scrollbutton_desappear_callback(buttons):
    if buttons.dimension > 0:
        buttons.alfa -= 0.02
        buttons.dimension -= 1
        buttons.parent.queue_draw()
    else:
        GObject.source_remove(buttons.source_id)
        buttons.inAnimation = False
        buttons.enabled = False
    return True


# FILE PLACEHOLDER'S TIMEOUT EVENT HANDLER
def placeholder_timeout_callback(placeholder):
    ph = placeholder
    ifflag = (ph.real_dimension[0] < ph.dimension_request[0]) and (
        ph.appeared is False)
    if ifflag:
        ph.real_position[0] -= 1
        ph.real_position[1] -= 1
        ph.real_dimension[0] += 2
        ph.real_dimension[1] += 2
        ph.fontsize += 20 / 35
        ph.alfa += 1 / 20
        ph.parent.queue_draw()
    else:
        ph.appeared = True
        ph.inAnimation = False
        GObject.source_remove(ph.source_id)
    return True

# FILE PLACEHOLDER'S TIMEOUT EVENT HANDLER


def robot_appear_timeout_callback(robotbutton):
    rb = robotbutton
    ifflag = (rb.real_dimension[0] < rb.dimension_request[0]) and (
        rb.appeared is False)
    if ifflag:
        rb.gap -= 1
        rb.real_dimension[0] += 2
        rb.real_dimension[1] += 2
        rb.alfa += 1 / 58
        rb.parent.queue_draw()
    else:
        rb.appeared = True
        rb.inAnimation = False
        GObject.source_remove(rb.source_id)
    return True


def robot_desappear_timeout_callback(robotbutton):
    rb = robotbutton
    ifflag = (rb.real_dimension[0] > 1) and (
        rb.appeared is True)
    if ifflag:
        rb.gap += 1
        rb.real_dimension[0] -= 2
        rb.real_dimension[1] -= 2
        rb.alfa -= 1 / 58
        rb.parent.queue_draw()
    else:
        rb.appeared = False
        rb.inAnimation = False
        rb.enabled = False
        GObject.source_remove(rb.source_id)
    return True


# BUTTON'S TIMEOUT EVENT HANDLER
def button_timeout_callback(button):

    if button.alfa > 0:
        button.radius += 1.5
        button.alfa -= 0.011
    else:
        button.radius = 0
        button.alfa = 0
        GObject.source_remove(button.source_id)
        button.inAnimation = False

        if button.RecPlay is False:
            button.message = "REC"
        else:
            button.message = "STOP"

        button.appear()
    button.parent.queue_draw()
    return True


def button_disappear_timeout_callback(button):

    if button.alfa > 0:
        button.radius -= 1
        button.alfa -= 1 / 60
    else:
        button.radius = 0
        GObject.source_remove(button.source_id)
        button.inAnimation = False
        button.disappeared = True
        if button.parent.waitingFlag:
            button.parent.main.OnProcessing()
            button.message = "REC"
    button.parent.queue_draw()
    return True


def button_appear_timeout_callback(button):

    if button.alfa < 1.0:
        button.alfa += 1 / 60
        button.radius += 1
    else:
        GObject.source_remove(button.source_id)
        button.inAnimation = False
        button.disappeared = False
    button.parent.queue_draw()
    return True


# TIMER'S TIMEOUT EVENT
def timer_timeout_callback(timer):
    if timer.Play is True:
        timer.seconds += 1
        # print(str(timer.seconds))
    timer.parent.queue_draw()
    return True


def wait_timeout_callback(ww):

    pp = ww.parent

    if pp.waitingFlag:
        ww.count = ww.count + 1

        if ww.count >= cv.CLIMIT:
            ww.count = 0

        ww.parent.queue_draw()

    else:
        ww.source_id = 0
        pp.RecStopButton.appear()
        ww.PLAppend()
        return False

    return True
        
