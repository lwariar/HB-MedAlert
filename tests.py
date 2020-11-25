import unittest
from server import app, session
import model
import pwd_encrypt

#tests for the flask routes
class FlaskTests(unittest.TestCase):

    def setUp(self):
        # to do before every test
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_login(self):
        # test login page
        result = self.client.post("/login", data={"email": "lucky@yahoo.com", "password": "Sample1234"}, follow_redirects=True)
        self.assertIn(b"Search for regulatory warnings", result.data)
    
    def test_homepage(self):
        # test homepage 
        result = self.client.get('/')
        self.assertIn(b"Welcome", result.data)

"""
# tests for the database
class RDBTests(unittest.TestCase):
    #test if the model classes populate the tables correctly

    def setUp(self):
        #to do before very test
        connect_to_db(app, "postgresql:///mytestdb")
        db.create_all()


    def tearDown(self):
        # to do after each test
        db.session.close()
        db.drop_all()
"""
if __name__ == "__main__":
    unittest.main()
