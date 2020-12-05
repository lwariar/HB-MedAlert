![alt text](https://github.com/lwariar/HB-MedAlert/blob/main/static/img/MedAlert_icon_2.PNG "MedAlert")


__MED*alert*__ is a tool that allows a user to search for regulatory warnings or recalls issued for their pharmaceuticals and/or medical devices. Users can register and add a list of drugs and devices they would like to monitor. If the user finds recall notifications, they can get advice from their healthcare provider about the risks and benefits. The app uses the openFDA API (Food and Drug Administration) as the data source on FDA actions.

Features for the first sprint include: 
1. Allow a user to Sign In using a user name and password 
2. Register a new user and be able to edit the user profile 
3. Add, update or delete a list of drugs or devices for each user 
4. Search for and display the results using the openFDA API 
5. E-mail the results to the user

### Project Tech Stack:
    Python, Flask, SQLAlchemy, PostgreSQL, JavaScript, JQuery, AJAX, HTML, CSS, Bootstrap, Jinja, Chart.js

### APIs:
    openFDA, newsapi

### Installation:
Clone this repository
Create and activate a virtual environment

    $ pip3 install virtualenv
    $ virtualenv env
    $ source env/bin/activate

Install dependencies

    (env) $ pip3 install -r requirements.txt

Create a secrets.sh file and save your API secret key
Activate the secrets.sh file

    (env) $ source secrets.sh

Create the database

    (env) $ createdb medalert
    (env) $ python3 model.py

Start the backend server:

    (env) $ python3 server.py

Open a new window/tab on your browser to localhost:5000

### Future Implementation:
    The app will automatically notify the user via email or text message of any recalls
    Autocomplete for names of drugs and devices