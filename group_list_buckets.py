#!/usr/local/bin/python
# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.
# This script takes the name of a group, gets all the users in that group and lists buckets owned by those users.
# You can use the GET /usage admin API call to get utilization by group, by specifying a time-period.

import sys
import requests
import clusterconfig as C

# Get a username, and list buckets for that username.
def my_list_buckets(username,group,mycluster):

    # Get the credentials of a particular user in the group that was specified on the command line.
    my_url = mycluster.admin_url + "user/credentials/list?userId=" + username + "&groupId=" + group
    try:
        r = mycluster.admin_session.get(my_url)
        r.raise_for_status()
    # If we get an unsuccessful status code, bail out here.
    except Exception as ex:
        print(ex)
        return(1)

    # If len of the text response we got is zero we got a successful status code but no output!
    # Maybe we're trying to get admin creds which is forbidden.
    if (len(r.text) == 0):
        print("Got empty response for user credentials for user: {} from group {}.".format(username,group))
        return(1)
    secInfo = r.json()[0]
    akey = secInfo['accessKey']
    skey = secInfo['secretKey']
    
    # Here we are over-riding the credentials in clusterconfig and running as another user!
    temp_cl = C.my_api(akey,skey,C.endpoint)
    response_b = temp_cl.s3_client.list_buckets()
    print(">>>> Bucket listing for user {} from group {}.".format(username,group))
    list_of_buckets = response_b['Buckets']
    # In addition to printing the bucket name you could print the utilization here also.
    # so call the admin URL with GET /usage.
    for x in list_of_buckets:
        bucket_name = x['Name']
        print("****** ",bucket_name)
    return(0)

if __name__ == "__main__":

    if (len(sys.argv) != 2):
        print ("<Usage>: <{}> <group name>".format(sys.argv[0]))
        print ("Where <group name> is a group on your HyperStore cluster.")
        sys.exit(1)

    group = sys.argv[1]
    mycluster = C.my_api(C.accesskey,C.secretkey,C.endpoint)
    status,ret = mycluster.verify_creds()
    # If status is not 0, then we weren't able to connect for some reason.
    if (status != 0):
        print("Cannot connect to HyperStore.")
        print("Did you remember to update the config file?")
        print(ret)
        sys.exit(1)

    # Get the list of users in the group.
    my_url = mycluster.admin_url + "user/list?groupId=" + group + "&userType=all&userStatus=active"
    r = mycluster.admin_session.get(my_url)
    list_of_users = r.json()
    if (len(list_of_users) == 0):
        print("No users found in group {}. Did you mis-spell it?".format(group))
        sys.exit(1)
    retval = 1
    for x in list_of_users:
        retval = my_list_buckets(x['userId'],group,mycluster)
        # if we ran into an error bail out so we can correct the issue.
        if retval != 0:
            print("Ran into some error..bye")
            break
    
    # Print this if we got some successful output.
    if retval == 0:
        print("Please use GET /usage to get utilization status over a particular period.")
    
    sys.exit(0)
