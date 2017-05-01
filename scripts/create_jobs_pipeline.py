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
    
    # repos_path = os.path.abspath("..\\data\\repositories\\valid_maven_repos.csv")
    # repos_path = os.path.abspath("..\\data\\repositories\\test.csv")
    repos_path = os.path.abspath("..\\data\\repositories\\test_small.csv")
    
    template_path = os.path.abspath("..\\data\\templates\\template_config.xml")
    chain_template_path = os.path.abspath("..\\data\\templates\\chain_template_config.xml")
    
    with open(template_path,'r') as config:
        config_xml = config.read()
    config.close()
    
    with open(chain_template_path) as chain_config:
        chain_config_xml = chain_config.read()
    chain_config.close()
    
    with open(repos_path,'rb') as repos_file:
        repos = list(csv.reader(repos_file))
    repos_file.close()
    random.shuffle(repos)
    
    # create the last job first since it has no dependencies
    user,name,url = repos[0]
    job_name = user+'-'+name
    print job_name
    job_xml = config_xml.replace('%PROJECT_URL%',url) 
    server.create_job(job_name,job_xml)
    
    for i in range(1,len(repos)):
        user,name,url = repos[i]
        job_name = user+'-'+name
        next_user,next_name,next_url = repos[i-1]
        next_job_name = next_user+'-'+next_name
        job_xml = chain_config_xml.replace('%PROJECT_URL%',url)
        job_xml = job_xml.replace('%NEXT_PROJECT_NAME%',next_job_name)
        server.create_job(job_name,job_xml)
        print job_name,' -> ',next_job_name
    
    domino_path = os.path.abspath('..\\data\\dominos\\'+host+'.txt')
    with open(domino_path,'w') as outfile:
        user,name,url = repos[-1]
        domino_name = user+'_'+name
        outfile.write(domino_name)
    outfile.close()
    print 'First Project to Run: ', domino_name
    print 'Written to',domino_path
               
if __name__ == '__main__':
    main()