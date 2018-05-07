#!/usr/bin/env python3

# -*- coding:utf-8 -*-
# Writen by Lianghong  2018-01-04 17:08:30

import os
import sys
import argparse
import boto3
# import moviepy.editor as mp
import time
# import datetime
import utilits
import s3_utilits
import srt_utilits

def usage():
    print("python3 auto_subtitle.py --video videofilename\n")

def start_transcribe(s3obj):
    transcribe = boto3.client('transcribe', region_name=region)
    job_name = utilits.gen_jobname()
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3obj},
        MediaFormat='mp3',
        LanguageCode='en-US',
        MediaSampleRateHertz=utilits.sampling_rate
    )
    start_time = time.time()
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status == 'COMPLETED':
            transcriptFileUri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            # print(transcriptFileUri)
            break
        elif status == 'FAILED':
            print("Job failed!")
            break
        elif status == 'IN_PROGRESS':
            print("Job spend {0:.1f}sec but not ready yet, wait please...".format(time.time() - start_time))
            time.sleep(5)
    return transcriptFileUri if transcriptFileUri else None


if __name__ == '__main__':
    bucket_name = "transcribe-audio"
    region = "us-west-2"

    parser = argparse.ArgumentParser(description='Generate subtitle for your in_videofile')
    parser.add_argument("-v", "--video", dest="videofile", help="Specify your video file", required=True)
    args = parser.parse_args()

    if not args.videofile or not os.path.exists(args.videofile):
        usage()
        sys.exit(2)

    video_filename = args.videofile
    audio_filename = utilits.extract_audio(video_filename)

    s3 = s3_utilits.init_s3_client()
    s3_utilits.upload_to_s3(s3, audio_filename, bucket_name)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

    obj_url = s3_utilits.gen_object_url(region, bucket_name, s3_utilits.gen_s3key(audio_filename))
    json_url = start_transcribe(s3obj=obj_url)
    srt_utilits.convert_json(json_url, utilits.gen_srtfilename(audio_filename))
    print("Job finished.")

