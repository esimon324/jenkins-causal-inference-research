import jenkins
import sys
import os
import pandas as pd

import collect_build_stats as build_stats

def main():
    host = (str)(sys.argv[1]) # Instance DNS
    is_seq = (str)(sys.argv[2]) # Sequentiality
    slaves = (str)(sys.argv[3]) # Number of slave nodes used
    
    if is_seq == 'TRUE':
        outfile = os.path.abspath('..\\data\\results\\sequential-'+slaves+'.csv')
    elif is_seq == 'FALSE':
        outfile = os.path.abspath('..\\data\\results\\parallel-'+slaves+'.csv')
    else:
        raise Exception('Invalid value of sequentiality')
    
    # collect various stats
    build_stats = pd.read_csv(os.path.abspath('..\\data\\jenkins\\build_stats\\'+host+'_build_stats.csv')) # Jenkins build stats
    grep_stats = pd.read_csv(os.path.abspath('..\\data\\jenkins\\grep_stats\\'+host+'_grep_stats.csv')) # Jenkins grep stats
    git_stats = pd.read_csv(os.path.abspath('..\\data\\github\\git_stats.csv')) # Jenkins build stats
    merged = pd.merge(git_stats,pd.merge(build_stats,grep_stats,on=['user','repo']),on=['user','repo'])
    merged['is_seq'] = is_seq
    merged['slaves'] = slaves
    print merged
    merged.to_csv(outfile, index=False)

if __name__ == '__main__':
    main()