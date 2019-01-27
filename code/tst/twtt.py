import sys
reload(sys)  
sys.setdefaultencoding('latin1')
from HTMLParser import HTMLParser
import re
import NLPlib
tagger = NLPlib.NLPlib()

def to_str(arr):
	output = ''
	for word in arr:
		if output == '':
			output += word
		else:
			output += ' ' + word
	return output
	
def process(twt, sentiment):
	twt = re.sub(' +',' ',twt).strip()
	
	# Removes HTML tags
	processed = twtt1(twt)
	# Replaces all URL character codes
	processed = twtt2(processed)
	# Deletes all URLs
	processed = twtt3(processed)
	# Removes the first character of Twitter usernames/hashtags
	processed = twtt4(processed)
	# Uses abbreviations to split array on sentences
	processed = twtt5(processed)
	# Splits clitics and non-end-of-sentence punctuation
	processed = twtt7(processed)
	# Tagger
	processed = twtt8(processed)
	# Prepends sentiment
	processed = twtt9(processed, sentiment)

	# if (len(processed) == 
	return processed[:]
	
def twtt1(raw_html):
	html_opening_tag = re.compile('<[^>]+>')
	result = re.sub(html_opening_tag, '', raw_html)
	html_closing_tag = re.compile('<\/[^>]+>')
	result = re.sub(html_opening_tag, '', raw_html)
	return result
	
def twtt2(twt):
	#fix HTML Character Codes
	twt = twt.split(' ')
	h = HTMLParser()
	
	for i in range(len(twt)):
		twt[i] = h.unescape(twt[i])

	return to_str(twt)

def twtt3(twt):
	#Remove any words that need to be removed
	twt = twt.split(' ')
	output = ''
	URL = ['http://', 'www.', '.com']

	for word in twt:
		for to_remove in URL:
			if re.search(to_remove, word, re.IGNORECASE):
				twt.remove(word)
				break

	return to_str(twt)

def twtt4(twt):
	#Remove HTML tags and attributes
	twt = twt.split(' ')
	chars_to_remove = '@#'

	for i in range(len(twt)):
		twt[i] = twt[i].strip(chars_to_remove)
	return to_str(twt)
	
def twtt5(twt):
	twt = twt.split(' ')
	with open('abbrev.english') as f:
		abbrev = f.read().lower().splitlines()

	EoS = ['?', '.', '!'] #end of sentence punctutations
	salutations = ["mr.", "dr.", "ms.", "mrs."]
	EoS_pattern = re.compile('([/.?!]{2,})')

	result = ""
	sentence = []
	for i in range(len(twt)):
		punctuation_count = sum(twt[i].count(p) for p in EoS)
		if punctuation_count == 1 and twt[i].lower() in salutations:
			# Salutation, don't end sentence
			sentence.append(twt[i]) # add the word normally
		elif twt[i].lower() in abbrev:
			if i == len(twt) - 1 or len(twt[i+1]) == 0:
				# Abbrev, but end sentence
				sentence.append(twt[i])
				result += to_str(sentence) + "\n"
				sentence = []
			elif twt[i+1][0].islower():
				# Abbrev, don't end sentence
				sentence.append(twt[i]) # add the word normally
			else:
				# Abbrev, but end sentence b/c next word is upper case
				sentence.append(twt[i])
				result += to_str(sentence) + "\n"
				sentence = []
		elif punctuation_count > 1:
			# Multiple punctuation, end sentence
			word = twt[i]
			matches = re.findall(EoS_pattern, twt[i])
			
			if matches:
				for match_i in range(len(matches)):
					if match_i == len(matches) - 1:
						location = word.index(matches[match_i])
						sentence.append(word[:location])
						sentence.append(matches[match_i])
						
						#end sentence
						result += to_str(sentence) + "\n"						
						#start new sentence
						sentence = [word[location + len(matches[match_i]):]]
					else:
						location = word.index(matches[match_i])
						sentence.append(word[:location])
						sentence.append(matches[match_i])
						word = word[location + len(matches[match_i]):]

		elif punctuation_count == 1:
			# End sentence			
			first_occurence = float('inf')
			for p in EoS:
				if twt[i].find(p) < first_occurence and twt[i].find(p) != -1:
					first_occurence = twt[i].find(p)
			sentence.append(twt[i][:first_occurence])
			sentence.append(twt[i][first_occurence:first_occurence + 1])
			result += to_str(sentence) + "\n"
			sentence = []
			if len(twt[i][first_occurence+1:]) > 0:
				sentence.append(twt[i][first_occurence+1:])
		else:
			sentence.append(twt[i]) # add the word normally
	if len(sentence) != 0:
		result += to_str(sentence) + "\n \n"
	return result

