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
count = 1

if sys.argv[1] == 'list':
    
    print("")
    for item in response['Reservations']:

        for list in item['Instances']:
            
            ec2_state = str(list['State']['Name'])
            ec2_id = str(list['InstanceId'])

            if ec2_state == "terminated":
                print("Instance %s has been terminated\n" 
                      % ec2_id)
                break
            
            ec2_vpcid = str(list['VpcId'])
            ec2_privateip = str(list['PrivateIpAddress'])
            ec2_subnetid = str(list['SubnetId'])
            ec2_sc = str(list['SecurityGroups'][0]['GroupName'])
            
            try: ec2_name = str(list['Tags'][0]['Value'])
            except: ec2_name = "No Tag Name Assigned"
            
            try: ec2_pubip = str(list['PublicIpAddress'])
            except: ec2_pubip = str("Public IP Not Assigned")


            print('Node ' + str(count) + "\nName: " + ec2_name)
            print('Instance ID: ' + ec2_id)
            print('Security Group: ' + ec2_sc)
            print("State: " + ec2_state)
            print("VPC: " + ec2_vpcid)
            print("Subnet: " + ec2_subnetid)
            print("Private IP: " + ec2_privateip)
            print("Public IP: " + ec2_pubip)
            print("")

            count += 1

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
