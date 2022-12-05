# NLP & spacy

import spacy

nlp = spacy.load("en_core_web_sm")
from re import sub
from decimal import Decimal

# holds raw data from EmailLog.txt
all_data = ""

# read in all data from EmailLog.txt to a string
f = open("EmailLog.txt", "r", encoding="utf-8")
for i in f.readlines():
    all_data += i
f.close()

doc = nlp(all_data)

# save spaCy data to a text file
f = open("ParsedData.txt", mode="wt", encoding="utf-8")
for token in doc:
	f.write(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)) + "\n")
f.close()

# read spaCy data from a text file
f = open("ParsedData.txt", mode="r", encoding="utf-8")
for line in f:
    line = line.strip("\n")

# string to hold all extracted values: emails, money, company names
sentence_string = ""

# variables
phrase = ""
money = 0
moneyList = []
totalMoney = 0
count = 0
companyList = []

# parsing starts here
for i, token in enumerate(doc):
    # if current text is an email
    if token.like_email:
        sentence_string += token.text + " : "
        money = 0
        moneyList.clear()

    # if current text is money
    elif token.tag_ == "$":
        phrase = token.text
        i = token.i + 1
        while doc[i].tag_ == "CD":
            phrase += doc[i].text + " "
            i += 1
        phrase = phrase[:-1]

        # split incase number like "50 thousand"
        d = phrase.split()
        if len(d) > 1:
            # make "50 thousand" a number
            if d[1] == "hundred":
                phrase = d[0] + "00"
                y = Decimal(sub(r"[^\d.]", "", phrase))
                phrase = "$" + "{:,}".format(y)
            elif d[1] == "thousand":
                phrase = d[0] + "000"
                y = Decimal(sub(r"[^\d.]", "", phrase))
                phrase = "$" + "{:,}".format(y)
            elif d[1] == "million":
                phrase = d[0] + "000000"
                y = Decimal(sub(r"[^\d.]", "", phrase))
                phrase = "$" + "{:,}".format(y)

        money += Decimal(sub(r"[^\d.]", "", phrase))
        moneyList.append(phrase)

    # if current text is a company name
    elif (
        token.pos_ == "PROPN"
        and token.dep_ == "pobj"
        or token.tag_ == "NNP"
        and doc[i - 1].text == "to"
        or doc[i - 1].text == "for"
        or doc[i - 1].text == "with"
    ):
        if token.text == "Inc.":
            continue
        companyList.append(token.text)

    # if token is >, we're at the end of that email
    elif token.text == ">":
        # two >>, only want to go in on the second >
        count += 1
        if count > 1:
            # add all money to total money
            totalMoney += money
            t = "{:,}".format(money)
            sentence_string += "$" + str(t) + " to "
            companyList2 = companyList.copy()

            # loop through company list and list out companies
            for x in list(companyList):
                if len(companyList) > 2:
                    sentence_string += x + ", "
                    companyList.remove(x)
                elif len(companyList) == 2:
                    sentence_string += x + " and "
                    companyList.remove(x)
                else:
                    sentence_string += x
                    companyList.remove(x)
            sentence_string += ". "

            # only want to do if there's more than one company so we're not listing same thing twice
            if len(companyList2) > 1:
                # loop through company list again to list price for each company
                for x, value in enumerate(list(companyList2)):
                    if len(companyList2) > 2:
                        sentence_string += moneyList[x] + " to " + value + ", "
                        companyList2.remove(value)
                    elif len(companyList2) == 2:
                        sentence_string += moneyList[x] + " to " + value + " and "
                        companyList2.remove(value)
                    else:
                        sentence_string += moneyList[x] + " to " + value + "."
                        companyList2.remove(value)
            sentence_string += "\n"
            # reset for <<END>>
            count = 0

# print out info
print(sentence_string)
l = "{:,.2f}".format(totalMoney)
print("Total Requests: $" + l)

f.close()