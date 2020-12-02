import unittest
import os
from flask import Flask, render_template, request, session, flash, redirect, jsonify
from server import app
from model import connect_to_db, db, User, Drug, Device, example_data
import crud
import pwd_encrypt

#tests for the flask routes
class FlaskTests(unittest.TestCase):

    def setUp(self):
        # to do before every test
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///testdb')
        # Create tables
        db.create_all()

    def tearDown(self):
        # executed after each test
        db.session.close()
        db.drop_all()
    
    def test_homepage(self):
        # test homepage 
        result = self.client.get('/')
        self.assertIn(b'Click here', result.data)
    
    def test_login(self):
        # test login page
        return self.client.post('/login', data={'email': 'lucky@yahoo.com', 'password': 'Sample1234'}, follow_redirects=True)

    def test_logout(self):
        # test logout
        return self.client.get('/signout', follow_redirects=True)

    def test_add_user(self):
        # test add user page
        result = self.client.get('/add-user')
        self.assertIn(b'Create an account', result.data)
        
    def test_about(self):
        # test about page
        result = self.client.get('/about')
        self.assertIn(b'Click here', result.data)

    def test_contact_us(self):
        # test contact us page
        return self.client.post('/contactus', data={'name': 'Lucky One', 'email': 'lucky@yahoo.com', 'subject': 'Hello', 'message': 'How to do something?'}, follow_redirects=True)

if __name__ == "__main__":
    unittest.main()
