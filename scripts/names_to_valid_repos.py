# Prunes the repo names for only those that are still active on github
import requests
import os
import csv
def main():
    outpath = os.path.abspath('..\\data\\valid_maven_repos.csv')
    with open(outpath,'wb') as csvfile:
        csvwriter = csv.writer(csvfile,dialect=csv.excel)
        inpath = os.path.abspath('..\\data\\maven_repository_names.txt')
        with open(inpath,'r') as infile:
            for line in infile:
                line = line.rstrip()
                index = line.find('-')
                user = line[:index]
                repo = line[index+1:]
                url = name_to_url(user,repo)
                has_valid_url = False
                while index >= 0:
                    if try_connection(url):
                        has_valid_url = True
                        break
                    index = line.find('-',index+1)
                    user = line[:index]
                    repo = line[index+1:]
                    url = name_to_url(user,repo)
                
                if has_valid_url:
                    csvwriter.writerow([user,repo,url])
                    print user,repo,url
                else:
                    csvwriter.writerow([user,repo,'None'])
                    print user,repo,'NONE'
                

def try_connection(url):
    try:
        r = requests.get(url)
        if r.status_code == 404:
            return False
        else:
            return True
    except:
        return False
        
def name_to_url(user,repo):
    return 'https://www.github.com/'+user+'/'+repo
        
if __name__ == '__main__':
    main()
    