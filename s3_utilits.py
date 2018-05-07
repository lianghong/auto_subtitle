#!/usr/bin/env python3

# -*- coding:utf-8 -*-
# Writen by Lianghong  2018-01-04 17:08:30

import boto3
import botocore
import urllib.parse
import utilits

expiration = 604800

def init_s3_client():
     return boto3.client('s3')
    
def gen_s3key(filename):
    base, ext = utilits.split_filename(filename)
    return ".".join([base, ext]).replace(' ', '+')

def upload_to_s3(client, filename, bucket):
    try:
        print("Uploading file:", filename)
        key = gen_s3key(filename)
        if not check_object_existing(client, bucket, key):
            tc = boto3.s3.transfer.TransferConfig()
            tf = boto3.s3.transfer.S3Transfer(client=client,
                                            config=tc)
            tf.upload_file(filename, bucket, key)
        uri = client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expiration)
    except Exception as e:
        print(e)
    return uri

def check_object_existing(client, bucket, key):
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            print("object existing")
            return obj['Size']

def get_object_public_url(client, bucket, key):
    config = client._client_config
    config.signature_version = botocore.UNSIGNED
    return boto3.client('s3', config=config).generate_presigned_url(
        'get_object', ExpiresIn=0, Params={'Bucket': bucket, 'Key': key})

def gen_object_url(region, bucket, key):
    return "https://s3-{}.amazonaws.com/{}/{}".format(region, urllib.parse.quote(bucket), urllib.parse.quote(key))


if __name__ == '__main__':
    filename = "How we teach computers to understand pictures _ Fei Fei Li-40riCqvRoMs.mp3"
    bucket = "transcribe-audio"
    region = "us-west-2"

    s3 = boto3.client('s3')
    upload_to_s3(s3, filename, bucket)
    url = gen_object_url(region, bucket, gen_s3key(filename))
