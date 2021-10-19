# bucketops
Scripts that manipulate buckets on Cloudian.
More for information regarding the Cloudian HyperStore REST API, please browse sections 11 through 16 of the manual.

You will need Python, I used version 3.9.7. Also the boto3 Python library (AWS SDK): 
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

You will also need the requests library and the requests_aws4auth library. So:

pip install requests

pip install requests_aws4auth

To clone this repo, navigate to the folder of your choice and type:
git clone git://github.com/cloudian-api/bucketops

Here is a description of the files in this repo:
* clusterconfig.py contains variables and common functions used in the code. It is a Python module. You will need to update the variables above the line in order to get the programs to work.

* create_bucket.py takes various arguments:
   * Without any parameters it outputs all the storage policies you have configured on HyperStore. You will need the policy ID of a particular storage policy for the next step. Remember, a storage policy has a policy name and a policy ID.
   * With a bucket name and a policy ID (which you obtained from the previous step) it will create a bucket with the corresponding storage policy.
   * With just a bucket name (one parameter) it will create a bucket with the default storage policy, whatever it is defined to be.
  Creating a bucket with a particular storage policy is a custom extension to the S3 API by HyperStore. It is implemented in create_bucket.py by utilizing the requests library. All buckets are created in the current region as returned by boto3. An exercise could be to modify the create_bucket() function to take a region as a parameter.

* list_buckets.py lists all buckets owned by a user specified in clusterconfig.py.

* delete_bucket.py deletes a bucket owned by a user specified in clusterconfig.py.
