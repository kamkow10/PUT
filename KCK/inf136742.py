import scipy.io.wavfile
from numpy import *
from scipy import *
from scipy.signal import decimate
import warnings
import sys
import numpy as np


def prepareSignal(spectrum, freq, n, bitrate, decimateParam):
    fftSpectrum = fft(spectrum)
    fftSpectrum = decimate(fftSpectrum, decimateParam)
    firstHalf = fftSpectrum[0:len(freq)]
    firstAmpl = abs(firstHalf) * 2 / n

    return firstAmpl


if __name__ == "__main__":
    warnings.simplefilter("ignore")

    if len(sys.argv) != 2:
        print("Wrong number of arguments. Expected one argument.")
        sys.exit()

    bitrate, signal = scipy.io.wavfile.read(str(sys.argv[1]))
    if signal.shape.__len__() == 2:
        signal = [s[0] for s in signal]
    w = 1
    spectrum = signal[::w]
    n = len(spectrum)

    mainfreq = np.fft.fftfreq(n)
    mainfreq = abs(mainfreq * bitrate)
    mainfreq = [x for x in mainfreq if x <= 1000]

    mainampl = prepareSignal(spectrum, mainfreq, n, bitrate, 1)

    for i in range(2,6):
        ampl = prepareSignal(spectrum, mainfreq, n, bitrate, i)
        mainampl *= ampl

    maxValue = 0
    ind = 0
    for i in range(1, len(mainfreq)):
        if (mainampl[i] > maxValue) and (mainfreq[i] > 80):
            maxValue = mainampl[i]
            ind = i

    if mainfreq[ind] < 168:
        print("M")
    else:
        print("K")