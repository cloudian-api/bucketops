#!/usr/bin/python
import requests
import os
import csv
import sys
requests.packages.urllib3.disable_warnings()

programName = sys.argv[0]
if len(sys.argv) > 1:
    clusterName = sys.argv[1]
    adminUser = sys.argv[2]
    adminPass = sys.argv[3]
else:
    adminUser = os.popen('hsctl config get admin.auth.username').read().strip()
    adminPass = os.popen('hsctl config get admin.auth.password').read().strip()
    clusterName = "localhost"
adminEndpoint = "https://{}:19443".format(clusterName)
buckets = []
finalOut = {}

def get_server_session(username, password):
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        return session

def getBucketList(adminSession):

    blurl = "{}/bppolicy/bucketsperpolicy".format(adminEndpoint)
    blRequest = adminSession.get(blurl)

    return blRequest

def getObjectInfo(bucket, adminSession):

    objurl = "{}/usage/repair/bucket?bucket={}".format(adminEndpoint, bucket)
    objReq = adminSession.post(objurl)

    try:
        return objReq.json()
    except:
        print("\n{} Request Failed with status {}({})".format(objReq.url,objReq.status_code,objReq.reason))
        exit(1)

def getBucketOwner(adminSession):
    bucketOwners = {}
    groupReq = adminSession.get(adminEndpoint + '/group/list')
    for group in groupReq.json():
        ownerReq = adminSession.get(adminEndpoint + '/system/bucketlist?groupId=' + group['groupId'])
        for owner in ownerReq.json():
            bucketOwners[owner['userId']] = []
            for bucket in owner['buckets']:
                bucketOwners[owner['userId']].append(bucket['bucketName'])
    try:
        return bucketOwners
    except:
        if groupReq.status_code != 200:
            print("\n{} Request Failed with status {}({})".format(groupReq.url, groupReq.status_code,groupReq.reason))
        else:
            print("\n{} Request Failed with status {}({})".format(ownerReq.url, ownerReq.status_code,ownerReq.reason))
        exit(1)

def main():
    try:
        adminSession = get_server_session(adminUser, adminPass)
        bucketowners = getBucketOwner(adminSession)

        for bucket_info in getBucketList(adminSession).json():
            for bkl in bucket_info['buckets']:
                buckets.append(bkl)

        for bkt in buckets:
            objInfo = getObjectInfo(bkt, adminSession)
            finalOut[bkt] = {}
            finalOut[bkt]['TotalBytes'] = objInfo['TB']
            finalOut[bkt]['TotalObjects'] = objInfo['TO']
            finalOut[bkt]['AvgObjectSize(KB)'] = int((objInfo['TB']/objInfo['TO'])/1024)
            for owner_info in bucketowners:
                if bkt in bucketowners[owner_info]:
                    finalOut[bkt]['BucketOwner'] = owner_info.encode('ascii')

        print("Printing on Screen....")
        print(finalOut)
        print("Exporting it to CSV(Filename=Bucket_Stats.csv)....")
        csvTemp = csv.writer(open("Bucket_Stats.csv", "wb+"))
        csvTemp.writerow(["Bucket Name", "Bucket Owner", "Total Bytes", "Total Objects", "AvgObjectSize(KB)"])

        for bucket in finalOut:
            csvTemp.writerow([bucket, 
                            finalOut[bucket]['BucketOwner'],
                            finalOut[bucket]['TotalBytes'],
                            finalOut[bucket]['TotalObjects'],
                            finalOut[bucket]['AvgObjectSize(KB)']])
    except Exception as e:
        print(e)

if __name__ == '__main__':

    main()