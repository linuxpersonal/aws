#!/usr/bin/python3

import boto3
import argparse
import sys

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', '--securityid', nargs=1, required=True,
                        help='Insert Security ID')
    parser.add_argument('-l', '--list', action="store_true",
                        help='List Security Group Rules')
    parser.add_argument('-a', '--add', nargs=1,
                        help='Insert Port (Open incoming port)')
    parser.add_argument('-rm', '--revoke', nargs=1,
                        help='Insert Port (Revoke incoming port)')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()

def sc_list(sc_id):

    try:
        print('\nSecurity Group Rules for %s:\n' % sc_id)
        response = ec2.describe_security_groups(GroupIds=[sc_id])
        for rules in response['SecurityGroups']:
            for i in rules['IpPermissions']:
                print("From Port: " + str(i['FromPort']) + "    To Port: "\
                      + str(i['ToPort']) + "     Source "\
                      + str(i['IpRanges'][0]['CidrIp']))
        print("")
    except Exception as e:
        print(e)

def add_rule(port):
    response = security_group.authorize_ingress(
	IpProtocol='tcp',
	FromPort=port,
	ToPort=port,
	CidrIp="0.0.0.0/0",
	DryRun=False
    )

    return(response)

def revoke_rule(port):
    response = security_group.revoke_ingress(
	IpProtocol='tcp',
	FromPort=port,
	ToPort=port,
	CidrIp="0.0.0.0/0",
	DryRun=False
    )

    return(response)

def main():
    
    arg = parse_input()
    sc_id = arg.securityid[0]

    ec2_one = boto3.resource('ec2')

    global ec2
    ec2 = boto3.client('ec2')
    
    global security_group
    security_group = ec2_one.SecurityGroup(sc_id)

    if arg.list:
        sc_list(sc_id)
    elif arg.add:
        add_port = int(arg.add[0])
        print(add_rule(add_port))
    elif arg.revoke: 
        revoke_port = int(arg.revoke[0])
        print(revoke_rule(revoke_port))

if __name__ == '__main__':
    main()
