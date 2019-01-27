import sys
reload(sys)  
sys.setdefaultencoding('latin1')

def build_arff(twt):
    
    arff = []
    twt = twt.strip()
    arff.append(feat1(twt))
    arff.append(feat2(twt))
    arff.append(feat3(twt))
    arff.append(feat4(twt))
    arff.append(feat5(twt))
    arff.append(feat6(twt))
    arff.append(feat7(twt))
    arff.append(feat8(twt))
    arff.append(feat9(twt))
    arff.append(feat10(twt))
    arff.append(feat11(twt))
    arff.append(feat12(twt))
    arff.append(feat13(twt))
    arff.append(feat14(twt))
    arff.append(feat15(twt))
    arff.append(feat16(twt))
    arff.append(feat17(twt))
    arff.append(feat18(twt))
    arff.append(feat19(twt))
    arff.append(feat20(twt))
    # print twt
    # print arff
    return arff

def feat1(twt):
    # first person pronouns
    sentences = twt.split('\n')
    
    count = 0
    fpp = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']

    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for pronoun in fpp:
                if word[:word.index("/")].lower() == pronoun.lower():
                    count += 1
                    
    return count

def feat2(twt):
    # second person pronouns
    sentences = twt.split('\n')
    
    count = 0
    spp = ['you', 'your', 'yours', 'u', 'ur', 'urs']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for pronoun in spp:
                if word[:word.index("/")].lower() == pronoun.lower():
                    count += 1
                    
    return count
    
