import unittest
import os
from server import app, session
import model
import crud
import pwd_encrypt

#tests for the flask routes
class FlaskTests(unittest.TestCase):

    def setUp(self):
        # to do before every test
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        # executed after each test
        pass
    
    def test_homepage(self):
        # test homepage 
        result = self.client.get('/')
        self.assertIn(b"MEDALERT", result.data)
    
    def test_login(self):
        # test login page
        return self.client.post("/login", data={"email": "lucky@yahoo.com", "password": "Sample1234"}, follow_redirects=True)

    def test_logout(self):
        # test logout
        return self.client.get("/signout", follow_redirects=True)


# tests for the database
class RDBTests(unittest.TestCase):
    #test if the model classes populate the tables correctly

    def setUp(self):
        #to do before very test
        connect_to_db(app, "postgresql:///medalert")
        db.drop_all()
        db.create_all()


    def tearDown(self):
        # to do after each test
        db.session.close()
        
if __name__ == "__main__":
    unittest.main()
