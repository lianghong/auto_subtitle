#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Writen by Lianghong  2018-04-25 14:17:31

import boto3
import re

def init_translate(region):
    translate = boto3.client(service_name='translate',
                             region_name=region,
                             use_ssl=True)
    return translate

def translate_text(translater, source,source_language, target_language):
    result = translater.translate_text(
        Text=source, SourceLanguageCode=source_language,
        TargetLanguageCode=target_language)
    return result.get('TranslatedText')


def translate_file(translater, source_file,source_language,dest_file,dest_language):
    source = open(source_file,"r")
    dest = open(dest_file,"w")

    original = source.read()
    sentences = [s.strip() for s in re.split('[\.\?!]' , original) if s]
    sentence = "" 
    for l in sentences:
        if len(l) + len(sentence) < 1000:
            sentence +=l
            sentence +="。"
        else:
            sentence += "\n"
            print(sentence)
            sen_translated = translate_text(translater, sentence, source_language, dest_language)
            sentence = l
            print(sen_translated)
            dest.write(sen_translated)

    dest.write("。")
    dest.close()
    source.close()


if __name__ == '__main__':
    region = "us-west-2"
    source = "transcripts.en.txt"
    dest ="transcripts.zh.txt"

    translater = init_translate(region)
    translate_file(translater, source, "en", dest, "zh")


