# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.

import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Cloudian cluster details. We need these in order to log into the REST API.
# You can get these by logging into CMC as a non-admin user and then Security Credentials.
# You can also feed in the access and secret keys in the following way:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
# Another way to do this may be to read ~/.aws/credentials.
# But the keys are defined here for convenience and hopeafully better understanding.
accesskey = "your access key"
secretkey = "your secret key"
endpoint = "http://s3-<region>.<domain>"

# These variables are only used for the Admin API.
# adminIP is the IP address of any node in your HS cluster.
# Sysadmin details can be obtained by logging into HSH and:
# sudo hsctl config get admin.auth
# Please be sure to check that admin_auth_enabled is set to true as well.
adminIP="10.10.10.10"
adminApiPort=19443
adminName="sysadmin"
adminPass="your admin password"

# ============ DO NOT CHANGE ANYTHING BELOW THIS LINE ==========
class my_api():
    def __init__(self,accesskey,secretkey,endpoint):

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        try:
            self.s3 = boto3.resource('s3',aws_access_key_id=accesskey,aws_secret_access_key=secretkey,endpoint_url=endpoint)
            self.session = boto3.session.Session()
        except Exception as ex:
            print(ex)
        self.admin_url = "https://%s:%s/" %(adminIP,adminApiPort)
        self.admin_session = self.get_server_session(adminName,adminPass)

    # Very simple function to verify that our credentials are correct.
    # Ask HS for a bucket listing.
    def verify_creds(self):
        i=0
        try:
            for bucket in self.s3.buckets.all():
                if (i > 0):
                    break
                i = i + 1
                bucket_name = bucket.name
        except Exception as ex:
            return(-1,ex)
        # If we are here then we were able to connect. There were either zero buckets or at least one.
        if (i == 0): 
            return(0,"None")
        else:
            return(0,bucket_name)

    # We need an admin session only for dealing with bucket storage policies.
    def get_server_session(self, username, password):
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        return session

    # Get the signed authorization header for when we call requests().
    # Boto3 takes care of this automagically. But we need requests() for HyperStore custom headers.
    # We could follow the steps in: https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html
    # but we take the easy way out and use the requests_aws4auth library instead.
    def get_auth_string(self,region):

        return(AWS4Auth(accesskey,secretkey,region,"s3"))

    # Get storage policies.
    def get_storage_policies(self):
        bpolicy_url = self.admin_url + "bppolicy/listpolicy"
        try:
            server_response = self.admin_session.get(bpolicy_url)
            return(server_response.status_code,json.loads(server_response.text))
        except Exception as ex:
            print(ex)
            return(-1,bpolicy_url)

    # Get buckets per storage policy.
    def get_bucketsstorage_policies(self):
        bpolicy_url = self.admin_url + "bppolicy/bucketsperpolicy"
        try:
            server_response = self.admin_session.get(bpolicy_url)
            return(server_response.status_code,json.loads(server_response.text))
        except Exception as ex:
            print(ex)
            return(-1,bpolicy_url)    

    # List storage policies by policyname and policyID.
    def list_storage_policies(self,storage_policies):
        for storage_policy in storage_policies:
            items = storage_policy.items()
            for item in items:
                key = item[0]
                value = item[1]
                if (key == "policyName"):
                    print("PolicyName: ",value)
                elif (key == "policyId"):
                    print("PolicyID: ",value)
            print("******************************************")
        return(0)

    # Get default storage policy of cluster.
    def get_default_storage_policy(self):
        status,resp = self.get_storage_policies()
        # If we can't connect we send back a dummy name for the storage policy.
        if (status != 200):
            print("Cannot connect to ",resp)
            return("@@@",-1)
        storage_policies = resp
        found=False
        for storage_policy in storage_policies:
            if (found is True):
                break
            items = storage_policy.items()
            pname=""
            pid=""
            for item in items:
                key = item[0]
                value = item[1]
                if (key == "systemDefault" and value is True):
                    found=True
                if (key == "policyName"):
                    pname = value
                elif (key == "policyId"):
                    pid = value
        return(pname,pid)
