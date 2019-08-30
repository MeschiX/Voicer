#! /usr/bin/env python

from aubio import source, sink, pvoc


def Robotize(inputfilename, outputfilename):

    samplerate = 44100
    f = source(inputfilename, samplerate, 256)
    g = sink(outputfilename, samplerate)
    total_frames, read = 0, 256

    win_s = 512                          # fft size
    hop_s = win_s // 2                   # hop size
    pv = pvoc(win_s, hop_s)              # phase vocoder

    while read:
        samples, read = f()
        spectrum = pv(samples)           # compute spectrum
        # spectrum.norm *= .8             # reduce amplitude a bit
        spectrum.phas[:] = 0.            # zero phase
        new_samples = pv.rdo(spectrum)   # compute modified samples
        g(new_samples, read)             # write to output
        total_frames += read

    format_str = "read {:d} samples from {:s}, written to {:s}"
    print(format_str.format(total_frames, f.uri, g.uri))
