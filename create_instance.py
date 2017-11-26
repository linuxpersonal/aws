#!/usr/bin/python3

import boto3
import argparse
import sys

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def parse_input():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=1,
                        help='Insert Tag Name (Create Instance from AMI)')
    parser.add_argument('-t', '--terminate', nargs=1,
                        help='Insert VPC ID (Destroy/Terminate Instance)')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()

def create(ec2_tagname):

    instance = ec2.create_instances(
	ImageId='ami-1a668878',
	MinCount=1,
	MaxCount=1,
	InstanceType='t2.micro',
	TagSpecifications=[
	    {
            'ResourceType': 'instance',
	    'Tags': [
                {'Key': 'Name',
                 'Value': ec2_tagname},
		    ]
	    },
	  ]
	)

    return(instance[0].id)

def terminate(ec2_terminate):
    
    terminated = []
    for i in ec2_terminate:
        response = client.terminate_instances(
                InstanceIds=[
                    ec2_terminate
                    ]
                )
        terminated.append(i)
    return(i)

def main():
    
    arg = parse_input()
    if arg.create:
        print(create(arg.create[0]))
    elif arg.terminate:
        print(terminate(arg.terminate[0]))

if __name__ == "__main__":
    main()
