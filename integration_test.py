import unittest
import server
from server import app
from server import app,connect_to_db


class MyAppIntegrationTestCase(unittest.TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""

        app.config['SECRET_KEY'] = 'key'
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        self.client = app.test_client()


    def test_logout_homepage(self):
        """Testing <h1> when not login"""
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'<h1>Welcome to Taco Land</h1>',result.data)


    def test_anchor_tacoVendor_homepage(self):
        """Testing taco vendors anchor"""
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'<a href="/tacovendors">Taco Vendors</a>', result.data)
    
    def test_login_home_page(self):
        """Testing <h1> when login"""
        # Start each test with a user ID stored in the session.  
        with self.client as c:
            with c.session_transaction() as sess:
                sess['id'] = 23
                sess['login'] = "login"
                sess['name'] = 'eric'

        result = c.get("/")
        name_str = sess['name']
        self.assertIn(f"<h1>Welcome {name_str} to Taco Land</h1>", result.data.decode('utf-8'))
        
    def test_tacovendors_page(self):
        """Testing <h1> in tacoVendors server"""
        client = self.client
        result = client.get('/tacovendors')
        self.assertIn(b'<h1>All Vendors</h1>',result.data)
    

if __name__ == '__main__':
    connect_to_db(app)
    unittest.main()