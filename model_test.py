import unittest
from server import app
from model import db,User, connect_to_db


class UserTestCase(unittest.TestCase):
    def test_get_email_by_user(self):
        email = 'eric@gmail.com'
        user = User.get_email_by_user(email)
        assert email == user.email 



if __name__ =="__main__":
    connect_to_db(app)
    unittest.main()