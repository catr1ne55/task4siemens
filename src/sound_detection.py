from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy.signal import fftconvolve


def similarity(template, test):
    corr = fftconvolve(template, test, mode='same')

    return corr


def record_audio(fs=44100, duration=5):
    """
     Recording audio from the microphone.

    :param fs: the frequency of the recorded signal
    :param duration: the duration of the recorded signal
    :return: the recording, type: numpy.ndarray
    """

    print(f"Recording audio for the next {duration} sec.")
    dfs = duration * fs
    recording = sd.rec(dfs, samplerate=fs, channels=1,dtype='float64')
    sd.wait()
    print("Audio recording is completed.")
    return recording.reshape((dfs, ))


def read_audio(path):
    """
    Read audiofile by the given path.

    :param path: the path of the file
    :return: audiosignal
    """

    input_data = read(path)
    audio = input_data[1]
    return audio


def cross_correlation(audio, sound):
    """
    Compute the cross correlation value of two signals.

    :param audio: array, representing the given audio
    :param sound: array, representing the reference sound
    :return: correlation values
    """

    maxVA = np.max(np.abs(audio))
    vA = audio / maxVA

    refVA = sound / np.max(np.abs(sound))

    vTestSignal = vA
    vRefSignal = refVA

    numSamplesTestSignal = np.size(vTestSignal)
    numSamplesRefSignal = np.size(vRefSignal)

    vCrossCorrelationVal = np.zeros(numSamplesTestSignal - numSamplesRefSignal + 1)

    for ii in range(np.size(vCrossCorrelationVal)):
        vTestSignalSamples = vTestSignal[ii:(ii + numSamplesRefSignal)]
        vCrossCorrelationVal[ii] = np.dot(vTestSignalSamples, vRefSignal)

    return vCrossCorrelationVal


def display(audio, reference, correlation, name='Plot.png'):
    """
    Plots the given audio with intervals where the reference sound appears.

    :param audio: array, representing the given audio
    :param reference: array, representing the reference sound
    :param correlation: array, containing the correlation values
    :param name: Name of file with the plot.
    :return: None
    """

    plt.plot(audio, 'black')
    crossCorrelationMax = np.argmax(np.abs(correlation))

    plt.axvspan(crossCorrelationMax, crossCorrelationMax + np.size(reference), facecolor='r')
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Sample Wav")
    plt.savefig(name)
