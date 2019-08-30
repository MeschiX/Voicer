#! /usr/bin/env python

import sys
import wave, struct, math
from aubio import source, notes


def ExtractMelody(filename, outputfilename):

    def midi2Hz(d):
        f = 2**((d-69)/12)
        f *= 440
        return f



    downsample = 1
    samplerate = 44100 // downsample

    win_s = 512 // downsample # fft size
    hop_s = 256 // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    wavef = wave.open(outputfilename,'w')
    wavef.setnchannels(1) # mono
    wavef.setsampwidth(2) 
    wavef.setframerate(samplerate)

    notes_o = notes("default", win_s, hop_s, samplerate)
    notes_o.set_silence(-40)

    print("%8s" % "time","[ start","vel","last ]")

    samenotecounter = 1
    lastnote = 0
    lastvelocity = 0
    volumeunit = 32767 / 127
    # total number of frames read
    total_frames = 0


    while True:
        
        samples, read = s()
        new_note = notes_o(samples)

        if (new_note[0] != 0):

            for i in range(int(hop_s)*samenotecounter):
                value = int(volumeunit*lastvelocity*math.sin(2*lastnote*math.pi*float(i)/float(samplerate)))
                data = struct.pack('<h', value)
                wavef.writeframesraw( data )

            samenotecounter = 1
            lastnote = midi2Hz(new_note[0])
            lastvelocity = new_note[1]

            print("%.6f" % (total_frames/float(samplerate)), new_note[0], new_note[1])

        else:

            samenotecounter += 1

            total_frames += read

        if read < hop_s: 

            for i in range(int(hop_s)*samenotecounter):
                value = int(volumeunit*lastvelocity*math.sin(2*lastnote*math.pi*float(i)/float(samplerate)))
                value = value % 32766
                data = struct.pack('<h', value)
                wavef.writeframesraw( data )

            break

    wavef.close()
