#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script lists all buckets owned by a particular user specified in clusterconfig.py.

import sys
import boto3
import clusterconfig as C


# Print usage messages.
def PrintUsage():

    print ("<Usage>: <{}>".format(sys.argv[0]))
    print ("List all buckets belonging to a particular user.")
    return

def list_buckets(mycluster):
    ret_list=[]
    count=0
    for bucket in mycluster.s3.buckets.all():
        ret_list.append(bucket.name)
        count = count + 1;
    return(count, ret_list)


if __name__ == "__main__":

    if (len(sys.argv) != 1):
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

    status,ret = list_buckets(mycluster)
    print("Number of buckets: ", status)
    ret.sort()
    print(*ret, sep = "\n")
    sys.exit(0)
