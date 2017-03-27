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
                name = line[:index] + '/' + line[index+1:]
                url = name_to_url(name)
                has_valid_url = False
                while index >= 0:
                    if try_connection(url):
                        has_valid_url = True
                        break
                    index = line.find('-',index+1)
                    name = line[:index] + '/' + line[index+1:]
                    url = name_to_url(name)
                
                if has_valid_url:
                    csvwriter.writerow([line,url])
                else:
                    csvwriter.writerow([line,'None'])
                

def try_connection(url):
    try:
        r = requests.get(url)
        print url,r.status_code
        if r.status_code == 404:
            return False
        else:
            return True
    except:
        return False
        
def name_to_url(name):
    return 'https://www.github.com/'+name
        
if __name__ == '__main__':
    main()
    