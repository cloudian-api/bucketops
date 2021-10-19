#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script creates a bucket that is owned by a particular user specified in clusterconfig.py.

import re
import sys
import boto3
import clusterconfig as C
import requests
from requests_aws4auth import AWS4Auth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Print usage messages.
def PrintUsage():
    
    print ("<Usage>: <{}>")
    print ("With no arguments will display all configured storage policies.\n")
    print ("<Usage>: <{}> <bucket name>".format(sys.argv[0]))
    print ("Will create a bucket with name <bucket_name> with the default storage policy.\n")
    print ("<Usage>: <{}> <bucket name> <policy ID>".format(sys.argv[0]))
    print ("Will create a bucket with name <bucket name> with <policy ID>.")
    print ("You can get the policy ID by running the script without any arguments.")
    return

# Create a bucket in the current region. You could add a parameter to this function to deal with a region that is NOT the current region.
# We use the requests and requests_awsauth4 library here because boto3 doesn't seem to handle custom headers properly.
# Remember x-gmt-policy is a custom header that needs to be sent to Cloudian at the time of bucket creation.
# The only way to do this is via an HTTP PUT.
# We can use this approach for all HyperStore extensions to the S3 API.
def create_bucket(bucket_name,spolicy,mycluster):

    session = boto3.session.Session()
    #session.region_name returns all upper case sometimes which violates naming constraints.
    current_region = session.region_name.lower()
    auth = AWS4Auth(C.accesskey,C.secretkey,current_region,"s3")
    headers = {"x-gmt-policyid": spolicy}
    myendpoint = re.sub("http://", "http://" + bucket_name + ".", C.endpoint)
    try:
        response = requests.put(myendpoint, auth=auth, headers=headers)
        bucket_response = response.text
        retval = "Created: ", bucket_name + " " + "In region: ", current_region
    except Exception as ex:
        retval = ex
        bucket_response = -1
    return (bucket_response, retval)

if __name__ == "__main__":

    display_spolicies=False
    # Display storage policies.
    if (len(sys.argv) == 1):
        display_spolicies=True
    # Create a bucket using the default storage policy. 
    elif (len(sys.argv) == 2):
        bucket_name = sys.argv[1]
        spolicy = "default"
    # Create a bucket using the specified storage policy. 
    elif (len(sys.argv) == 3):
        bucket_name = sys.argv[1]
        spolicy = sys.argv[2]
    else:
        PrintUsage()
        sys.exit(1)

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    mycluster = C.my_api(C.accesskey,C.secretkey,C.endpoint)
    status,ret = mycluster.verify_creds()
    # If status is not 0, then we weren't able to connect for some reason.
    if (status != 0):
        print("Cannot connect to HyperStore.")
        print("Did you remember to update the config file?")
        print(ret)
        sys.exit(1)

    # Display all storage policies.
    if (display_spolicies == True):
        status, resp = mycluster.get_storage_policies()
        if (status != 200):
            print("Cannot connect to ",resp)
            print("Did you remember to update the config file?")
            sys.exit(1)
        print("******* PLEASE SPECIFY POLICYID DURING BUCKET CREATION. *******\n")
        storage_policies = resp
        mycluster.list_storage_policies(storage_policies)
        sys.exit(0)

    # If we marked the storage_policy as default, get the hex ID so we can pass it to create_bucket()
    if (spolicy == "default"):
        status,spolicy = mycluster.get_default_storage_policy()
        # "@@@" can never be a policy name as per naming rules.
        if (status == "@@@"):
            print("Failed!")
            sys.exit(1)

    # Now we can create the bucket.
    # We could check here if the bucket exists first and drop out otherwise.
    status, ret = create_bucket(bucket_name,spolicy,mycluster)
    print (status,ret)
    sys.exit(0)
