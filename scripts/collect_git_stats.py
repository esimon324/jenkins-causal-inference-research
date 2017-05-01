import sys
import os
import csv
from github import Github

def main():
    username = (str)(sys.argv[1]) # Github user name
    password = (str)(sys.argv[2]) # Github password
    write_type = (str)(sys.argv[3]) # Opens csv with this write type
    if len(sys.argv) > 4:
        start = (str)(sys.argv[4]) # Users alphabetically greater than
        end = (str)(sys.argv[5]) # Users alphabetically less than
        not_filtering = False
    else:
        start, end = ''
        not_filtering = True
    gh = Github(username,password)
    
    # repos_path = os.path.abspath("..\\data\\repositories\\valid_maven_repos.csv")
    repos_path = os.path.abspath("..\\data\\repositories\\test.csv")
    # repos_path = os.path.abspath("..\\data\\repositories\\test_small.csv")
    
    with open(repos_path,'rb') as infile:
        repos = list(csv.reader(infile))
    infile.close()
    
    outpath = os.path.abspath("..\\data\\git_stats.csv")
    errpath = os.path.abspath("..\\data\\git_repo_errors.txt")
    with open(outpath,write_type) as csvfile:
        csvwriter = csv.writer(csvfile,dialect=csv.excel)
        csvwriter.writerow(['user','repo','repo_size','contributors'])
        user,name,url = repos[0]
        gh_user = gh.get_user(user)
        with open(errpath,write_type) as errfile:
            for user,name,url in repos:
                if url != 'None':
                    if not_filtering or (user.lower() >= start and user.lower() < end):
                        try: 
                            if gh_user.name != user:
                                gh_user = gh.get_user(user)
                            repo = gh_user.get_repo(name)
                            csvwriter.writerow([user,name,repo.size,num_contributors(repo.get_contributors())])
                            print user,name
                        except:
                            outstr = user+','+name+','+url+'\n'
                            errfile.write(outstr)
        errfile.close()
    csvfile.close()
    
def num_contributors(contributors):
    num = 0
    for user in contributors:
        num += 1
    return num
    
if __name__ == '__main__':
    main()