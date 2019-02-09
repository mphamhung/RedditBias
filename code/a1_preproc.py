import sys
import argparse
import os
import json
import re
import html

import timeit
import spacy
nlp = spacy.load('en', disable=['parser', 'ner']) 

indir = '/u/cs401/A1/data/'


if os.path.isdir('/u/cs401'):
    data = '/u/cs401/A1/data/'
    abbrev = '/u/cs401/Wordlists/abbrev.english'
    clitics = '/u/cs401/Wordlists/clitics'
    stopwords = '/u/cs401/Wordlists/StopWords'
else:
    pwd = os.getcwd()
    data = pwd+'/../data'
    abbrev = pwd+'/../extras/Wordlists/abbrev.english'
    clitics = pwd+'/../extras/Wordlists/clitics'
    stopwords = pwd+'/../extras/Wordlists/StopWords'

def preproc1( comment , steps=range(1,11)):
    ''' This function pre-processes a single comment

    Parameters:                                                                      
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step  

    Returns:
        modComm : string, the modified comment 
    '''

    modComm = comment
    if 1 in steps:
        # Remove new line characters
        modComm = re.sub(r'\n', '', modComm)
        # print("Removed newline characters: ", modComm)
        modComm = re.sub(r'[ ]+', ' ', modComm)

    if 2 in steps:
        # Replace HTML character codes
        splitComm = modComm.split(' ')

        for i in range(len(splitComm)):
            splitComm[i] = html.unescape(splitComm[i])
        modComm = ' '.join(splitComm)

        # print("Replaced HTML character codes: ", modComm)

    if 3 in steps:
        #Remove URLs
        modComm = re.sub(r'[:/.(1-z)]*((www)|(https)|(.com))[:/.(1-z)]*', '', modComm) 
        # print("Removed URLS: ", modComm)

    if 4 in steps:
        #Make punctuation their own token
        splitComm = modComm.split(' ')
        newComm = ''

        with open(abbrev) as f:
            listOfAbbrevs = [j.strip(' \n') for j in f.readlines()] + ['e.g.']
            for token in splitComm:
                if newComm == '':
                    space = ""
                else: 
                    space = " "

                if '.' in token:
                    if token in listOfAbbrevs:
                        newComm += space + re.sub(r'([!"#$%&()*+,\-/:;<=>?@\[\\\]^_`{|}~]+)', r' \1', token) #No period
                    else:
                        newComm += space + re.sub(r'([!"#$%&()*+,.\-/:;<=>?@\[\\\]^_`{|}~]+)', r' \1', token)
                else:
                    newComm += space + re.sub(r'([!"#$%&()*+,\-/:;<=>?@\[\\\]^_`{|}~]+)', r' \1', token) #No period
        modComm = newComm         
        # print("Split Punctuation: ", modComm)

    if 5 in steps:
        #Split clitics

        splitComm = modComm.split(' ')
        newComm = ''

        for token in splitComm:
                if newComm == '':
                    space = ""
                else: 
                    space = " "
                if re.search(r'(n\'[\w]+)', token, flags=0):
                    newComm += space + re.sub(r'(n\'[\w]+)', r' \1', token) #covers can't won't
                else:
                    newComm += space + re.sub(r'(\'[\w]*)', r' \1', token) #covers everything else
        modComm = newComm         

        # print("Split Clitics: ", modComm)

    if 6 in steps:
        newComm = ''
        utt = nlp(modComm)
        for token in utt: 
            if newComm == '':
                space = ""
            else: 
                space = " "
            
            newComm += space + token.text+'/'+str(token.tag_)

        modComm = newComm         

        # print("Tagged tokens: ", modComm)
    if 7 in steps:
        splitComm = modComm.split(' ')
        newComm = ''
        with open(stopwords) as f:
            listOfStopwords = [j.strip(' \n') for j in f.readlines()]
        for token in splitComm:
            tmp = re.sub(r'\/\S+', '', token)
            if tmp in listOfStopwords:
                continue
            else:
                if newComm == '':
                    space = ""
                else: 
                    space = " "

                newComm += space + token
        modComm = newComm
        # print("Removed Stop words: ", modComm)

    if 8 in steps:
        modComm = re.sub(r'\/\S+', '', modComm)

        newComm = ''
        utt = nlp(modComm)
        for token in utt: 
            if newComm == '':
                space = ""
            else: 
                space = " "
            if str(token.lemma_)[0] == '-' and token.text[0] != '-':
                newComm += space + str(token.text)+'/'+str(token.tag_)
            else:
                newComm += space + str(token.lemma_)+'/'+str(token.tag_)
        modComm = newComm         

        # print("Applyed Lemmatization: ", modComm)
    if 9 in steps:
        modComm = re.sub(r'(\/\.) ', r'\1\n', modComm)

        # print("Added newline to end of Sentence: ", modComm)
    if 10 in steps:
        modComm = re.sub(r'(\S+\/)', lambda x: x.group(1).lower() , modComm)
        # print("Lowercased the words: ", modComm)

    return modComm

def main( args ):
    
    allOutput = []
    for subdir, dirs, files in os.walk(indir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            print( "Processing " + fullFile)
            a = timeit.timeit()
            data = json.load(open(fullFile))

            
            # TODO: select appropriate args.max lines
            for i in range(int(args.ID[0])%int(args.max),int(args.ID[0])%int(args.max) + int(args.max)):
                line = data[i]
                # TODO: read those lines with something like `j = json.loads(line)`
                j = json.loads(line)
                # TODO: choose to retain fields from those lines that are relevant to you
                relevent_fields = ['id', 'body', 'subreddit']
                j = {x: j[x] for x in j if x in relevent_fields}
                # print(j)
                # TODO: add a field to each selected line called 'cat' with the value of 'file' (e.g., 'Alt', 'Right', ...)
                j['cat'] = file
                # TODO: process the body field (j['body']) with preproc1(...) using default for `steps` argument
                # TODO: replace the 'body' field with the processed text
                j['body'] = preproc1(j['body'])
                
                # TODO: append the result to 'allOutput'
                allOutput.append(j)
            b = timeit.timeit()
            print("Finished processing after: " + str(b-a))
    fout = open(args.output, 'w')
    fout.write(json.dumps(allOutput))
    fout.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument('ID', metavar='N', type=int, nargs=1,
                        help='your student ID')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("--max", help="The maximum number of comments to read from each file", default=10000)
    args = parser.parse_args()

    if (int(args.max) > 200272):
        print( "Error: If you want to read more than 200,272 comments per file, you have to read them all." )
        sys.exit(1)
        
    main(args)
