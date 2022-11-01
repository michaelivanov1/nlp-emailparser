import spacy
# regex import
import re

nlp = spacy.load('en_core_web_sm')
# doc = nlp(u'Hi Dave, I’d like to invest $10,000 with Microsoft and another $15,000 with Amazon. Thanks, Tom.')

# read & write text file
read_file_name = "EmailLog.txt"
write_file_name = "ParsedEmails.txt"
read_file_text = open(read_file_name).read()
doc = nlp(read_file_text)

all_emails = []

with open(write_file_name, "wt") as txt_file: 
    for token in doc:
        if(token.like_email): 
            all_emails.append(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)))
            txt_file.write(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)) + '\n') 
print(write_file_name + " file written")

print(all_emails)

# read spaCy data from a text file
f = open(write_file_name, mode='r', encoding='utf-8')
for line in f:
	line = line.strip('\n')
	print(line)

f.close()


# read spaCy data from a text file
# f = open('demo.txt', mode='r', encoding='utf-8')
# for line in f:
# 	line = line.strip('\n')
# 	# print(line)

# f.close()