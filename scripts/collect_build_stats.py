import jenkins
import sys
import os
import csv
import random
def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    
    jobs = server.get_jobs()
    
    print 'Duration (ms)','Result','Test Count','Failed Count'
    for job in jobs:
        name = job['name']
        info = server.get_build_info(name,1)
        test_info = info['actions'][4]
        failed = test_info['failCount']
        total = test_info['totalCount']
        print info['duration'],info['result'],total,failed

if __name__ == '__main__':
    main()