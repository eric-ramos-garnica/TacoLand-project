from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Rating(db.Model):

    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    vender_id = db.Column(db.Integer,db.ForeignKey("venders.vender_id"))
    score = db.Column(db.Integer)
    
    #relationship with User and Vender class
    user = db.relationship("User", back_populates="ratings")
    vender = db.relationship("Vender", back_populates = "ratings")

    def __repr__(self):
        return f"<<(RatingClass) rating_id={self.rating_id} score ={self.score}>>"
    
    @classmethod
    def create(cls,user,vender,score):
        obj = cls(user=user,vender=vender,score=score)
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
    

class Vender(db.Model):

    __tablename__ = "venders"

    vender_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    vender_name = db.Column(db.String)
    location = db.Column(db.String)
    working_hours = db.Column(db.String)
    menu = db.Column(db.String)

    #relationship with Rating
    ratings = db.relationship("Rating", back_populates = "vender")
    
    def __repr__(self):
        return f"<<(VenderClass) vender_id={self.vender_id} location={self.location} hours={self.working_hours}>>"
   
    
    @classmethod
    def create(cls,vender_name,location,working_hours,menu):
        """Creates venders"""
        obj = cls(vender_name=vender_name,location=location,working_hours=working_hours,menu=menu)
        db.session.add(obj)
        db.session.commit()
        return obj



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
