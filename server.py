""" Flask routes """

import requests
import os
import json
from flask import Flask, render_template, request, session, flash, redirect, jsonify
from jinja2 import StrictUndefined
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

import crud
from model import connect_to_db
import pwd_encrypt
from twilio.rest import Client

NEWSAPIKEY = os.environ['NEWS_API_KEY']
#Twilio cccount info
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_TEST_NUMBER']

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """View homepage"""
    
    if 'user_id' not in session:
        session['user_id'] = ''
        
    news_articles = []
    # get the news from newsapi
    try:
        url = 'http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=' + NEWSAPIKEY
        response = requests.get(url)
        response_json = response.json()
        articles = response_json['articles']
        jsonify(articles)
        
        # get the first three articles
        
        for i in range(0,3):
            news_articles.append(articles[i])
    
    except requests.exceptions.RequestException as e: 
        print('NewsAPI not responding!!!')

    #data for charts from json files
    with open('data/drug_recall_total.json') as f:
        drug_recall_data = json.load(f)

    with open('data/device_recall_total.json') as f:
        device_recall_data = json.load(f)

    return render_template('homepage.html', news_articles=news_articles, 
            drug_recall_data=drug_recall_data, device_recall_data=device_recall_data)

@app.route('/signin')
def signin():
    """View login page"""
    return render_template('login.html') 

@app.route('/signout')
def signout():
    """logout"""
    #remove the user id from session
    session['user_id'] = ''
    return redirect('/')

@app.route('/login', methods=['POST'])
def user_login():
    """Log a user into the website"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_password(email)
    #encrypt the password
    decoded_pwd = pwd_encrypt.decrypt_message(user.password)
    
    if decoded_pwd == password:
        #if user:
        #add user id to the session
        session['user_id'] = user.user_id
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template('search.html', user=user, device=device, drug=drug)
    else:
        flash('Login info incorrect, please try again')
        return redirect('/signin')

@app.route('/about')
def about():
    """View about"""

    user_id = session.get('user_id')

    if user_id:
        user = crud.get_user_by_id(user_id)
        return render_template('about.html', user=user)
    else:
        flash('Please sign in')
        return render_template('login.html')

@app.route('/contactus', methods=['POST'])
def contactus():
    """Send an email"""
    
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    MY_ADDRESS = 'medalert_lw@outlook.com'
    PASSWORD = 'Sample1234'

    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()       # create a message

    # setup the parameters of the message
    msg['From']='medalert_lw@outlook.com'
    msg['To']=email
    msg['Subject']="From MedAlert - " + subject

    # add in the message body
    message = 'Thank you for your email. We will get back to you as soon as possible.\n\n' + message
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    server.send_message(msg)
    
    del msg
    return redirect('/')

@app.route('/add-user')
def add_user():
    """View add user page"""
    return render_template('register.html')

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
    
    #Check to see if user is already in database
    if user:
        flash('This email already exists. Please try again')
        return redirect('/')
    else:
        #encrypt the password
        encoded_pwd = pwd_encrypt.encrypt_message(password)
    
        # create user and add to table
        user = crud.create_user(email, encoded_pwd, fname, lname, tel_num, caregiver_email)

        #add user id to the session
        session['user_id'] = user.user_id
        return redirect('/addupdate')

@app.route('/addupdate')
def add_update():
    """View add-update """

    user_id = session.get('user_id')

    if user_id:
        user = crud.get_user_by_id(user_id)
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template('addupdate.html', user=user, device=device, drug=drug)
    else:
        flash('Please sign in')
        return render_template('login.html')

@app.route('/update_dd', methods=['POST'])
def update_dd():
    """ update the device and drug tables"""

    user_id = session.get('user_id')
    #update or delete drugs/devices
    # get the selected options from the form
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            if key[0:3] == 'dev':
                if value == 'update':
                    devname = request.form.get('devname')
                    devmname = request.form.get('devmname')
                    device = crud.update_device(key[3:], devname, '', '', devmname, user_id)
                elif value == 'delete':
                    crud.delete_device(key[3:])

            elif key[0:3] == 'dru':
                if value == 'update':
                    druname = request.form.get('druname')
                    drumname = request.form.get('drumname')
                    drug = crud.update_drug(key[3:], druname, drumname, user_id)
                elif value == 'delete':
                    crud.delete_drug(key[3:])
    # get user info by user_id
    user = crud.get_user_by_id(user_id)
    #add drug/device for the user
    qtype = request.form.get('qtype')
    name = request.form.get('name')
    mname = request.form.get('mname')

    if qtype == 'device':
        device = crud.add_device(name, '', '', mname, user.user_id)
    elif qtype == 'drug':
        drug = crud.add_drug(name, mname, user.user_id)
    
    #get a list of devices and drugs for the user
    device = crud.get_devices_by_user_id(user.user_id)
    drug = crud.get_drugs_by_user_id(user.user_id)

    return render_template('search.html', user=user, device=device, drug=drug)

@app.route('/search')
def search():
    """View search"""
    
    # get the list of drugs and devices for this user
    user_id = session.get('user_id')
    if user_id:
        user = crud.get_user_by_id(user_id)
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template('search.html', user=user, device=device, drug=drug)
    else:
        flash('Please sign in')
        return render_template('login.html')

@app.route('/profile')
def profile():
    """View edit profile"""

    user_id = session.get('user_id')

    if user_id:
        user = crud.get_user_by_id(user_id)
        pwd = pwd_encrypt.decrypt_message(user.password)
        return render_template('profile.html', user=user, pwd=pwd)
    else:
        flash('Please sign in')
        return render_template('login.html')

@app.route('/update-profile', methods=['POST'])
def update_profile():
    """Update user records"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    tel_num = request.form.get('tel_num')
    caregiver_email = request.form.get('caregiver_email')

    user_id = session.get('user_id')
    encoded_pwd = pwd_encrypt.encrypt_message(password)
    user = crud.update_user(user_id, fname, lname, email, encoded_pwd, tel_num, caregiver_email)
    if user:
        device = crud.get_devices_by_user_id(user.user_id)
        drug = crud.get_drugs_by_user_id(user.user_id)
        return render_template('search.html', user=user, device=device, drug=drug)
    else:
        flash('Oops! Something went wrong!')
        return redirect('/login')

@app.route('/smsthis')
def sms_results():
    """SMS the results to the user via Twilio"""

    sms_body = 'Hello'

    print("in sms this")

    client = Client(account_sid, auth_token)
    message = client.messages.create(body=sms_body, from_=twilio_number, to='+17632189128')
    print(message.sid)
    return redirect('/')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
