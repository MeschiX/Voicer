#!/usr/bin/python

import threading
import wave
import os
import glob
import pyaudio
import gi
import struct
from Robotize import Robotize
from TimeStretch import Stretch
from ExtractMelody import ExtractMelody
gi.require_version('Gtk', '3.0')
from MasterWindow import MasterWindow
from gi.repository import Gtk


class Main(object):

    def __init__(self):

        self.counter = 0
        self.filename = ""
        self.recflag = False
        self.filename = ""

        self.RecFrames = []
        self.stream = None
        self.audiocontext = None

        self.processThread = None

        # CREATE MAIN WINDOW
        self.window = MasterWindow(self)

        self.window.show_all()

    def OnRec(self):

        self.recflag = True

        self.counter += 1

        self.audiocontext = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            if self.recflag:
                callback_falg = pyaudio.paContinue
                self.RecFrames.append(in_data)
                x = (struct.unpack( "h", in_data[:2]))

                if not self.window.RecStopButton.inAnimation:
                    self.window.RecStopButton.radius = 60 + int(abs(x[0] / 170))
                    self.window.queue_draw()
            else: 
                self.window.RecStopButton.radius = 60
                callback_falg = pyaudio.paComplete
                self.window.queue_draw()                
            return None, callback_falg

        self.stream = self.audiocontext.open(format=pyaudio.paInt16,
                                             channels=1,
                                             rate=44100,
                                             input=True,
                                             frames_per_buffer=1024,
                                             stream_callback=callback)

        self.stream.start_stream()
        print("recording...")

    def OnStop(self):

        self.recflag = False
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.audiocontext.terminate()

        self.filename = "take" + str(self.counter) + ".wav"

        sf = wave.open(self.filename, 'wb')
        sf.setnchannels(1)
        sf.setsampwidth(self.audiocontext.get_sample_size(pyaudio.paInt16))
        sf.setframerate(44100)
        sf.writeframes(b''.join(self.RecFrames))
        sf.close()

        self.audiocontext = None
        self.RecFrames = []

        self.window.PlayFlag = False
        self.window.MelodyFlag = False
        self.window.SlowFlag = False
        self.window.FastFlag = False
        self.window.RobotFlag = False
        self.window.cr.save()
        self.window.WaitWidjet.active()

        
        
    def OnQuit(self, plus):

        for filename in glob.glob("take*"):
            os.remove(filename)
        print("Closing")
        Gtk.main_quit()

    def OnPlay(self, filename):

        wf = wave.open(filename, 'rb')

        # instantiate PyAudio (1)
        self.audiocontext = pyaudio.PyAudio()
        p = self.audiocontext

        # define callback (2)
        def callback(in_data, frame_count, time_info, status):

            if in_data != "":
                data = wf.readframes(frame_count)
                callbackflag = pyaudio.paContinue
            else:
                callbackflag = pyaudio.paComplete
                self.StopPlay(wf)

            return (data, callbackflag)

        # open stream using callback (3)
        self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True,
                             stream_callback=callback)

        self.stream.start_stream()

    def StopPlay(self, wf):
        # stop stream (6)
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.audiocontext.terminate()
        self.audiocontext = None
        wf.close()

    def OnProcessing(self):
        
        def Process(filename, counter):
            Robotize(filename, "take" + str(counter) + "-robot.wav")
            ExtractMelody(filename, "take" + str(counter) + "-melody.wav")
            Stretch(filename, "take" + str(counter) + "-slower.wav", 0.5)
            Stretch(filename, "take" + str(counter) + "-faster.wav", 2.0)
            self.window.waitingFlag = False


        self.processThread = threading.Thread(target=Process, args=(self.filename, self.counter))
        self.processThread.start()


app = Main()
Gtk.main()
