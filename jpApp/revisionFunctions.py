from jpApp.db import get_db
from jpApp.functions import *
from datetime import datetime

def checkInput(inputMeaning, inputPrc, dbWord):
    
    meanings = dbWord['meaning']
    meanings = meanings.split(',')
    
    wrong = False
    if not inputMeaning in meanings:
        print("Input Meaning: " + str(inputMeaning) + " db meaning: " + str(dbWord['meaning']))
        wrong = True
        print("meaning mismatch")
    if inputPrc != dbWord['pronunciation']:
        print("Input Prc: " + str(inputPrc) + " db prc: " + str(dbWord['pronunciation']))        
        wrong = True
        print("prc mismatch")
    return not wrong


def updateRevisionDB(word, correct):
    print("calling updateRevisionDb")
    db = get_db()
    learntDate = word['dateRevised']
    currDate = datetime.now()
    daysElapsed = (currDate - learntDate).days + 1
    print("Correct: " + str(correct))
    if correct: 
        #*2 our stability.
        currS = word['stability']
        newS = currS * 2

    else:
        #if its wrong, we need to drop the stability so that it pops up slightly more frequently.
        #we assume that our memory retainment of this word is now 0.05, we get our S accordingly.
        newS = getS(0.05, daysElapsed)

    #check whether its revisable.
    memoryRet = getR(newS, daysElapsed)
    print("Memory ret: " + str(memoryRet) + " word is: "+ word['jpWord'])
    if isRevisable(memoryRet):
        revisable = 1
    else:
        revisable = 0
        

    db.execute(
        'UPDATE studiedVocab SET stability = ?, revisable = ?'
        ' WHERE dict_id = ?',
        (newS, revisable, word['id'])
    )
    db.commit() 
    print("updated db from revision")


def getDBWordsForRevise(level):
    db = get_db()
    #get test words.
    testVocab = db.execute(
        'SELECT * FROM studiedVocab'
        ' LEFT JOIN coreJpDict ON studiedVocab.dict_id = coreJpDict.id'
        ' WHERE revisable = 1 AND coreJpDict.wordLevel = ?'
        ' ORDER BY stability ASC',
        (level, )
    ).fetchall()

    if len(testVocab) == 0:
        return None

    return testVocab

    
'''
if fail the test, set retainment to 0.05, compute s with getS
if pass the test, double stability value, compute r with getR

Our ideal stability value would be 512, if we hit 512, then it will take 1 year for us to retest.
'''
