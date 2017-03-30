import jenkins
import sys
import os
import csv
def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    path = os.path.abspath("..\\data\\valid_maven_repos.csv")
    
    jobs = server.get_jobs()
    for job in jobs:
        job_name = job['name']
        server.delete_job(job_name)
        print job_name,'DELETED'

if __name__ == '__main__':
    main()