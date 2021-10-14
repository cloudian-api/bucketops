#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script creates a bucket that is owned by a particular user specified in clusterconfig.py.

import sys
import boto3
import clusterconfig as C


# Print usage messages.
def PrintUsage():
    
    print ("<Usage>: <{}> bucket_name".format(sys.argv[0]))
    print ("Will create a bucket with name 'bucket_name'")
    return

# Create a bucket in the current region.
def create_bucket(bucket_name,mycluster):

    session = boto3.session.Session()
    #session.region_name returns all upper case sometimes.
    current_region = session.region_name.lower()
    try:
        bucket_response = mycluster.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': current_region})
        retval = "Created: ", bucket_name + " " + "In region: ", current_region
    except Exception as ex:
        retval = ex
        bucket_response = -1
    return (bucket_response, retval)

if __name__ == "__main__":

    if (len(sys.argv) != 2):
        PrintUsage()
        sys.exit(1)

    mycluster = C.my_api(C.accesskey,C.secretkey,C.endpoint)
    status,ret = mycluster.verify_creds()
    # If status is not 0, then we weren't able to connect for some reason.
    if (status != 0):
        print("Cannot connect to HyperStore.")
        print("Did you remember to update the config file?")
        print(ret)
        sys.exit(1)

    # Now we can create the bucket.
    bucket_name = sys.argv[1]
    status, ret = create_bucket(bucket_name,mycluster)
    print (status,ret)
    sys.exit(0)
