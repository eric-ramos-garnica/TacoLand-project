import unittest
from server import app
from model import db,Rating, connect_to_db

class UserTestCase(unittest.TestCase):
        
    def test_get_ratings(self):
        # test the method
        results = Rating.get_ratings()
        assert len(results) == 11

    def test_get_vendor_rating_by_id(self):
        vendor_id = 1
        # test the method
        results = Rating.get_vendor_rating_by_id(vendor_id)
        assert len(results) == 11

    def test_get_vendor_rating_by_user_id_and_vendor_id(self):
        user_id = 1
        vendor_id = 1
        obj = Rating.get_vendor_rating_by_user_id_and_vendor_id(user_id, vendor_id)
        assert len(obj) == 1

    def test_get_all_ratings_dec_sorted_scores_by_user_id(self):
        user_id = 1
        objs = Rating.get_all_ratings_dec_sorted_scores_by_user_id(user_id)
        scores = []
        for obj in objs:
            scores.append(obj.score)
        assert scores == sorted(scores, reverse=True)

    def test_get_rating_obj_by_user_id(self):
        user_id = 1
        rating_obj = Rating.get_rating_obj_by_user_id(user_id)
        assert isinstance(rating_obj, Rating)# is an assertion statement that checks whether the rating_obj variable is an instance of the Rating class
        assert rating_obj.user_id == user_id
        


if __name__ =="__main__":
    connect_to_db(app)
    unittest.main()