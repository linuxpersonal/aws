#!/usr/bin/env python

import boto3
import sys

if len(sys.argv) != 3 and len(sys.argv) !=2:
    print("Usage: %s start/stop/list Instance_ID/Name(Not required for list)" 
          % sys.argv[0])
    exit()

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
response = client.describe_instances() 
instance_id = False

if sys.argv[1] == 'list':
    
    for instance in ec2.instances.all():
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                print "\nInstance Name: " + tag['Value']

        print "Instance ID: ", instance.id
        print "Instance State: ", instance.state['Name']
        print "Instance Code: ", instance.state['Code']

    print("")

else:
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