def twtt7(twt):
	twt = twt.split("\n")
	result = ""
	punctuation = ['#', '$', ',', ':', '(', ')', ';', '"', "'"]
	clitics = ["n't", "'ve", "'s", "'re", "'m", "'ll", "'all", "'d", "'clock"]
	
	for sentence in twt:
		if len(sentence.strip()) > 0:
			sentence = sentence.split(' ')
			parsed_sentence = []
			for word in sentence:
				continue_parsing = True
				for c in clitics:
					if c in word and continue_parsing:
						parsed_sentence.append(word[:word.index(c)])
						parsed_sentence.append(word[word.index(c):])
						continue_parsing = False
				for p in punctuation:
					if p in word and continue_parsing:
						parsed_sentence.append(word[:word.index(p)])
						parsed_sentence.append(word[word.index(p):word.index(p)+1])
						if len(word[word.index(p)+1:]) > 0:
							parsed_sentence.append(word[word.index(p)+1:])
						continue_parsing = False
				if continue_parsing:
					parsed_sentence.append(word)
						
			result += to_str(parsed_sentence) + "\n"

	return result

def twtt8(twt):
	twt = twt.split("\n")
	result = ""
	
	for sentence in twt:
		if len(sentence.strip()) > 0:
			sentence = sentence.strip().split(' ')
			parsed_sentence = []
			tags = tagger.tag(sentence)
			for i in range(len(sentence)):
				parsed_sentence.append(sentence[i] + '/' + tags[i])
						
			result += to_str(parsed_sentence) + "\n"

	return result
	
def twtt9(twt, sentiment):
	return "<A={}>\n".format(sentiment) + twt
	
if __name__ =='__main__':
	tweets_smaller_than_20000 = []
	tweets = []
	larger_than_20000 = False

	twt_filename = str(sys.argv[1])
	student_no = int(sys.argv[2])
	output_filename = str(sys.argv[3])
	
	print "Reading tweets"
	with open(twt_filename) as f:
		for i, line in enumerate(f):
			if i < 20000:
				tweets_smaller_than_20000.append(line[1:-2].split('","'))
			elif i == 20000:
				larger_than_20000 = True
				
			if i - (student_no % 80)*10000 >= 0 and i - (student_no % 80)*10000 < 10000:
				tweets.append(line[1:-2].split('","'))
			elif i - 800000 - (student_no % 80)*10000 >= 0 and i - 800000 - (student_no % 80)*10000 < 10000:
				tweets.append(line[1:-2].split('","'))
	f.close()

	output_f = open(output_filename, 'w')
	if larger_than_20000:
		print "Processing %d tweets" % len(tweets)
		for i in range(len(tweets)):
			twt = tweets[i]
			if i == (len(tweets) - 1):
				output_f.write(process(twt[len(twt) - 1], int(twt[0]))[:-2])
			else:
				output_f.write(process(twt[len(twt) - 1], int(twt[0])))
	else:
		print "Processing %d tweets" % len(tweets_smaller_than_20000)
		for i in range(len(tweets_smaller_than_20000)):
			twt = tweets_smaller_than_20000[i]
			if i == (len(tweets_smaller_than_20000) - 1):
				output_f.write(process(twt[len(twt) - 1], int(twt[0]))[:-2])
			else:
				output_f.write(process(twt[len(twt) - 1], int(twt[0])))

	output_f.close()
	
	print("Done")