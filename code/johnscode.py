import sys
import argparse
import os
import json

indir = '/u/cs401/A1/data/';

def preproc1( comment , steps=range(1,11)):
    ''' This function pre-processes a single comment

    Parameters:                                                                      
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step  

    Returns:
        modComm : string, the modified comment 
    '''

    modComm = ''
    if 1 in steps:

        # add our code here: do stripping

        modComm = comment.replace('\r\n', ' ')
        # print(comment)
        # print(modComm)


    if 2 in steps:
        # modComm = modComm.decode('unicode-escape')

        import html
        modComm = html.unescape(modComm)
    if 3 in steps:


        import re
        # we can do this by simply scanning over each word (or in fact, high level python gives us the option to simply do a string replace!)
        # first, find if the thing exists in the string. Then take it until the end. So, actually a regex is probably best here. We will need to recall the regex
        # compile, match etc.!
        url_pattern = re.compile("((http|www).*[\s\/])") # we want to take the entire string until the end!
        # now match them
        # now we get the groups out!
        matches = url_pattern.findall(modComm) #returns a series of match objects, which we can extract the groups out of
        modComm = url_pattern.sub("", modComm)
        if "conduit" in comment:

            print("eeps")
            print(comment)

            # actually, the "match" is still the same; it's just that we have some more groups to
            # express it!
            print(modComm)
        # print(modComm)
        # if matches is not None:
        #     # print(matches.groups())
        #     for match in matches:
        #
        #         print(match)

        # print(matches_group.groups())
        # modComm.replace("")
        print('TODO')
    if 4 in steps:

        # recall we are writing a regex to match these conditions, and then perform actions
        import string
        puncts = string.punctuation
        puncts_without_apostrophe = puncts.replace('\'', '')
        puncts_without_apostrophe_periods = puncts_without_apostrophe.replace(".", '')
        print(puncts_without_apostrophe)
        print(puncts)

        import re
        print(re.escape(puncts_without_apostrophe))

        escaped_literal_puncts = re.escape(puncts_without_apostrophe_periods)

        period_template = "(?<![\.]\w)([\.])(?!\w|\\1)"
        remaining_punct_template = "([{}])(?!\\1)".format(escaped_literal_puncts)

        period_regex = re.compile(period_template)
        other_punct_regex = re.compile(remaining_punct_template)

        query_string = "hello. this, is moi. however it will also split up !!! and e.g. and f.a.s.t. w.o.w. it really works now. this is strange since.Actually this is diff. This is also p!r!o!b!l!e!m"
        # matches = punct_template.findall("hello. this, is moi.") #returns a series of match objects, which we can extract the groups out of
        modComm = period_regex.sub(" \\1 ", modComm)
        print(modComm)
        modComm = other_punct_regex.sub(" \\1 ", modComm)
        print(modComm)        # to get around this, we want perhaps some negative assertion. we could also look into somehow consuming the characters

        # we should write a regex that can do a group replace
        # we can have an abbreviation list
        # a regex might not be able to express the list however!
        # but anything like a.b.c.d. would remain as a token, which could be good
        # the regex would be kind of useful for the general case
        # but the string operation would also be straightforward: simply replace the punctutation
        # if the next character is not a regular character!
        # regex is a little better thanks to the grouping we have

        # how do we repalce based on the contents of the word?!


        print('TODO')
    if 5 in steps:

        # general plan: simply find the regex which extracts characters around the apostrophe
        # the only question is: do we need to only handle the cases in the clitics list given? or can we just abstractly/generally do it
        # we envision the rest to take maybe 5 hours to do. OK!
        print('TODO')
    if 6 in steps:
        print('TODO')
    if 7 in steps:
        print('TODO')
    if 8 in steps:
        print('TODO')
    if 9 in steps:
        print('TODO')
    if 10 in steps:
        print('TODO')
        
    return modComm

def main( args ):

    allOutput = []
    for subdir, dirs, files in os.walk(indir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            print( "Processing " + fullFile)
            with open(fullFile) as file:
                for line in file:
                    print(len(line))
                    break
            data = json.load(open(fullFile))

            # print(data["body"])
            #  we can iterate the data
            for counter, line in enumerate(data):

                if counter > 100:
                    break

                json_object = json.loads(line)
                # print(type(json_object))

                # print(json_object["body"].count('\n'))

                # only process if we have the newline character
                if "\r\n" in (json_object ["body"]): #we can use the repr here but must look for \\n instead

                    preprocessed = preproc1(json_object ["body"], steps=range(1,4))

                    print(repr(json_object ["body"]))


                    #  if we want to test just a single step, then we need this clunky syntax

                    # https://stackoverflow.com/questions/17391437/how-to-use-r-to-print-on-same-line#_=_ this is the issue we are having!
                    # hence, we should always remove \r along with \n!! (otherwise printing the string just clobbers whatever is already there!)
                    print(preprocessed)
                    print("ok some more datas")
                    print("why is preprocessed so messed up {}".format(preprocessed))

                    print(repr(preprocessed))

                    print(json_object ["body"])


            #     we have established correspondence between \n in the text and \n in the representation
            #     now, we can call our preprocl function, and see how each of the steps work out

            # data[text]

            # TODO: select appropriate args.max lines
            # TODO: read those lines with something like j = json.loads(line)
            # TODO: choose to retain fields from those lines that are relevant to you
            # TODO: add a field to each selected line called 'cat' with the value of 'file' (e.g., 'Alt', 'Right', ...) 
            # TODO: process the body field (j['body']) with preproc1(...) using default for steps argument
            # TODO: replace the 'body' field with the processed text
            # TODO: append the result to 'allOutput'
            
    fout = open(args.output, 'w')
    fout.write(json.dumps(allOutput))
    fout.close()

if _name_ == "_main_":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument('ID', metavar='N', type=int, nargs=1,
                        help='your student ID')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("--max", help="The maximum number of comments to read from each file", default=10000)
    args = parser.parse_args()

    if (args.max > 200272):
        print( "Error: If you want to read more than 200,272 comments per file, you have to read them all." )
        sys.exit(1)
        
    main(args)