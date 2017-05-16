from s3config import AWS_S3_KEY, AWS_S3_SECRET
from datetime import datetime
import boto3
import botocore

import logging
import logging.config
import os
import sys
from time import time


logging.config.fileConfig('log_config.ini',defaults={'logfilename':'apilogs/uploads/state_of_union.log'})
logger = logging.getLogger(__name__)

# Session is made for custom session towards some region?
# FROM: http://stackoverflow.com/questions/33577503/how-to-configure-authorization-mechanism-inline-with-boto3#answer-33668804
session = boto3.session.Session(region_name="eu-central-1")

client = boto3.client('s3',
                       aws_access_key_id=AWS_S3_KEY,
                       aws_secret_access_key=AWS_S3_SECRET,
                       config=boto3.session.Config(signature_version="s3v4"))
s3 = boto3.resource("s3")


if __name__ == "__main__":
    '''
    buckets = [bucket['Name'] for bucket in client.list_buckets()['Buckets']]
    print(", ".join(buckets))

    for bucket in s3.buckets.all():
        print(bucket.name, sep=", ")

    for k in client.list_objects(Bucket='elz')['Contents']:
        print(k['Key'])
    '''
    
    start = time()

    # list all files in logs directory
    logfiles = os.listdir('logs')

    for logfile in logfiles:
        file_to_upload = os.path.join(os.getcwd(), 'logs', logfile) 
        filename = file_to_upload.split('/')[-1]
        
        try:
            #FROM: http://stackoverflow.com/questions/42008288/upload-file-to-amazon-cloud-subfolder-using-python-boto3#answer-42008433
            client.upload_file(file_to_upload, "elz", f"sb_logs/{filename}")
            os.unlink(file_to_upload)
            end = time() - start
            logger.info(f"Uploaded {filename} to AWS S3 for {end:.4f} sec.")

        except botocore.exceptions.ClientError as e:
            logger.warning(f"Problem with S3: {e}")
            sys.exit(1)
