import random
import os
import csv
import time
import sys
import jenkins

def main():
    host = (str)(sys.argv[1]) # Instance DNS
    username = (str)(sys.argv[2]) # Jenkins user name
    password = (str)(sys.argv[3]) # Jenkins password
    server = jenkins.Jenkins('http://'+host+':8080', username=username, password=password)

    jobs = server.get_jobs()
    random.shuffle(jobs)

    num_jobs = len(jobs)
    lambd = 1/40.0

    wait_times = [0]
    for i in range(1,num_jobs):
        wait_times.append(random.expovariate(lambd))

    print 'wait_times:',wait_times

    for job in jobs:
        t = wait_times.pop(0)
        time.sleep(t)
        print 'Building job',job['name']
        server.build_job(job['name'])

if __name__ == '__main__':
    main()
