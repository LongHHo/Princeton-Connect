#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv
from database import searchEntry, insertEntry, getAll
from sys import argv, stderr, exit
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
import entryInfo
import json
from CASClient import CASClient

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

# Generated by os.urandom(16)
app.secret_key = b'\xcdt\x8dn\xe1\xbdW\x9d[}yJ\xfc\xa3~/'

#-----------------------------------------------------------------------
# Very basic interface to search for entries in the database. Still need
# interface to search for entries
#-----------------------------------------------------------------------

@app.route('/')
@app.route('/templates/home')
def home():

    username = CASClient().authenticate()

    html = render_template('home.html')
    response = make_response(html)
    return response
    


#-----------------------------------------------------------------------


@app.route('/templates/submit')
def submit():
    try:
        username = CASClient().authenticate()

        markersData = getAll() #getting all the user info
        html = render_template('submit.html', markersData=json.dumps(markersData))
        response = make_response(html)
        return response
    except Exception as e:
        print(e, file=stderr)

#-----------------------------------------------------------------------

# can only search for entries in database, not a function to insert
@app.route('/templates/lookup')
def lookup():
    try:
            username = CASClient().authenticate()

            netid = request.args.get('netid')
            name = request.args.get('name')
            email = request.args.get('email')
            phone = request.args.get('phone')
            description = request.args.get('description')
            address = request.args.get('address')

            print(description)
            user = entryInfo.entryInfo()
            user.setNetid(netid)
            user.setName(name)
            user.setEmail(email)
            user.setPhone(phone)
            user.setDescription(description)
            user.setAddress(address)

            userEntries = searchEntry(user)

            html = render_template('lookup.html',
                userEntries=userEntries)
            response = make_response(html)

            return response
    except Exception as e:
        html = render_template('error.html', error=e)
        response = make_response(html)
        return response

@app.route('/templates/handleSubmit', methods=['GET'])
def handleSubmit():
    try:
        
        username = CASClient().authenticate()


        netid = request.args.get('netid')
        name = request.args.get('name')
        email = request.args.get('email')
        phone = request.args.get('phone')
        description = request.args.get('description')
        address = request.args.get('address')

        
        entry = entryInfo.entryInfo(name, netid, email, phone, description, address)
        insertEntry(entry)
      
        # Step 1: Display entry, if it is not None

        # Step 2: Have option to EDIT and DELETE entry
        markersData = getAll()
        html = render_template('submit.html', markersData=json.dumps(markersData))
        response = make_response(html)
        return response
    except Exception as e:
        print(e, file=stderr)


#-----------------------------------------------------------------------

# @app.route('/searchresults')
# def searchResults():

#     username = CASClient().authenticate()

#     author = request.args.get('author')
#     if (author is None) or (author.strip() == ''):
#         errorMsg = 'Please type an author name.'
#         return redirect(url_for('searchForm', errorMsg=errorMsg))

#     session['prevAuthor'] = author

#     database = Database()
#     database.connect()
#     books = database.search(author)
#     database.disconnect()

#     html = render_template('searchresults.html',
#         ampm=getAmPm(),
#         currentTime=getCurrentTime(),
#         username=username,
#         author=author,
#         books=books)
#     response = make_response(html)
#     return response

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
