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
    prefix = pwd + '/../extras/Wordlists/'
    data = pwd+'/../data'

firstperson = prefix + 'First-person'
secondperson = prefix + 'Second-person'
thirdperson = prefix + 'Third-Person'
slang = prefix + 'Slang'

with open(firstperson) as f:
    firstpersonPat = re.sub('\n', '', r' (('+ r')|('.join(f.readlines()) + r'))\/')

with open(secondperson) as f:
    secondpersonPat = re.sub('\n', '', r' (('+ r')|('.join(f.readlines()) + r'))\/')
    
with open(thirdperson) as f:
    thirdpersonPat = re.sub('\n', '', r' (('+ r')|('.join(f.readlines()) + r'))\/')

with open(slang) as f:
    slangPat = re.sub('\n', '', r' (('+ r')|('.join(f.readlines()) + r'))\/')
    
def extract1( comment ):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''

    '''
    1. Number of ﬁrst-person pronouns 
    2. Number of second-person pronouns 
    3. Number of third-person pronouns 
    4. Number of coordinating conjunctions 
    5. Number of past-tense verbs 
    6. Number of future-tense verbs 
    7. Number of commas 
    8. Number of multi-character punctuation tokens 
    9. Number of common nouns 
    10. Number of proper nouns 
    11. Number of adverbs 
    12. Number of wh- words 
    13. Number of slang acronyms 
    14. Number of words in uppercase (≥ 3 letters long) 
    15. Average length of sentences, in tokens 
    16. Average length of tokens, excluding punctuation-only tokens, in characters 
    17. Number of sentences. 
    18. Average of AoA (100-700) from Bristol, Gilhooly, and Logie norms 
    19. Average of IMG from Bristol, Gilhooly, and Logie norms 
    20. Average of FAM from Bristol, Gilhooly, and Logie norms 21. Standard deviation of AoA (100-700) from Bristol, Gilhooly, and Logie norms 22. Standard deviation of IMG from Bristol, Gilhooly, and Logie norms 23. Standard deviation of FAM from Bristol, Gilhooly, and Logie norms 24. Average of V.Mean.Sum from Warringer norms 25. Average of A.Mean.Sum from Warringer norms 26. Average of D.Mean.Sum from Warringer norms 27. Standard deviation of V.Mean.Sum from Warringer norms 28. Standard deviation of A.Mean.Sum from Warringer norms 29. Standard deviation of D.Mean.Sum from Warringer norms '''
    feats = np.zeros(173)

    feats[0] += len(re.findall(firstpersonPat, comment)) #Number of first person pronouns
    feats[1] += len(re.findall(secondpersonPat, comment)) #Number of second person pronouns
    feats[2] += len(re.findall(secondpersonPat, comment)) #Number of second person pronouns
    feats[3] += len(re.findall(r'\/CC ', comment)) #Number of Coordinating Conjunctions
    feats[4] += len(re.findall(r'\/VBD ', comment)) #Number of Past tense verbs
    feats[5] += len(re.findall(r'((\'ll)|(will)|(gonna)|(going\/\w+ to))\/', comment)) #Number of Future-tense verbs
    feats[6] += len(re.findall(r'\/, ', comment)) #number of commas
    feats[7] += len(re.findall(r'[?!.]{2,}', comment)) #number of multi-character punctuation
    feats[8] += len(re.findall(r'\/((NN)|(NNS)) ', comment)) #number of common nouns
    feats[9] += len(re.findall(r'\/((NNP)|(NNPS)) ', comment)) #number of proper nouns
    feats[10] += len(re.findall(r'\/((RB)|(RBR)|(RBS)) ', comment)) #number of adverbs
    feats[11] += len(re.findall(r'\/((WDT)|(WP)|(WP$)|(WRB)) ', comment)) #number of wh- words
    feats[12] += len(re.findall(slangPat, comment)) #find slang acronyms
    feats[13] += len(re.findall(r' ([A-Z]{3,})\/', comment)) #find all capped words >= 3 letters long
    feats[14] += (len(re.findall(r' ', comment)) + 1)/float(len(re.findall(r'/.', comment))) # avg number of tokens per sentence
    feats[15] += (len(re.findall(r'\w+\/', comment)) + 1)/float(len(re.findall(r'/.', comment)))
    feats[16] += len(re.findall(r'/.', comment))
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

