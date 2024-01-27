#!/bin/env python3
import logging
import os
import tempfile

import boto3
import yt_dlp
from botocore.exceptions import ClientError


def handler(event, context):
    download_url = event["queryStringParameters"]["url"]

    if download_url is None or download_url == "":
        return "bad url :("

    bucket_name = os.environ["S3Bucket"]
    presigned_urls = []
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        yt_dlp._real_main(argv=[f"{download_url} -o %(title)s.%(ext)s"])
        for ytfile in os.listdir(tmp):
            upload_file(f"{tmp}/{ytfile}", bucket_name)
            presigned_urls.append(create_presigned_url(bucket_name, ytfile))

    return presigned_urls


def create_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