def feat3(twt):
    # third person pronouns
    sentences = twt.split('\n')
    
    count = 0
    tpp = ['he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for pronoun in tpp:
                if word[:word.index("/")].lower() == pronoun.lower():
                    count += 1
                    
    return count
    
def feat4(twt):
    # coordinating conjunctions
    sentences = twt.split('\n')
    
    count = 0
    cc = ['CC']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for conj in cc:
                if word[word.index("/")+1:].lower() == conj.lower():
                    count += 1
                    
    return count
    
def feat5(twt):
    # past tense verbs
    sentences = twt.split('\n')
    
    count = 0
    ptv = ['VBD']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for verb in ptv:
                if word[word.index("/")+1:].lower() == verb.lower():
                    count += 1
                    
    return count
    
def feat6(twt):
    # future tense verbs
    sentences = twt.split('\n')
    
    count = 0
    ft = ["'ll", 'will', 'gonna']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for j in range(len(words)):
            word = words[j]
            actual_word = words[j][:word.index("/")]
            for tense in ft:
                if actual_word.lower() == tense.lower():
                    count += 1
            if actual_word == "going" and j < (len(words) - 2):
                if words[j+1][:word.index("/")] == "to" and words[j+2][word.index("/")+1:] == "VB":
                    count += 1
                    
    return count
    
def feat7(twt):
    # commas
    sentences = twt.split('\n')
    
    count = 0
    comma = [',']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for punctuation in comma:
                if word[:word.index("/")].lower() == punctuation.lower():
                    count += 1
                    
    return count
    
def feat8(twt):
    # colons and semicolons
    sentences = twt.split('\n')
    
    count = 0
    colons = [':', ';']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for punctuation in colons:
                if word[:word.index("/")].lower() == punctuation.lower():
                    count += 1
                    
    return count
    
def feat9(twt):
    # dashes
    sentences = twt.split('\n')
    
    count = 0
    dashes = ['-']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for punctuation in dashes:
                if punctuation in word:
                    count += 1
                    
    return count
    
def feat10(twt):
    # parentheses
    sentences = twt.split('\n')
    
    count = 0
    parentheses = ['(', ')']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for punctuation in parentheses:
                if punctuation in word:
                    count += 1
                    
    return count
    
def feat11(twt):
    # ellipses
    sentences = twt.split('\n')
    
    count = 0
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            num_periods = word[:word.index("/")].count(".")
            if num_periods > 1:
                count += 1
                    
    return count
    
def feat12(twt):
    # common nouns
    sentences = twt.split('\n')
    
    count = 0
    cm = ['NN', 'NNS']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for noun in cm:
                if word[word.index("/")+1:].lower() == noun.lower():
                    count += 1
                    
    return count
    
def feat13(twt):
    #proper nouns
    sentences = twt.split('\n')
    
    count = 0
    pn = ['NNP', 'NNPS']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for noun in pn:
                if word[word.index("/")+1:].lower() == noun.lower():
                    count += 1
                    
    return count
    
def feat14(twt):
    #adverbs
    sentences = twt.split('\n')
    
    count = 0
    adv = ['RB', 'RBR', 'RBS']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for verb in adv:
                if word[word.index("/")+1:].lower() == verb.lower():
                    count += 1
                    
    return count
    
def feat15(twt):
    # wh words
    sentences = twt.split('\n')
    
    count = 0
    wh_words = ['WDT', 'WP', 'WP$', 'WRB']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for wh_word in wh_words:
                if word[word.index("/")+1:].lower() == wh_word.lower():
                    count += 1
                    
    return count
    
def feat16(twt):
    # slang
    sentences = twt.split('\n')
    
    count = 0
    slang_words = ["smh", 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol']
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            for slang in slang_words:
                if word[:word.index("/")].lower() == slang.lower():
                    count += 1
                    
    return count


def feat17(twt):
    #words in all caps
    sentences = twt.split('\n')
    
    count = 0
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            if len(word[:word.index("/")]) > 2 and word[:word.index("/")].isupper():
                count += 1
                    
    return count

def feat18(twt):
    # avg len of sentences
    sentences = twt.split('\n')
    
    count = 0
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            if len(word[:word.index("/")]) > 0:
                count += 1
                    
    return round(float(count)/(len(sentences)-1), 5)

def feat19(twt):
    # avg len of words, excluding punctuation tokens
    sentences = twt.split('\n')
    
    word_count = 0
    word_len = 0
    punctuation = ['#', '$', ',', ':', '(', ')', '"', "'", "!", ".", "?"]
    
    for i in range(1, len(sentences)):
        words = sentences[i].split(' ')
        for word in words:
            if len(word[:word.index("/")]) > 0:
                if word[0] not in punctuation:
                    word_count += 1
                    word_len += len(word[:word.index("/")])

    return round(float(word_len)/float(word_count), 5)


def feat20(twt):
    # num sentences
    sentences = twt.split('\n')
    return (len(sentences)-1)
    

if __name__ =='__main__':
    twt_filename = str(sys.argv[1])
    output_filename = str(sys.argv[2])
    for max_num in range(1, 21):
        num_per_class = 500*max_num
        
        print "Reading and processing (maximum %d tweets per class)" % num_per_class
        arffs = []
        curr_twt = ""
        sent_0_processed = 0
        sent_4_processed = 0
        curr_sent = 0
        process = True
        
        with open(twt_filename) as f:
            for line in f:
                if len(line) > 0:
                    if line[0:3] == "<A=":
                        # new tweet, first finish up processing previous tweet if necessary
                        if len(curr_twt) > 0:
                            arffs.append(build_arff(curr_twt) + [curr_sent])
                            
                        #process new tweet if necessary
                        curr_sent = int(line[3:4])
                        if curr_sent == 0 and sent_0_processed < num_per_class:
                            sent_0_processed += 1
                            process = True
                            curr_twt = line
                        elif curr_sent == 4 and sent_4_processed < num_per_class:
                            sent_4_processed += 1
                            process = True
                            curr_twt = line
                        else: #don't process this tweet
                            process = False
                            curr_twt = ""
                    elif process:
                        curr_twt += line
    
            if len(curr_twt) > 0:
                arffs.append(build_arff(curr_twt) + [curr_sent])
        f.close()
        
    
        print "Writing %d tweets to output .arff" % (sent_4_processed + sent_0_processed)
        output_f = open("3_2/training_%d.arff" % num_per_class, 'w')
        
        default_output = "@relation twit_classification\n\n@attribute 1st_person_pro numeric\n@attribute 2nd_person_pro numeric\n@attribute 3rd_person_pro numeric\n@attribute coord_conj numeric\n@attribute past_tense_vb numeric\n@attribute future_tense_vb numeric\n@attribute commas numeric\n@attribute colons numeric\n@attribute dashes numeric\n@attribute parentheses numeric\n@attribute ellipses numeric\n@attribute common_nn numeric\n@attribute proper_nn numeric\n@attribute adv numeric\n@attribute wh_words numeric\n@attribute slang numeric\n@attribute all_caps_words numeric\n@attribute avg_sentence_len numeric\n@attribute avg_token_len numeric\n@attribute num_sentences numeric\n@attribute emotion {0,4}\n\n@data"
        
        output_f.write(default_output)
        
        for arff in arffs:
            output_f.write("\n")
            for i in range(len(arff)):
                if i == len(arff) - 1:
                    output_f.write(str(arff[i]))
                else:
                    output_f.write(str(arff[i]) + ",")
        
        output_f.close()
        
        print "Done writing %d tweets" % len(arffs)