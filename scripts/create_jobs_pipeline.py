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
    # jobs_path = os.path.abspath("..\\data\\valid_maven_repos.csv")
    jobs_path = os.path.abspath("..\\data\\test.csv")
    template_path = os.path.abspath("..\\data\\template_config.xml")
    chain_template_path = os.path.abspath("..\\data\\chain_template_config.xml")
    
    with open(template_path,'r') as config:
        config_xml = config.read()
    config.close()
    
    with open(chain_template_path) as chain_config:
        chain_config_xml = chain_config.read()
    chain_config.close()
    
    with open(jobs_path,'rb') as jobs_file:
        jobs = list(csv.reader(jobs_file))
    jobs_file.close()
    random.shuffle(jobs)
    
    # create the last job first since it has no dependencies
    last_job_name,last_repo_url = jobs[0]
    print last_job_name
    last_job_xml = config_xml.replace('%PROJECT_URL%',last_repo_url) 
    server.create_job(last_job_name,last_job_xml)
    
    for i in range(1,len(jobs)):
        job_name,repo_url = jobs[i]
        next_job_name,next_repo_url = jobs[i-1]
        job_xml = chain_config_xml.replace('%PROJECT_URL%',repo_url)
        job_xml = job_xml.replace('%NEXT_PROJECT_NAME%',next_job_name)
        server.create_job(job_name,job_xml)
        print job_name,' -> ',next_job_name
    
    domino_path = os.path.abspath("..\\data\\domino.txt")
    with open(domino_path,'w') as outfile:
        outfile.write(jobs[len(jobs)-1][0])
    outfile.close()
    print 'First Project to Run: ', jobs[len(jobs)-1][0]
    print 'Written to',domino_path
               
if __name__ == '__main__':
    main()