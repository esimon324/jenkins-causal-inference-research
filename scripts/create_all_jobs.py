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
    
    # jobs_path = os.path.abspath("..\\data\\repositories\\valid_maven_repos.csv")
    # jobs_path = os.path.abspath("..\\data\\repositories\\test.csv")
    jobs_path = os.path.abspath("..\\data\\repositories\\test_small.csv")
    
    template_path = os.path.abspath("..\\data\\templates\\template_config.xml")
    
    with open(template_path,'r') as infile_xml:
        template_xml = infile_xml.read()
    infile_xml.close()
    
    with open(jobs_path,'rb') as infile:
        repos = list(csv.reader(infile))
    infile.close()
    random.shuffle(repos)
    
    for user,name,url in repos:
        job_name = user+'_'+name
        job_xml = template_xml.replace('%PROJECT_URL%',url)
        server.create_job(job_name,job_xml)
        print job_name,'CREATED'

if __name__ == '__main__':
    main()