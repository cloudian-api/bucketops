# DISCLAIMER: This script is not officially supported by Cloudian. Please contact
# cariapa@gmail.com if you have any questions.

import boto3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Cloudian cluster details. We need these in order to log into the REST API.
# You can get these by logging into CMC as a non-admin user and then Security Credentials.
# You can also feed in the access and secret keys in the following way:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
accesskey = "some access key"
secretkey = "some secret key"
endpoint = "http://s3-<region>.<domain>"

# ============ DO NOT CHANGE ANYTHING BELOW THIS LINE ==========
class my_api():
    def __init__(self,accesskey,secretkey,endpoint):
        self.s3 = boto3.resource('s3',aws_access_key_id=accesskey,aws_secret_access_key=secretkey,endpoint_url=endpoint)

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

