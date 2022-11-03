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
    # start parsing here
    

f.close()