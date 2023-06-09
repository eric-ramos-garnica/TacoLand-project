from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, select


db = SQLAlchemy()

class Rating(db.Model):

    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    vendor_id = db.Column(db.Integer,db.ForeignKey("vendors.vendor_id"))
    score = db.Column(db.Integer)
    review =db.Column(db.String)
    photo = db.Column(db.String, nullable =True )
    
    #relationship with User and Vender class
    user = db.relationship("User", back_populates="ratings")
    vendor = db.relationship("Vendor", back_populates = "ratings")

    def __repr__(self):
        return f"<<(RatingClass) rating_id={self.rating_id} score ={self.score}>>"
    
    @classmethod
    def create(cls,user_id,vendor_id,score,review,photo):
        obj = cls(user_id=user_id,vendor_id=vendor_id,score=score,review=review,photo=photo) 
        db.session.add(obj)
        db.session.commit()
        return obj
    @classmethod
    def get_ratings(cls):
        return Rating.query.all()
    @classmethod
    def get_vendor_rating_by_id(cls,id):
        return Rating.query.filter_by(vendor_id = id).all()
    @classmethod
    def get_vendor_rating_by_user_id_and_vendor_id(cls,user_id,vendor_id):
        return Rating.query.filter((Rating.user_id == user_id) & (Rating.vendor_id == vendor_id)).all()
    @classmethod
    def get_all_ratings_dec_sorted_scores_by_user_id(cls,user_id):
        all_ratings_by_user = Rating.query.filter(Rating.user_id == user_id)
        return all_ratings_by_user.order_by(desc(Rating.score)).all()
    @classmethod
    def get_rating_obj_by_user_id(cls,user_id):
        return Rating.query.filter_by(user_id = user_id).first()
   


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    email = db.Column(db.String, unique = True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    password = db.Column(db.String)
    user_image = db.Column(db.String, nullable =True)
    phone =db.Column(db.String,nullable =True)
    gender = db.Column(db.String,nullable =True)

    #relationship with Rating
    ratings = db.relationship("Rating", back_populates = "user")
    vendors = db.relationship("Vendor", back_populates = "user")

    def __repr__(self):
        return f"<<(UserCLass) user_id ={self.user_id} email={self.email}>>"
    
    @classmethod
    def create(cls, email, fname,lname,password):
        """Creates users"""
        obj = cls(email=email,fname=fname,lname=lname,password=password)
        db.session.add(obj)
        db.session.commit()
        return obj
    @classmethod
    def get_email_by_user(cls,email):
        """return email if its in the database"""         
        return User.query.filter(User.email == email).first()
    @classmethod
    def get_user_info_by_user_id(cls,user_id):
        return User.query.filter_by(user_id = user_id).first()
    

class Vendor(db.Model):

    __tablename__ = "vendors"

    vendor_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    vendor_name = db.Column(db.String)
    location = db.Column(db.String)
    working_hours = db.Column(db.String)
    image = db.Column(db.String)
    zipcode =db.Column(db.Integer)
    state = db.Column(db.String)
    city = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    coords = db.Column(db.String)
    business_type = db.Column(db.String)
    
    #relationship with Rating
    ratings = db.relationship("Rating", back_populates = "vendor")
    user = db.relationship("User", back_populates = "vendors")
    
    def __repr__(self):
        return f"<<(VenderClass) vendor_id={self.vendor_id} location={self.location} hours={self.working_hours}>>"
   
    
    @classmethod
    def create(cls,vendor_name,location,working_hours,image,zipcode,state,city,user_id,coords,business_type):
        """Creates venders"""
        obj = cls(vendor_name=vendor_name,location=location,working_hours=working_hours,image=image,zipcode=zipcode,state=state,city=city,user_id =user_id, coords=coords, business_type=business_type)
        db.session.add(obj)
        db.session.commit()
        return obj
    @classmethod
    def get_vendor(cls):
        return Vendor.query.all()
    @classmethod
    def get_vendor_by_id(cls,vendor_id):
        """Returns a vendor by primary key"""
        return Vendor.query.get(vendor_id)
    @classmethod
    def get_businesses_by_user_id(cls,id):
        """Retunrs business by user/owner """
        return Vendor.query.filter_by(user_id = id).all()
    @classmethod
    def get_businesses_by_user_business_type(cls,vendor_type):
        return Vendor.query.filter_by(business_type=vendor_type)
    @classmethod
    def get_businesses_by_zipcode_and_business_type(cls,zipcode,business_type):
        return Vendor.query.filter((Vendor.zipcode == zipcode) & (Vendor.business_type == business_type))
    @classmethod
    def get_businesses_by_zipcode(cls,zipcode):
        return Vendor.query.filter_by(zipcode=zipcode)
    @classmethod
    def get_businesses_by_city_and_business_type(cls,city,business_type):
        return Vendor.query.filter((Vendor.city == city) & (Vendor.business_type == business_type))
    @classmethod
    def get_businesses_by_city(cls,city):
        return Vendor.query.filter_by(city=city)
    @classmethod
    def get_businesses_by_zipcode_city_business_type(cls,zipcode,city,business_type):
        return Vendor.query.filter((Vendor.zipcode == zipcode) & (Vendor.city == city) & (Vendor.business_type == business_type))
    @classmethod
    def get_businesses_by_zipcode_and_city(cls,zipcode,city):
        return Vendor.query.filter((Vendor.zipcode == zipcode) & (Vendor.city == city))


def connect_to_db(flask_app, db_uri="postgresql:///tacoratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()