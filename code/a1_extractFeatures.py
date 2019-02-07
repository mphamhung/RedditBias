import numpy as np
import sys
import argparse
import os
import json

import re
import csv

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

BNGL = {}
with open(prefix+'BristolNorms+GilhoolyLogie.csv', newline ='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        BNGL[row['WORD']] = {"AoA": int(row['AoA (100-700)']), "IMG": int(row['IMG']), "FAM": int(row['FAM'])}

Warr = {}
with open(prefix+'Ratings_Warriner_et_al.csv', newline ='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Warr[row['Word']] = {"V.Mean.Sum":int(row['V.Mean.Sum']), "A.Mean.Sum": int(row['A.Mean.Sum']), "D.Mean.Sum": int(row['D.Mean.Sum'])}

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
    20. Average of FAM from Bristol, Gilhooly, and Logie norms 
    21. Standard deviation of AoA (100-700) from Bristol, Gilhooly, and Logie norms 
    22. Standard deviation of IMG from Bristol, Gilhooly, and Logie norms 
    23. Standard deviation of FAM from Bristol, Gilhooly, and Logie norms 
    24. Average of V.Mean.Sum from Warringer norms 
    25. Average of A.Mean.Sum from Warringer norms 
    26. Average of D.Mean.Sum from Warringer norms 
    27. Standard deviation of V.Mean.Sum from Warringer norms 
    28. Standard deviation of A.Mean.Sum from Warringer norms 
    29. Standard deviation of D.Mean.Sum from Warringer norms 
    '''
    feats = np.zeros(173+1)

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
    feats[15] += (len(''.join(re.findall(r'\b[0-z]+\/', comment))) - 1)/float(len(re.findall(r'\b[0-z]+\/', comment))) #avg len of tokens
    feats[16] += len(re.findall(r'/.', comment)) #Number of sentences

    words = [word.strip('/') for word in re.findall(r'\w+\/', comment)]
    feats[17] = sum([BNGL[word]['AoA'] for word in words if word in BNGL.keys()])/len(words)
    feats[18] = sum([BNGL[word]['IMG'] for word in words if word in BNGL.keys()])/len(words)
    feats[19] = sum([BNGL[word]['FAM'] for word in words if word in BNGL.keys()])/len(words)

    feats[20] = math.sqrt(sum([(BNGL[word]['AoA'] - feats[17])^2 for word in words if word in BNGL.keys()])/len(words))
    feats[21] = math.sqrt(sum([(BNGL[word]['IMG'] - feats[18])^2  for word in words if word in BNGL.keys()])/len(words))
    feats[22] = math.sqrt(sum([(BNGL[word]['FAM'] - feats[19])^2  for word in words if word in BNGL.keys()])/len(words))
    
    feats[23] = sum([Warr[word]['V.Mean.Sum'] for word in words if word in Warr.keys()])/len(words)
    feats[24] = sum([Warr[word]['A.Mean.Sum'] for word in words if word in Warr.keys()])/len(words)
    feats[25] = sum([Warr[word]['D.Mean.Sum'] for word in words if word in Warr.keys()])/len(words)

    feats[26] = math.sqrt(sum([(Warr[word]['V.Mean.Sum'] - feats[17])^2 for word in words if word in Warr.keys()])/len(words))
    feats[27] = math.sqrt(sum([(Warr[word]['A.Mean.Sum'] - feats[18])^2  for word in words if word in Warr.keys()])/len(words))
    feats[28] = math.sqrt(sum([(Warr[word]['D.Mean.Sum'] - feats[19])^2  for word in words if word in Warr.keys()])/len(words))  

    # TODO: your code here
    return feats
    feats
def main( args ):

    data = json.load(open(args.input))
    feats = np.zeros( (len(data), 173+1))

    # TODO: your code here
    for i in range(len(data)):
    if (i % 100 == 0):
        print("complete: "+ str(i/float(len(data))*100) + "%")
        feats[i][:29] = extract1(data[i]["body"])


        



        if (data[i]["cat"] == "Alt"):
            feats[i][-1] = 3
        elif (data[i]["cat"] == "Center"):
            feats[i][-1] = 1
        elif (data[i]["cat"] == "Left"):
            feats[i][-1] = 0
        elif (data[i]["cat"] == "Right"):
            feats[i][-1] = 2

    np.savez_compressed( args.output, feats)

    
# if __name__ == "__main__": 

#     parser = argparse.ArgumentParser(description='Process each .')
#     parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
#     parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
#     args = parser.parse_args()
                 

#     main(args)

