#!/usr/bin/env python

import boto3
import sys

if len(sys.argv) != 3:
    print("Usage: start/stop %s Instance_ID/Name" % sys.argv[0])
    exit()

client = boto3.client('ec2')
response = client.describe_instances() 
instance_id = False

for item in response['Reservations']:
    for list in item['Instances']:
        name = str(list['Tags'][0]['Value'])
	id = str(list['InstanceId'])	

        if name == sys.argv[2]:
            instance_id = id

if not instance_id:
    instance_id = sys.argv[2]

if sys.argv[1] == 'start':

    response = client.start_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False
    )

elif sys.argv[1] == 'stop':
    
    response = client.stop_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False,
        Force=True
    )

elif sys.argv[1] == 'terminate':
    response = client.terminate_instances(
	InstanceIds=[
	    instance_id,
	],
	DryRun=False
    )

print(response)
