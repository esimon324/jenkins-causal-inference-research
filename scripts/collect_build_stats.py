import jenkins
import sys
import os
import csv

def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    
    jobs = server.get_jobs()
    
    outpath = os.path.abspath("..\\data\\"+host+"_stats.csv")
    
    with open(outpath,'wb') as csvfile:
        csvwriter = csv.writer(csvfile,dialect=csv.excel)
        csvwriter.writerow(['duration(ms)','status','timestamp','artifacts','failed','total'])
        print 'Duration (ms),Status,Timestamp,Number of Artifacts,Failed Tests,Total Tests'
        for job in jobs:
            name = job['name']
            info = server.get_build_info(name,1) # access the first build
            testing_info = info['actions'][4]  # holds metrics on testing
            
            # Variables
            duration = info['duration'] # build time in ms
            result = info['result'] # build status
            timestamp = info['timestamp'] # timestamp of run in UTC
            artifacts = len(info['artifacts']) # number of artifacts created
            failed = testing_info['failCount']  # number of failed unit tests
            total = testing_info['totalCount'] # number of unit tests
            csvwriter.writerow([duration,result,timestamp,artifacts,failed,total])
            print duration,result,timestamp,artifacts,failed,total

if __name__ == '__main__':
    main()