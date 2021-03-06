from flask import (Blueprint, render_template, g, redirect, url_for, flash, request, jsonify)
from jpApp.db import get_db
from datetime import datetime
from jpApp.revisionFunctions import *




import math
bp = Blueprint("revision", __name__)


@bp.route('/revise/<int:level>', methods=('GET','POST'))
def revise(level):
    words = getDBWordsForRevise(level)
    if words is None:
        return redirect(url_for("revision.noWordsForTest"))

    currWord = words[0]
    return render_template('revision/reviseVocab.html', reviseWord = currWord, currLevel=level)

@bp.route('/selectLevel', methods=('GET','POST'))
def selectLevel(): 
    return render_template('revision/levelPage.html')

@bp.route('/noWordsForTest', methods=('GET',))
def noWordsForTest():
    return render_template('revision/noWordsForTest.html')


#We will do all the processing here instead of in the revise function.
@bp.route('/revision/processUserInput', methods=['GET'])
def processUserInput():    
    print("Cheeck user Input api called")
    uMeaning = request.args.get('userMeaning')
    uPrc = request.args.get('userPrc')
    id = request.args.get('id')

    #get the db word.
    db = get_db()
    dbWord = db.execute(
        'SELECT * FROM studiedVocab'
        ' LEFT JOIN coreJpDict ON studiedVocab.dict_id = coreJpDict.id'
        ' WHERE coreJpDict.id = ?',
        (id, )
        ).fetchone()

    print('-----fetching from db...')

    xd = db.execute(
        'SELECT * FROM studiedVocab'
        ' LEFT JOIN coreJpDict ON studiedVocab.dict_id = coreJpDict.id'
    )
    
    for word in xd:
        print(word.keys())
        print(word['id'], word['jpWord'], word['dict_id'], word['meaning'])
    
    
    print("From user printed at backend server--")
    print(uMeaning)
    print(uPrc)
    correct = checkInput(uMeaning, uPrc, dbWord)
    updateRevisionDB(dbWord, correct)
    
    return jsonify({"validInput": correct})

