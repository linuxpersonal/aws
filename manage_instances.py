#!/usr/bin/env python

import boto3
import sys
import argparse

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
response = client.describe_instances() 

def parse_input():

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        help="List Instances", action="store_true")
    parser.add_argument('-s', '--start', nargs=1,
                        help="Insert Instance Name/ID start instance")
    parser.add_argument('-d', '--stop', nargs=1,
                        help="Insert Instance Name/ID to stop instance")
    parser.add_argument('-t', '--terminate', nargs=1,
                        help="Insert Instance Name/ID to terminate instance")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def ec2_list():
    
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
            ec2_scid = str(list['SecurityGroups'][0]['GroupId'])
            
            try: ec2_name = str(list['Tags'][0]['Value'])
            except: ec2_name = "No Tag Name Assigned"
            
            try: ec2_pubip = str(list['PublicIpAddress'])
            except: ec2_pubip = str("Public IP Not Assigned")


            print("Name: " + ec2_name)
            print('Instance ID: ' + ec2_id)
            print('Security Group: ' + ec2_sc + " (%s)" % ec2_scid)
            print("State: " + ec2_state)
            print("VPC: " + ec2_vpcid)
            print("Subnet: " + ec2_subnetid)
            print("Private IP: " + ec2_privateip)
            print("Public IP: " + ec2_pubip)
            print("")

def get_instance_id(instance_identifier):

    instance_id=False

    for item in response['Reservations']:
        for list in item['Instances']:
            name = str(list['Tags'][0]['Value'])
            id = str(list['InstanceId'])	

            if name == instance_identifier:
                instance_id = id

    if not instance_id:
        instance_id = instance_identifier

    return(instance_id)

def ec2_start(instance_identifier):
    
    instance_id = get_instance_id(instance_identifier)

    response = client.start_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False
    )
    print("Instance %s started" % instance_id)

def ec2_stop(instance_identifier):
    
    instance_id = get_instance_id(instance_identifier)

    response = client.stop_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False,
        Force=True
    )
    print("Instance %s stopped" % instance_id)

def ec2_terminate(instance_identifier):

    instance_id = get_instance_id(instance_identifier)
    
    response = client.terminate_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False
    )
    print("Instance %s terminated" % instance_id)

def main():

    arg=parse_input()

    if arg.list:
        ec2_list()
    elif arg.start:
        instance_identifier = arg.start[0]
        ec2_start(instance_identifier)
    elif arg.stop:
        instance_identifier = arg.stop[0]
        ec2_stop(instance_identifier)
    elif arg.terminate:
        instance_identifier = arg.terminate[0]
        ec2_terminate(instance_identifier)


if __name__ == '__main__':
    main()
