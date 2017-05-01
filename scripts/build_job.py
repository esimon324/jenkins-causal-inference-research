import jenkins
import sys
import os
def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)
    
    # get provided job name or select dominoe job by default
    if len(sys.argv) == 5:
        job = (str)(sys.argv[4])
    else:
        domino_path = os.path.abspath('..\\data\\dominos\\'+host+'.txt')
        with open(domino_path,'r') as infile:
            job = infile.read()
        infile.close()
        
    # build job
    server.build_job(job)
    print job,'QUEUED'

if __name__ == '__main__':
    main()