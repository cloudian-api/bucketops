#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script lists all buckets owned by a particular user specified in clusterconfig.py.

import sys
import clusterconfig as C

# Print usage messages.
def PrintUsage():

    print ("<Usage>: <{}>".format(sys.argv[0]))
    print ("List all buckets belonging to a particular user.")
    return

def list_buckets(mycluster):
    mybuckets=[]
    ret={}
    count=0
    for bucket in mycluster.s3.buckets.all():
        mybuckets.append(bucket.name)
        count = count + 1;
    status,resp = mycluster.get_bucketsstorage_policies()
    if (status != 200):
        print("Cannot get bucket storage policies: ",resp)
        return(-1,ret)
    # Initialize ret dictionary. Key is the bucket name, value will be policy name and policy ID.
    for m in mybuckets:
        ret[m] = ""
    for bperpolicy in resp:
        pname=""
        pid=""
        append_dict={}
        items = bperpolicy.items()
        for item in items:
            key = item[0]
            value = item[1]
            if (key == "policyName"):
              pname = value
            elif (key == "policyId"):
                pid = value
            else:
                # key is "buckets". This is a list of buckets which have the same storage policy.
                # Find the intersection of this list with our list of buckets (mybuckets)
                bucket_list = value
                intersection = list(set(mybuckets).intersection(set(bucket_list)))
                # Now loop through the intersection list and update our return dictionary.
                for i in intersection:
                    ret[i] = pname + ";" + pid
    return(count,ret)

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

    count,ret = list_buckets(mycluster)
    if (count < 0):
        print("Failed!")
        sys.exit(1)
    print("Number of buckets: ", count)
    for bucket in sorted(ret):
        pname,pid = ret[bucket].split(';')
        print ("Bucket: {:<32} policyName: {:<32} policyId: {:>32}".format(bucket,pname,pid))
    sys.exit(0)
