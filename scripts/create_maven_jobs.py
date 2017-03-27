import jenkins
import sys
import os
import csv
def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    path = os.path.abspath("..\\data\\test_csv.csv")
    
    with open('template_config.xml','r') as infile_xml:
        template_xml = infile_xml.read()
    infile_xml.close()
    
    with open(path,'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            job_name,repo_url = row
            if repo_url == 'None':
                template_xml = template_xml.replace('%PROJECT_URL%',repo_url)
                server.create_job(job_name,template_xml)
if __name__ == '__main__':
    main()