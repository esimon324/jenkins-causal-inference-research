import jenkins
import sys
def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)

    jobs = server.get_jobs()
    for job in jobs:
        job_name = job['name']
        server.build_job(job_name)
        print job_name,'QUEUED'

if __name__ == '__main__':
    main()