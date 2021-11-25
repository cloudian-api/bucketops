# bucketops
Scripts that manipulate buckets on Cloudian.
For more information regarding the Cloudian HyperStore REST API, please browse sections 11 through 16 of the manual.

You will need Python, I used version 3.9.7. Also the boto3 Python library (AWS SDK): 
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

You will also need the requests library and the requests_aws4auth library. So:

pip install boto3

pip install requests

pip install requests_aws4auth

The boto3 library (you will hear people call it the AWS SDK also) is used for native S3 API calls on Cloudian HyperStore. You can use boto3 to interact with AWS as well. 
The requests library is more low-level, you use it to make HTTP GET/POST/PUT calls. In our scripts we use the requests library to utilize the S3 extensions provided by Cloudian HyperStore. In addition we also use the requests library to call the admin API of Cloudian HyperStore. 
The requests_aws4auth library is used to construct a signed authorization string when we call the requests library for S3 extensions. 

To clone this repo, navigate to the folder of your choice and type:
git clone git://github.com/cloudian-api/bucketops; cd bucketops; chmod 700 *.py. 
Now you can modify clusterconfig.py with your parameters (credentials, adminIP information) and type ./listbuckets.py to get started.

Here is a description of the files in this repo:
* clusterconfig.py contains variables and common functions used in the code. It is a Python module. You will need to update the variables above the line in order to get the programs to work.

* create_bucket.py takes various arguments:
   * Without any parameters it outputs all the storage policies you have configured on HyperStore. You will need the policy ID of a particular storage policy for the next step. Remember, a storage policy has a policy name and a policy ID.
   * With a bucket name and a policy ID (which you obtained from the previous step) it will create a bucket with the corresponding storage policy. Creating a bucket with a particular storage policy is a custom extension to the S3 API by HyperStore. It is implemented in create_bucket.py by utilizing the requests library. All buckets are created in the current region as returned by boto3. An exercise could be to modify the create_bucket() function to take a region as a parameter.

   * With just a bucket name (one parameter) it will create a bucket with the default storage policy, whatever it is defined to be.
  
* list_buckets.py lists all buckets owned by a user whose keys are specified in clusterconfig.py, along with their policy name and policy ID. Note that all operations having to do with retrieving information about bucket storage policies and setting bucket storage policies require the requests() library because they are custom extensions.

* delete_bucket.py deletes a bucket owned by a user whose keys are specified in clusterconfig.py.

* group_list_buckets.py takes the name of a group, finds all the users belonging to that group and lists buckets owned by those users.
