""" APIs,Flask routes """

import requests
import os
from flask import Flask, render_template, request, session, flash, redirect
from jinja2 import StrictUndefined

import crud
from model import connect_to_db


API_KEY = os.environ['OPENFDA_API_KEY']

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """View login"""
    
    return render_template("login.html")

@app.route('/about')
def about():
    """View about"""
    
    return render_template("about.html")

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
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("profile.html", user=user, device=device, drug=drug)
    else:
        flash("Please sign in")
        return render_template("login.html")


@app.route('/signin')
def signin():
    """View login page"""
    
    return render_template("login.html")

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

        #add drug/device for the user
        qtype = request.form.get('qtype')
        name = request.form.get('name')
        mname = request.form.get('mname')

        if qtype == 'device':
            # model_num = request.form.get('model_num') // we're not using this now
            # serial_num = request.form.get('serial_num')
            device = crud.add_device(name, "", "", mname, user.user_id)
        elif qtype == "drug':":
            drug = crud.add_drug(name, mname, user.user_id)
        #add user id to the session
        session["user_id"] = user.user_id
        flash("Your account was created successfully")
    
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("search.html", user=user, device=device, drug=drug)

@app.route('/login', methods=['POST'])
def user_login():
    """Log a user into the website"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.check_user_login_info(email, password)

    if user:
        #add user id to the session
        if "user_id" not in session:
            session["user_id"] = user.user_id
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template("search.html", user=user, device=device, drug=drug)
    else:
        flash("Login info incorrect, please try again")
        return redirect('/signin')

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
        #add drug/device for the user
        qtype = request.form.get('qtype')
        name = request.form.get('name')
        mname = request.form.get('mname')

        if qtype == 'device':
            device = crud.add_device(name, "", "", mname, user.user_id)
        elif qtype == "drug':":
            drug = crud.add_drug(name, mname, user.user_id)
        flash("Update successful")
    else:
        flash("Oops! Something went wrong!")
    
    device = crud.get_devices_by_user_id(user.user_id)
    drug = crud.get_drugs_by_user_id(user.user_id)
    return render_template("search.html", user=user, device=device, drug=drug)

# @app.route('/query', methods=['POST'])
# def query():
#     """build a query based on user input"""

#     qtype = request.form.get('qtype')
#     search_term = request.form.get('search_term')
#     print(qtype, search_term)

#     URL = f'https://api.fda.gov/{qtype}/enforcement.json?search=product_description:RANITIDINE&limit=10'

#     data = requests.get(URL).json()

#     for result in data.get('results', []):
#         print(result['product_description'])
#         print(result['reason_for_recall'])
#         print('*****************************************************************************************************')

#     return redirect('/')
# """
# """
# URL = 'https://api.fda.gov/drug/event.json?search=patient.reaction.reactionmeddrapt:"fatigue"&limit=5'

# 'https://api.fda.gov/device/event.json?search=device.generic_name:glucometer&limit=1'

# URL = 'https://api.fda.gov/drug/enforcement.json?search=product_description:RANITIDINE&limit=10'

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
