import sys
import os
import csv
from github import Github

def main():
    username = (str)(sys.argv[1]) # Jenkins user name
    password = (str)(sys.argv[2]) # Jenkins password
    gh = Github(username,password)
    
    repos_path = os.path.abspath("..\\data\\valid_maven_repos.csv")
    # repos_path = os.path.abspath("..\\data\\test.csv")    
    with open(repos_path,'rb') as infile:
        repos = list(csv.reader(infile))
    infile.close()
    
    outpath = os.path.abspath("..\\data\\git_stats.csv")
    errpath = os.path.abspath("..\\data\\git_repo_errors.txt")
    with open(outpath,'wb') as csvfile:
        csvwriter = csv.writer(csvfile,dialect=csv.excel)
        csvwriter.writerow(['User','Name','Size (KB)','Number of Contributors'])
        
        user,name,url = repos[0]
        gh_user = gh.get_user(user)
        with open(errpath,'wb') as errfile:
            for user,name,url in repos:
                if url != 'None':
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