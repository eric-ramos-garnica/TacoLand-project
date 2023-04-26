import unittest
from server import app
from model import db, Vendor,connect_to_db

class VendorTestcase(unittest.TestCase):
    def test_get_vendor(self):
        vendors = Vendor.get_vendor()
        # Assert that the correct number of vendors were returned
        self.assertEqual(len(vendors), 4)

    def test_get_vendor_by_id(self):
        id = 1
        obj = Vendor.get_vendor_by_id(id)
        assert id == obj.user_id

    def test_get_businesses_by_user_id(self):
        id = 18
        business=Vendor.get_businesses_by_user_id(id)
        businesses_amount = len(business)
        assert 3 == businesses_amount
    
    def test_get_businesses_by_user_business_type(self):
        Vendor_type_truck = 'taco truck'
        obj_truck = Vendor.get_businesses_by_user_business_type(Vendor_type_truck)
        vendor_truck_total = len(obj_truck.all())
        assert 4 == vendor_truck_total

        Vendor_type_stand = 'taco stand'
        obj_stand = Vendor.get_businesses_by_user_business_type(Vendor_type_stand)
        vendor_stand_total = len(obj_stand.all())
        assert 0 == vendor_stand_total
    
    def test_get_businesses_by_zipcode_and_business_type(self):
         # test the method with a valid zipcode and business type
        results = Vendor.get_businesses_by_zipcode_and_business_type('95035', 'taco truck').all()
        assert len(results) == 4
        # test the method with an invalid business type
        results = Vendor.get_businesses_by_zipcode_and_business_type('12345', 'pizza truck').all()
        assert len(results) == 0
        # test the method with an invalid zipcode
        results = Vendor.get_businesses_by_zipcode_and_business_type('99999', 'taco truck').all()
        assert len(results) == 0

    def test_get_businesses_by_zipcode(self):
        # test the method with a valid zipcode
        results = Vendor.get_businesses_by_zipcode('95035').all()
        assert len(results) == 4
        # test the method with an invalid zipcode
        results = Vendor.get_businesses_by_zipcode('99999').all()
        assert len(results) == 0

    def test_get_businesses_by_city_and_business_type(self):
        # test the method with a valid city and business type
        results = Vendor.get_businesses_by_city_and_business_type('milpitas', 'taco truck').all()
        assert 3 == len(results) 
        # test the method with an invalid city
        results = Vendor.get_businesses_by_city_and_business_type('New York', 'taco truck').all()
        assert len(results) == 0
        # test the method with an invalid business type
        results = Vendor.get_businesses_by_city_and_business_type('Los Angeles', 'pizza truck').all()
        assert len(results) == 0
        # test the method with both invalid criteria
        results = Vendor.get_businesses_by_city_and_business_type('New York', 'pizza truck').all()
        assert len(results) == 0

    def test_get_businesses_by_city(self):
        # test the method with a valid city
        results = Vendor.get_businesses_by_city('milpitas').all()
        assert len(results) == 3
        # test the method with an invalid city
        results = Vendor.get_businesses_by_city('New York').all()
        assert len(results) == 0

    def test_get_businesses_by_zipcode_city_business_type(self):
        # test the method with valid criteria
        results = Vendor.get_businesses_by_zipcode_city_business_type('95035', 'milpitas', 'taco truck').all()
        assert len(results) == 3
        # test the method with invalid criteria
        results = Vendor.get_businesses_by_zipcode_city_business_type('94110', 'Los Angeles', 'taco truck').all()
        assert len(results) == 0

    def test_get_businesses_by_zipcode_and_city(self):
        # test the method with valid criteria
        results = Vendor.get_businesses_by_zipcode_and_city('95035', 'milpitas').all()
        assert len(results) == 3
        # test the method with invalid criteria
        results = Vendor.get_businesses_by_zipcode_and_city('94110', 'Los Angeles').all()
        assert len(results) == 0
    

if __name__ =="__main__":
    connect_to_db(app)
    unittest.main()