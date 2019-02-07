import numpy as np
import sys
import argparse
import os
import json

import re

if os.path.isdir('/u/cs401'):
    prefix = '/u/cs401/Wordlists/'
    data = '/u/cs401/A1/data/'

else:
    pwd = os.getcwd()
    prefix = pwd + '../extras/Wordlists/'
    data = pwd+'/../data'

firstperson = prefix + 'First-person'
secondperson = prefix + 'Second-person'
thirdperson = prefix + 'Third-Person'
slang = prefix + 'Slang'

with open(firstperson) as f:
    firstpersonPat = r'(('+ r')|('.join(f.split("\n")) + r'))\/'
    print(firstpersonPat)

    
    
def extract1( comment ):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''

    feats = np.zeros(173)

    firstperson = r'((i)|(me)|(my)|(mine)|(we)|(us)|(our)|(ours))\/'
    secondperson = r'((you)|(your)|(yours)|(u)|(ur)|(urs))\/'
    thirdperson = r'((he)|(him)|(his)|(she)|(her)|(hers)|(it)|(its)|(they)|(them)|(their)|(theirs))\/'
     

    sentences = comment.split("\n")

    for sentence in sentences:
        if (sentence):
            feats[0] += len(re.findall(r'(/PRP)', sentence)) #Number of first person pronouns
            feats[1] += len(re.findall(r'(/PRP)', sentence)) #Number of second person pronouns
            
    # TODO: your code here

def main( args ):

    data = json.load(open(args.input))
    feats = np.zeros( (len(data), 173+1))

    # TODO: your code here

    np.savez_compressed( args.output, feats)

    
# if __name__ == "__main__": 

#     parser = argparse.ArgumentParser(description='Process each .')
#     parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
#     parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
#     args = parser.parse_args()
                 

#     main(args)

