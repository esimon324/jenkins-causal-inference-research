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
    # path = os.path.abspath("..\\data\\valid_maven_repos.csv")
    path = os.path.abspath("..\\data\\test.csv")
    
    with open('template_config.xml','r') as infile_xml:
        template_xml = infile_xml.read()
    infile_xml.close()
    
    with open(path,'rb') as infile:
        jobs = list(csv.reader(infile))
    random.shuffle(jobs)
    
    for job in jobs:
        job_name,repo_url = job
        job_xml = template_xml.replace('%PROJECT_URL%',repo_url)
        server.create_job(job_name,job_xml)
        print job_name,'CREATED'

if __name__ == '__main__':
    main()