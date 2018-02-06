# a python text emotion analyzer

import operator, re, sys, pprint

# delimiters = ['\n', ' ', ',', '.', '?']

inputThes = 'inputThes.txt'
inputFile = 'inputFile.txt'


# turn a csv into a returned list
def convcsvtolist(inputcsv):
    csvlist = []
    for word in re.split(',', inputcsv):
        csvlist.append(word)
    return csvlist


# read in text, separate by words, remove extra things,
# count the words and occurance of words

# dumb print a dictionary
def dprint(thislist):
    for stuff in thislist:
        print stuff, " ", thislist[stuff]
    return


# dumb print a list
def lprint(thislist):
    for stuff in thislist:
        print(stuff)
    return


# notangry,nothappy,veryhappy,verysad,coldfeet
# this does not fit into the reading in word in files
# mechanism - hard coding words is bad
# but this works with our method of scanning the files
# need to get these from the thesaurus thing
# to handle two word phrases
def exception(prevword, word, dblword):
    for thisword in dblword:
        w1, w2 = thisword.split()
        if prevword == w1 and word == w2:
            return w1 + w2
    return word


def stripEndingLf(word):
    word = word.replace("\n", "")
    return word.replace("\r", "")


def stripInnerSpace(word):
    word = word.replace(" ", "")
    return word


def clean(word):
    thisone = word.replace("(", "")
    thisone = thisone.replace(":", "")
    thisone = thisone.replace(";", "")
    thisone = thisone.replace("^", "")
    thisone = thisone.replace("=", "")
    thisone = thisone.replace("\r\n", "")
    thisone = thisone.replace("\x97", "")
    thisone = thisone.replace("\"", "")
    thisone = thisone.replace("\r", "")
    thisone = thisone.replace("\n", "")
    return thisone.replace(")", "")


def initializeThesaurus(myInput):
    athes = []
    dblword = []
    myThes = {'': ''}

    # input the thesaurus right now (spelling sorry)
    for line in open(myInput, 'r').readlines():
        if line[0] != '#':  # allow comments at first column
            athes.append(line)

            # really need to divide up into sublist
    for line in athes:
        ptr = 1
        for word in re.split(',', line):
            word = stripEndingLf(word)
            # if multiword then combine but note for other
            # process
            if len(word.split()) == 2:
                dblword.append(word);
            word = word.replace(" ", "")
            if (ptr == 1):
                special = word
                myThes[special] = word
            if ptr > 1:
                myThes[special] = myThes[special] + ',' + word
            ptr += 1
    return myThes, dblword


# input and initialize the input text file
def initializeText(inputFile):
    myReadText = {"": 1}
    bigcount = 0
    prevword = ""
    # read in the words and count them
    for line in open(inputFile, 'r').readlines():
        for word in re.split('[ |,|.|\?]', line):
            word = clean(word)
            # exceptions
            word = exception(prevword, word, dblword)
            bigcount += 1
            if len(word) > 0:
                if (word in myReadText):
                    myReadText[word] = myReadText[word] + 1
                else:
                    myReadText[word] = 1
            prevword = word
    return myReadText, bigcount


# main below Main below MAIN below =>

# read in the command line options - if any
# updates the global variables inputFile and thesFile
print "starting"

if len(sys.argv) > 1 and sys.argv[1] != 'null':
    inputFile = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] != 'null':
        thesFile = sys.argv[2]

# read in the thesaurus text
# thesword = {'':''}
thesword, dblword = initializeThesaurus(inputThes)
print "read in thesesaurus"
# correctly reading in all the text
###for thing in thesword:
###    print thesword[thing]

# for things in thesword:
#    print things,":",thesword[things]

# read in the text to be analyzed
# readText = {"":1}
readText, bigcount = initializeText(inputFile)
print "read in text"

# for things in readText:
#    print things,":",readText[things]

# now we have the readText amd the text we go through it
# and process it
for x in readText:
    for w in thesword:
        m = convcsvtolist(thesword[w])
        if x in convcsvtolist(thesword[w]):
            # need to append differently - use dict entry
            # readText[x] = str(readText[x]) + ',' + clean(thesword[w]) + ',' + w
            readText[x] = str(readText[x]) + ',' + w.upper()

# then sort it
sorted_readText = sorted(readText.items(), key=operator.itemgetter(1))

# prints everything but we extract the desired stuff below
# for item in sorted_readText:
#    print item

nextList = []
# below is ALL the separate words
# we need to combine them into the categories
# defined by the Thesaurus
for item in sorted_readText:
    #    print item
    if len(item[0]) > 0:
        try:
            value = int(item[1])
        except ValueError:
            nextList.append(item[1])

# the output of this is:
# (word,#words)  or   E.g., ('and', 15015)
# (word,#,emotionword)    E.g., ('repugnant', '1,DISGUST')

# below combines words with emotions and sums them for same emotions
# and discards non-emotion words
nextDict = {'': 1}
for item in nextList:
    thing2, thing1 = item.split(',')
    if thing1 in nextDict:
        nextDict[thing1] = int(nextDict[thing1]) + int(thing2)
    else:
        nextDict[thing1] = int(thing2)
print

# need a pretty print
for item in nextDict:
    #    print item
    if len(item) > 0:
        print("%8s\t%4s" % (item, nextDict[item]))

# this is the count of unique words in the dictionary
print "\ntotal distinct emotion words: ","\t",len(nextDict)-1
print "total entries: ","\t\t",len(nextList)
print "distinct words: ","\t\t", len(readText)
print "words total: ","\t\t\t", bigcount,"\n"

