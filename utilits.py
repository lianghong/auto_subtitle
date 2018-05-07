#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Writen by Lianghong  2018-04-25 15:16:08

import os
import time
import datetime
import moviepy.editor as mp
import s3_utilits

sampling_rate = 44100

def split_filename(filename):
    ext = filename.split(".")[-1]
    base = os.path.basename(filename).split('.')[0]
    return base, ext

def gen_audiofilename(filename):
    audio_ext = 'mp3'
    return gen_filename(filename, audio_ext)

def gen_srtfilename(filename):
    srt_ext = 'srt'
    return gen_filename(filename, srt_ext)

def gen_filename(filename, ext):
    base, _ = split_filename(filename)
    return '.'.join([base, ext])

def extract_audio(videofilename):
    audio_bitrate = '50k'
    audio_filename = gen_audiofilename(videofilename)
    if not os.path.exists(audio_filename):
        clip = mp.VideoFileClip(videofilename, audio=True)
        clip.audio.write_audiofile(
            audio_filename, bitrate=audio_bitrate,
            fps=sampling_rate, write_logfile=False,
            verbose=False, progress_bar=False)
        print("Extract audio file {}".format(audio_filename))
    return audio_filename

def gen_jobname():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H.%M.%S')
    return "".join(['myJob_', st])


