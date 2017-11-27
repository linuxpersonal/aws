#!/usr/bin/python3

import subprocess

def print_options():

    print("\nScript for changing AWS API Profiles, please choose a profile\n")
    print("1. Default")
    print("2. Personal\n")

def change_profile(profile):

    if profile == 1:
        access_key = "" # Insert Access Key Here
        secret_access_key = "" # Insert Secret Access Key here

    elif profile == 2:
        access_key = "" # Insert Access Key Here
        secret_access_key = "" # Insert Secret Access Key here

    return('''[default]
aws_access_key_id = %s
aws_secret_access_key = %s''' % (access_key, secret_access_key))

def write_to_file(profile):
    
    location = "/root/.aws/credentials"
    content = change_profile(profile)

    try:
        with open(location, 'w') as f:
            f.write(content)
        
        subprocess.call(['chmod', '0600', location])

        print("\nProfile changed to profile %s\n" % profile)

    except: print("Unable to write to file")

def main():

    print_options()
    choose = int(input("Enter profile number: "))
    write_to_file(choose)

if __name__ == '__main__':
    main()
