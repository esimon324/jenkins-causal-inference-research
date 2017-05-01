import jenkins
import sys
import os
import csv

def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    
    collect(host,username,password)
            
def collect(host,username,password):
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    
    jobs = server.get_jobs()
    
    outpath = os.path.abspath("..\\data\\jenkins\\build_stats\\"+host+"_build_stats.csv")
    
    with open(outpath,'wb') as csvfile:
        csvwriter = csv.writer(csvfile,dialect=csv.excel)
        csvwriter.writerow(['user','repo','duration','status','timestamp','artifacts','failed_tests','total_tests'])
        print 'user,repo,duration,status,timestamp,artifacts,failed_tests,total_tests'
        for job in jobs:
            name = job['name']
            last_build_number = server.get_job_info(name)['lastBuild']['number']
            info = server.get_build_info(name,last_build_number) # access the first build
            try:
                testing_info = info['actions'][4]  # holds metrics on testing
            except:
                failed = 0
                total = 0
            
            index = name.find('_') # extracting user and repo name from job name
            user = name[:index]
            repo = name[index+1:]
            
            # Variables
            try:
                duration = info['duration'] # build time in ms
            except:
                duration = 0
                
            try:
                result = info['result'] # build status
            except:
                result = 'FAILURE'
            
            try:
                timestamp = info['timestamp'] # timestamp of run in UTC
            except:
                timestamp = 0
                
            try:
                artifacts = len(info['artifacts']) # number of artifacts created
            except:
                artifacts = 0
                
            try:
                failed = testing_info['failCount']  # number of failed unit tests
            except:
                failed = 0
                
            try:
                total = testing_info['totalCount'] # number of unit tests
            except:
                total = 0
                
            csvwriter.writerow([user,repo,duration,result,timestamp,artifacts,failed,total])            
            print user,repo,duration,result,timestamp,artifacts,failed,total

if __name__ == '__main__':
    main()