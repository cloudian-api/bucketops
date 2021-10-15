# bucketops
Scripts that manipulate buckets on Cloudian.
More for information regarding the Cloudian HyperStore REST API, please browse sections 11 through 16 of the manual.

You will need Python, I used version 3.9.7. Also the boto3 Python library (AWS SDK): 
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

You will also need the requests library. So:

git clone git://github.com/requests/requests.git

cd requests

pip install .

To clone this repo, navigate to the folder of your choice and type:
git clone git://github.com/cloudian-api/bucketops

Here is a description of the files in this repo:
* clusterconfig.py contains variables and common functions used in the code. It is a Python module. You will need to update the variables above the line in order to get the programs to work.

* create_bucket.py creates a bucket that is owned by a user specified in clusterconfig.py.

* list_buckets.py lists all buckets owned by a user specified in clusterconfig.py.

* delete_bucket.py deletes a bucket owned by a user specified in clusterconfig.py.
