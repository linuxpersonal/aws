#!/usr/bin/env python

import boto3
import sys
import argparse

s3 = boto3.resource('s3')
client = boto3.client('s3')

def parse_input():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket', nargs=1, required=True,
                        help="Insert s3 Bucket Name")
    parser.add_argument('-l', '--list',
                        help="List Users", action="store_true")
    parser.add_argument('-a', '--add', nargs=1,
                        help="Insert file name to add(Add to s3)")
    parser.add_argument('-d', '--delete', nargs=1,
                        help="Insert file name to remove (Remove from s3)")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()

def s3_add(copyfile, bucket_name):

    try:
        with open(copyfile, 'rb') as data:
            client.upload_fileobj(data, bucket_name, copyfile)
        print("Inserting %s into bucket %s" % (copyfile, bucket_name))
    except Exception as e:
        print(e)

def s3_delete(deletefile, bucket_name):

    try:
        response = client.delete_object(
                Bucket = bucket_name,
                Key = deletefile
                )
        print("Removing %s from bucket %s" % (deletefile, bucket_name))
    except Exception as e:
        print(e)

def s3_list(bucket_name):

    for buckets in s3.buckets.all():
        print("All Buckets in AWS profile: ")
        print buckets

    response = client.list_objects(
	Bucket=bucket_name
    )

    print('\nListing Contents for bucket %s\n' % bucket_name)

    for i in response['Contents']:
	print(i['Key'])

    print('')


def main():

    arg=parse_input()
    bucket = arg.bucket[0]

    if arg.list:
        s3_list(bucket)
    elif arg.add:
        s3_file = arg.add[0]
        s3_add(s3_file, bucket)
    elif arg.delete:
        s3_file = arg.delete[0]
        s3_delete(s3_file, bucket)

if __name__ == '__main__':
    main()
