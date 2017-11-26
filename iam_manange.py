#!/usr/bin/env python

import boto3
import sys
import argparse

iam = boto3.client('iam')

def parse_input():

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        help="List Users", action="store_true")
    parser.add_argument('-a', '--add', nargs=1,
                        help="Insert IAM Username (Create IAM User)")
    parser.add_argument('-d', '--delete', nargs=1,
                        help="Insert IAM Username (Create IAM User)")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()

def list_users():

    list = iam.get_paginator('list_users')

    for users in list.paginate():
        print('\nUsername: %s' % users['Users'][0]['UserName'])
        print('Date Created: %s\n' % users['Users'][0]['CreateDate'])

def add(username):

    response = iam.create_user(UserName=username)
    print(response)

def delete(username):

    response = iam.delete_user(UserName=username)
    print(response)

def main():

    arg = parse_input()

    if arg.list: list_users()
    elif arg.add: add(arg.add[0])
    elif arg.delete: delete(arg.delete[0])


if __name__ == '__main__':
    main()
