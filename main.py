import re
import praw
import time
import calendar
import html

print("started!")
f = open("cardDBNS.txt", "r")
f2 = open("cardDB.txt", "r")
text = f.read()
origText = f2.read()

reddit = praw.Reddit(client_id='put ur stuff here',
                     client_secret='put ur stuff here',
                     username='put ur stuff here',
                     password='put ur stuff here',
                     user_agent='DBScardfetcher by /u/ipingpong1')
reddit.config.decode_html_entities = True
subreddit = reddit.subreddit('DBScardfetcher')


def findCardLink(cardName):

    cardNameNS = cardName.replace(' ','').replace(',', '').replace('’', '').replace('.', '').replace('-', '').lower()
    print(cardNameNS)
    index = text.index(cardNameNS)

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
    #################FIND CARDNAME

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


keyphrase = '{'
starttime = calendar.timegm(time.gmtime())

for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        reply = ''
        if starttime <= comment.created_utc:
            #############################
            test = html.unescape(str(comment.body))
            print(test)
            ##############################([A-Za-z0-9_\s]+)
            cardArr = re.findall(r"\{([A-Za-z0-9\s\,\’]+)\}", test)
            print(cardArr)



            # cardName = comment.body.replace(keyphrase, '')
            try:
                # cardName = comment.body[comment.body.rindex('{') + 1:comment.body.rindex('}')].lower()
                # reply = ('|'+'['+cardName+']'+'('+findCardLink(cardName)+')'+'|')
                for i in cardArr:
                    reply = reply + findCardLink(i) + '  '
                comment.reply(reply)
                print(reply)
                reply = ''

            except:
                print('failed')

# cardName = input("enter card name: ")

# findCardValue(cardName)
