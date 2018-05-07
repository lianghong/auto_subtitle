#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Writen by Lianghong  2018-04-23 11:41:22

import json
import re
import math
import urllib.request

def has_attribute(data, attribute):
    return attribute in data and data[attribute] is not None

def convert_time(raw_time):
    p = re.compile("(\d+)\.(\d+)")
    m = p.match(raw_time)
    if m:
        sec = int(m.group(1))
        ms = int(m.group(2))
    else:
        return "{}:{}:{},{}".format(0, 0, 0, 0)

    second = (int(sec) % 60)
    minute = int(math.floor(float(sec) / 60) % 60)
    hour = int(math.floor(float(sec) / 3600))
    return "{}:{}:{},{}".format(hour, minute, second, ms)

def get_time(time_value):
    p = re.compile("(\d+):(\d+):(\d+),(\d+)")
    m = p.match(time_value)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        return 0, 0, 0

def get_time_difference(start_time, end_time):
    start_hour, start_min, start_sec = get_time(start_time)
    end_hour, end_min, end_sec = get_time(end_time)
    return ((end_hour * 3600 + end_min * 60 + end_sec) -
            (start_hour * 3600 + start_min * 60 + start_sec))

def output_srt(target_file, counter, start_time, end_time, content):
    separator = '-->'
    target_file.write("{}\n{} {} {}\n{}\n\n".
                      format(counter, start_time, separator, end_time, content))

def convert_json(json_url, srt_file):
    counter = 1
    content = ""
    start_time = ""
    threshold_time = 3
    threshold_length = 20

    response = urllib.request.urlopen(json_url)
    raw_data = response.read()
    encoding = response.info().get_content_charset('utf-8')

    json_data = json.loads(raw_data.decode(encoding))['results']['items']
    transcript_data = json.loads(raw_data.decode(encoding))['results']['transcripts']
    with open("transcripts.en.txt", "w") as transcript_file:
        for item in transcript_data:
            for value in item['transcript']:
                transcript_file.write(value)

    dest_file = open(srt_file, 'w')

    for item in json_data:
        if has_attribute(item, 'alternatives'):
            for value in item['alternatives']:
                if has_attribute(item, 'start_time'):
                    content += " {}".format(value['content'])
                else:
                    content += value['content']

        if has_attribute(item, 'end_time'):
            end_time = convert_time(item['end_time'])

        if has_attribute(item, 'start_time') and start_time == "":
            start_time = convert_time(item['start_time'])

        if has_attribute(item, 'alternatives') and not has_attribute(item, 'start_time'):
            if (get_time_difference(start_time, end_time) > threshold_time and len(content) > threshold_length):
                output_srt(dest_file, counter, start_time, end_time, content)
                counter += 1
                start_time = ""
                content = ""
        elif len(content) > 50:
                output_srt(dest_file, counter, start_time, end_time, content)
                counter += 1
                start_time = ""
                content = ""
    if len(content) > 0:
        output_srt(dest_file, counter, start_time, end_time, content)
    dest_file.close()
    return 1

def main():
    jsonfile = "asrOutput.json"
    srt_file = "How we teach computers to understand pictures _ Fei Fei Li-40riCqvRoMs.srt"
    convert_json(jsonfile, srt_file)


if __name__ == "__main__":
    main()
