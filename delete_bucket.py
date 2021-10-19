#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script deletes a bucket owned by a particular user specified in clusterconfig.py.

import sys
import clusterconfig as C


# Print usage messages.
def PrintUsage():

    print ("<Usage>: <{}> <bucket name>.".format(sys.argv[0]))
    print ("Delete bucket with name <bucket name>.")
    return

def delete_bucket(bucket_name,mycluster):
    try:
        mycluster.s3.Bucket(bucket_name).delete()
    except Exception as ex:
        return(-1,ex)
    return(0, 0)


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
        sys.exit

    # Now we can delete the bucket.
    bucket_name = sys.argv[1]
    status,ret = delete_bucket(bucket_name,mycluster)
    if (status != 0):
        print("Could not delete bucket: ",bucket_name)
        print(ret)
    sys.exit(0)

