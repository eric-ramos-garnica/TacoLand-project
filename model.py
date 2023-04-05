from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Rating(db.Model):

    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    vendor_id = db.Column(db.Integer,db.ForeignKey("vendors.vendor_id"))
    score = db.Column(db.Integer)
    
    #relationship with User and Vender class
    user = db.relationship("User", back_populates="ratings")
    vendor = db.relationship("Vendor", back_populates = "ratings")

    def __repr__(self):
        return f"<<(RatingClass) rating_id={self.rating_id} score ={self.score}>>"
    
    @classmethod
    def create(cls,user,vendor,score):
        obj = cls(user=user,vendor=vendor,score=score)
        db.session.add(obj)
        db.session.commit()
        return obj
    


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    email = db.Column(db.String, unique = True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    password = db.Column(db.String)

    #relationship with Rating
    ratings = db.relationship("Rating", back_populates = "user")

    def __repr__(self):
        return f"<<(UserCLass) user_id ={self.user_id} email={self.email_id}>>"
    
    @classmethod
    def create(cls, email, fname,lname,password):
        """Creates users"""
        obj = cls(email=email,fname=fname,lname=lname,password=password)
        db.session.add(obj)
        db.session.commit()
        return obj
    

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



    #relationship with Rating
    ratings = db.relationship("Rating", back_populates = "vendor")
    
    def __repr__(self):
        return f"<<(VenderClass) vendor_id={self.vendor_id} location={self.location} hours={self.working_hours}>>"
   
    
    @classmethod
    def create(cls,vendor_name,location,working_hours,image,zipcode,state,city):
        """Creates venders"""
        obj = cls(vendor_name=vendor_name,location=location,working_hours=working_hours,image=image,zipcode=zipcode,state=state,city=city)
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
