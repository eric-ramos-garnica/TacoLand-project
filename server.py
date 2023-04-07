from flask import Flask, render_template, request, flash, session, redirect,url_for
from model import connect_to_db, db
from model import Vendor,User
import os

# import crud

from jinja2 import StrictUndefined
#added the part after comma
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
# app.config['UPLOAD_FOLDER'] = '/home/ericramosgarnica/src/tacoland/static/img'



# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage"""
    if 'login' in session:
        return render_template("/homepage_login.html") 
    else:  
        return render_template('homepage.html')

@app.route("/tacovendors")
def vendors():
    """view all vendors """
    vendors = Vendor.get_vendor()
    
    return render_template('vendorspage.html',vendors=vendors)

@app.route("/tacovendors/<vendor_id>")
def vendor_business(vendor_id):
    """Views a specific vendor """
    vendor_info = Vendor.get_vendor_by_id(vendor_id)
    return render_template('vendor_information.html',vendor_info=vendor_info)

@app.route("/createaccountpage")
def create_account():
    """Create account page"""
    return render_template('create_account.html')


@app.route("/createaccountpage",methods=["POST"])
def register_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_email_by_user(email)
    if user:
       flash("This email exist! Please enter a new email.")
    else:
        user =User.create(email,fname,lname,password)
        flash("Account created successfully! Please log in.")
    return redirect("/createaccountpage")

@app.route("/loginpage")
def loginpage():
    """Login page"""
    return render_template('login_page.html')

@app.route("/loginpage",methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    #getting email and password from database
    obj =User.get_email_by_user(email)
    # password_database = obj.password
    # email_database = obj.email
    if not obj or obj.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/loginpage')
    else:
        session['name'] = obj.fname
        session['login'] = "login"
        session['email'] = obj.email
        return render_template("/homepage_login.html")



@app.route("/vendorpage")
def create_vendor():
    """Vendor page"""
    return render_template('create_vendor_account.html')

@app.route("/vendorpage", methods=["POST"])
def vendor_info():
    vendor_name = request.form.get('vendorName')
    location = request.form.get('address')
    working_hours = request.form.get('hours')  
    zipcode = request.form.get('zipcode')
    state = request.form.get('state')
    city = request.form.get('city')
    image = request.form.get('image')
    
    # store data in database
    vendor = Vendor.create(vendor_name, location, working_hours, image, zipcode, state, city)
    if vendor:    
        flash("Account created successfully!")
        return redirect('/vendorpage')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
