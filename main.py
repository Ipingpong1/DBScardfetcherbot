import re
import praw
import time
import calendar
import html

print("started!")

#opens both databses for shenanigans to ensue

f = open("cardDBNS.txt", "r")
f2 = open("cardDB.txt", "r")

#organizes databses as long af strings

text = f.read()
origText = f2.read()

#initiates the reddit instance using APIkey shenanigans

reddit = praw.Reddit(client_id='N1WzYawyMVj5pQ',
                     client_secret='mEboVkpQw3QHEo2u-rR66VGNAKc',
                     username='DBScardfetcher',
                     password='DBScardfetcher',
                     user_agent='DBScardfetcher by /u/ipingpong1')

#decodes html entities from reddit comments as some special characters are html encoded

reddit.config.decode_html_entities = True

#assigns subreddit for bot to work in

subreddit = reddit.subreddit('DBScardfetcher')

#this function takes in the cardName parameter, which is the string that is taken from the {} inside the comments
#it then removes spaces, apostrophes, commas, periods, and capital leaders (leaving in '//' for leaders), the function then takes the index of the cardName in the cardDBNS
#database and shenanigans to find the number ID and the original text counterpart in cardDB, it then puts everything in the reddit hyperlink format and returns it, if the index
#does not exist for cardName it returns ''

def findCardLink(cardName):
    try:
        cardNameNS = cardName.replace(' ','').replace(',', '').replace('’', '').replace('.', '').replace('-', '').lower()
        print(cardNameNS)
        index = text.index(cardNameNS)

        #idk how to properly use for loops in python so here are ghetto ass java equivalents

        temp = ""
        tempEq = ""
        tempVal = 0
        untilEq = 0
        tempFullCardName = ''
        untilFullName = 0
        fullCardName = ''

        while tempEq != "=":
            tempEq = text[index + len(cardNameNS) + untilEq:index + len(cardNameNS) + 1 + untilEq]
            untilEq = untilEq + 1

        untilEq = untilEq - 1

        while temp != ";":
            temp = text[index + tempVal: index + tempVal + 1]
            tempVal = tempVal + 1
        cardCode = text[index + 1 + len(cardNameNS) + untilEq:   index + tempVal - 1 + untilEq]
        cardCodeOnlyNum = re.sub("[^0-9]", "", cardCode)
        cardCodeNoHyper = ("https://www.dbs-decks.com/#!/cards/" + cardCodeOnlyNum)

        numIndex = origText.index(cardCodeOnlyNum)-1

        while tempFullCardName != ";":
            tempFullCardName = origText[numIndex-untilFullName]
            fullCardName = fullCardName + tempFullCardName
            untilFullName = untilFullName + 1

        fullCardName = fullCardName[::-1]
        fullCardName = fullCardName[2:len(fullCardName)-1]

        print('the full name is: ' + fullCardName)
        #################
        cardCodeHyper = ('|' + '[' + fullCardName + ']' + '(' + cardCodeNoHyper + ')' + '|')
        print(cardCodeOnlyNum)

        return cardCodeHyper
    except:
        return ''
#sets the bot to trigger at the sight of open curly boi

keyphrase = '{'

#makes it so the bot only responds to comments after its been launched, or else it will retroactively respond to
#every comment ever made with its keyphrase

starttime = calendar.timegm(time.gmtime())

#handles the responding and the card name fetching from the comments. Using regex it looks for the card names
#inside of the curly bois and then saves all instances of them in an array, a for loop then loops through the
#array of the instances and then applies the findCardLink function to them implementing each element of the array
#as a string parameter, it then links each one to the end of an empty string, the sum of which is then replied to the comment
#failure at any point will respond with "failed" for debug purposes

for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        reply = ''
        if starttime <= comment.created_utc:
            test = html.unescape(str(comment.body))
            print(test)
            cardArr = re.findall(r"\{([A-Za-z0-9\s\,\’]+)\}", test)
            print(cardArr)

            try:

                for i in cardArr:
                    reply = reply + findCardLink(i) + '  '
                comment.reply(reply)
                print(reply)
                reply = ''

            except:
                print('failed')


