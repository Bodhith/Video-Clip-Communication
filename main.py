from ffpyplayer.player import MediaPlayer
from moviepy.editor import *

import speech_recognition as sr
import numpy as np
import subprocess
import ffmpeg
import pickle
import cv2
import os

#====================================================================================
#====================================================================================


def SplitVideos(personName, word, startTime, endTime):

    stream = ffmpeg.input('trim_sample.mp4', ss=(startTime/96.5), t=((endTime/96.5)-(startTime/96.5))+0.5)

    stream = ffmpeg.output(stream, "CLIPS/"+personName+"_"+word+".mp4")

    ffmpeg.run(stream)


#====================================================================================


def CombineVideos(name, foundWords):

    videoClip = []

    for word in foundWords:

        videoClip.append(VideoFileClip("CLIPS/"+name+"_"+word+".mp4"))

    finialRender = concatenate_videoclips(videoClip)

    finialRender.write_videofile('combined_sample.mp4', codec='libx264')


#====================================================================================


def SaveDictonary(words):

    with open('words.pickle', 'wb') as handle:

        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)


#====================================================================================


def GetWordsFromFile():

    with open('words.pickle', 'rb') as handle:

        words = pickle.load(handle)

        return words


#====================================================================================


def GenrateClips(words, peopleNames, wantedWords):

    foundWords = []

    for name in peopleNames:

        for word in words[name]:

            if word in wantedWords:

                foundWords.append(word)

                SplitVideos(name, word, words[name][word][0], words[name][word][1])

        return foundWords


#====================================================================================


def GetWordsFromVideos():

    r = sr.Recognizer()

    words = {}

    words['trump'] = {}

    with sr.AudioFile("trim_sample.wav") as source:

        audio = r.record(source)

        decoder = r.recognize_sphinx(audio, show_all=True)

        for seg in decoder.seg():

            if seg.word.isalpha():

                words['trump'][seg.word] = (seg.start_frame, seg.end_frame)

        SaveDictonary(words)


#====================================================================================


def Main():

    peopleNames = ['trump']

    wantedWords = "what investigation going against president off minneapolis pushed destroy ukraine loud".split()

    words = GetWordsFromFile()

    foundWords = GenrateClips(words, peopleNames, wantedWords)

    CombineVideos('trump', foundWords)

    print (words, foundWords)


#====================================================================================


if __name__ == "__main__":

    Main()
