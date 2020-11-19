""" Flask routes """

import requests
import os
import json
from flask import Flask, render_template, request, session, flash, redirect, jsonify
from jinja2 import StrictUndefined

import crud
from model import connect_to_db

#API_KEY = os.environ['OPENFDA_API_KEY']
NEWSAPIKEY = os.environ['NEWS_API_KEY']

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """View homepage"""
    # get the news from newsapi
    """
    url = "http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=" + NEWSAPIKEY
    response = requests.get(url)
    response_json = response.json()
    articles = response_json['articles']
    jsonify(articles)
    """

    #data for charts from json files
    with open('data/drug_recall_total.json') as f:
        drug_recall_data = json.load(f)

    with open('data/device_recall_total.json') as f:
        device_recall_data = json.load(f)

    return render_template("homepage.html", drug_recall_data=drug_recall_data, device_recall_data=device_recall_data)

@app.route('/signin')
def signin():
    """View login page"""
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def user_login():
    """Log a user into the website"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.check_user_login_info(email, password)

    if user:
        #add user id to the session
        session["user_id"] = user.user_id
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("search.html", user=user, device=device, drug=drug)
    else:
        flash("Login info incorrect, please try again")
        return redirect('/signin')

@app.route('/about')
def about():
    """View about"""
    return render_template("about.html")

@app.route('/add-user')
def add_user():
    """View add user page"""
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_user():
    """add a user info to users table"""
    
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    tel_num = request.form.get('tel_num')
    caregiver_email = request.form.get('caregiver_email')
    
    user = crud.get_user_by_email(email)
    
    """Check to see if user is already in database"""
    if user:
        flash("This email already exists. Please try again")
        return redirect('/')
    else:
        user = crud.create_user(email, password, fname, lname, tel_num, caregiver_email)

        #add user id to the session
        session["user_id"] = user.user_id
        flash("Your account was created successfully")
        
        return redirect('/addupdate')

@app.route('/addupdate')
def add_update():
    """View add-update """

    user_id = session.get("user_id")

    if user_id:
        user = crud.get_user_by_id(user_id)
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("addupdate.html", user=user, device=device, drug=drug)
    else:
        flash("Please sign in")
        return render_template("login.html")

@app.route('/update_dd', methods=['POST'])
def update_dd():
    """ update the device nd drug tables"""

    user_id = session.get("user_id")
    #update or delete drugs/devices
    # get the selected options from the form
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            if key[0:3] == "dev":
                if value == "update":
                    devname = request.form.get('devname')
                    devmname = request.form.get('devmname')
                    device = crud.update_device(key[3:], devname, "", "", devmname, user_id)
                elif value == "delete":
                    crud.delete_device(key[3:])

            elif key[0:3] == "dru":
                if value == "update":
                    druname = request.form.get('druname')
                    drumname = request.form.get('drumname')
                    drug = crud.update_drug(key[3:], druname, "", "", drumname, user_id)
                elif value == "delete":
                    crud.delete_drug(key[3:])
            print(key,":", value)
    # get user info by user_id
    user = crud.get_user_by_id(user_id)
    #add drug/device for the user
    qtype = request.form.get('qtype')
    name = request.form.get('name')
    mname = request.form.get('mname')

    if qtype == "device":
        device = crud.add_device(name, "", "", mname, user.user_id)
    elif qtype == "drug":
        print(qtype, name, mname)
        drug = crud.add_drug(name, mname, user.user_id)
    
    #get a list of devices and drugs for the user
    device = crud.get_devices_by_user_id(user.user_id)
    drug = crud.get_drugs_by_user_id(user.user_id)

    return render_template("search.html", user=user, device=device, drug=drug)

@app.route('/search')
def search():
    """View search"""
    
    # get the list of drugs and devices for this user
    user_id = session.get("user_id")
    if user_id:
        user = crud.get_user_by_id(user_id)
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("search.html", user=user, device=device, drug=drug)
    else:
        flash("Please sign in")
        return render_template("login.html")

@app.route('/profile')
def profile():
    """View edit profile"""
    user_id = session.get("user_id")

    if user_id:
        user = crud.get_user_by_id(user_id)
        return render_template("profile.html", user=user)
    else:
        flash("Please sign in")
        return render_template("login.html")

@app.route('/update-profile', methods=['POST'])
def update_profile():
    """Update user records"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    tel_num = request.form.get('tel_num')
    caregiver_email = request.form.get('caregiver_email')

    user_id = session.get("user_id")
    user = crud.update_user(user_id, fname, lname, email, password, tel_num, caregiver_email)
    if user:
        flash("Update successful")
    else:
        flash("Oops! Something went wrong!")
        return redirect('/login')
    
    device = crud.get_devices_by_user_id(user.user_id)
    drug = crud.get_drugs_by_user_id(user.user_id)
    return render_template("search.html", user=user, device=device, drug=drug)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
