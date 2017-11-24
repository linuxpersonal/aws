#!/usr/bin/env python

import boto3
import sys

s3 = boto3.resource('s3')
client = boto3.client('s3')

for buckets in s3.buckets.all():
    print("Buckets: ")
    print buckets

if len(sys.argv) < 3:
    print('Usage: add/remove object_name bucket_name')
    exit()
elif len(sys.argv) == 4:
    action = sys.argv[1]
    copyfile = sys.argv[2]
    bucket_name = sys.argv[3]
elif len(sys.argv) == 3:
    action = sys.argv[1]
    bucket_name = sys.argv[2]

if action == 'add':
    
    try:
        with open(copyfile, 'rb') as data:
            client.upload_fileobj(data, bucket_name, copyfile)
        print("Inserting %s into bucket %s" % (copyfile, bucket_name))
    except Exception as e:
        print(e)

elif action == 'remove':
    
    try:
        response = client.delete_object(
                Bucket = bucket_name,
                Key = copyfile
                )
        print(response)
    except Exception as e:
        print(e)

elif action == 'list':

    response = client.list_objects(
	Bucket=bucket_name
    )

    print('\nListing Contents for bucket %s\n' % bucket_name)

    for i in response['Contents']:
	print("%s" % i['Key'])

    print('')
