from flask import (Blueprint, render_template, g, redirect, url_for, flash, request, jsonify)
from jpApp.db import (get_db, updateDB)


bp = Blueprint("main", __name__)

@bp.route('/wordList')
def wordList():
    db = get_db()
    jpWords = db.execute(
        'SELECT id, jpWord, pronunciation, meaning, dateRevised FROM jpVocab'
    ).fetchall()
    print("JP WORDS LIST: ")
    for item in jpWords:
        for x in item:
            print(x)
    flash("hi")
    return render_template('main/wordList.html', jpWords = jpWords)

@bp.route('/addWord', methods=('GET', 'POST'))
def addWord():
    if request.method == 'POST':
        jpWord = request.form['jpWord']
        pronunciation = request.form['pronunciation']
        meaning = request.form['meaning']
        error = None

        if not jpWord:
            error = "Please enter a japanese word."
        if not pronunciation:
            error = "Please enter the pronunciation"
        if not meaning:
            error = "Please enter the meaning"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO jpVocab (jpWord, pronunciation, meaning)'
                ' VALUES (?,?,?)',
                (jpWord, pronunciation, meaning)
            )
            db.commit()
            return redirect(url_for('main.wordList'))
    return render_template("main/addWord.html")


@bp.route('/clearAllRecords', methods=('GET', 'POST'))
def clearAllRecords():
    db = get_db()
    db.execute('DELETE FROM jpVocab')
    db.commit()
    return redirect(url_for("main.wordList"))


@bp.route('/dbRecords', methods=('GET', 'POST'))
def dbRecords():
    db = get_db()
    records = db.execute('SELECT * FROM jpVocab').fetchall()
    return render_template('main/dbRecords.html', records = records)
        
@bp.route('/')
def index():
    updateDB()
    return render_template('main/index.html')


@bp.route('/getJpWordInfo', methods=['GET'])
def getJpWordInfo():
    jpWord = request.args.get('jpWord')

    db = get_db()
    dbWord = db.execute(
        'SELECT * FROM jpVocab'
        ' WHERE jpWord = ?',
        (jpWord, )
    ).fetchone()
    meaning = dbWord['meaning']
    prc = dbWord['pronunciation']
    print("prc :  "  +prc)
    print("meaning: " +  meaning)
    json = jsonify({"meaning":meaning, "prc":prc}) 
    print(json)
    return json
    

