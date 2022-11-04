# Group project for INFO-3142
# Members: Michael Ivanov, Thomas Pollard, Olivia Stemp

import spacy
nlp = spacy.load('en_core_web_sm')

# holds raw data from EmailLog.txt
all_data = ""
# read in all data from EmailLog.txt to a string
f = open('EmailLog.txt', 'r', encoding='utf-8')
for i in f.readlines():
	all_data += i
f.close()

doc = nlp(all_data)

# save spaCy data to a text file
f = open('ParsedData.txt', mode='wt', encoding='utf-8')
for token in doc:
	f.write(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)) + '\n')
f.close()


# read spaCy data from a text file
f = open('ParsedData.txt', mode='r', encoding='utf-8')
for line in f:
	line = line.strip('\n')

# string to hold all extracted values: emails, money, company names
sentence_string = ''

# parsing starts here

for i, token in enumerate(doc):
	# if current text is an email
	if(token.like_email):
		sentence_string += token.text + ' '
	# doc = nlp(sentence_string)

sentence_string += '\n'
phrase = ''
for i, token in enumerate(doc):
	# if current text is money
	if(token.tag_ == '$'):
		phrase = token.text
		i = token.i+1
		while doc[i].tag_ == 'CD':
			phrase += doc[i].text + ' '
			i += 1
		phrase = phrase[:-1]
		sentence_string += phrase + ' '
	# doc = nlp(sentence_string)
	
sentence_string += '\n'
for i, token in enumerate(doc):
	# if current text is a company name
	if(token.pos_ == 'PROPN' and token.dep_ == 'pobj' or token.tag_ == 'NNP' and doc[i-1].text == 'to' or doc[i-1].text == 'for' or doc[i-1].text == 'with'):
		if(token.text == 'Inc.'):
			continue
		sentence_string += token.text + ' '

# todo: change string to format properly and link emails to their sentences 
# have fun this language sux
print(sentence_string)

f.close()