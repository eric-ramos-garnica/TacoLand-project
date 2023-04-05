from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from model import Vendor,User
# import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage"""
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
    password_database = obj.password
    email_database = obj.email
    
    print('===>',password,'@@@@@@@',password_database)
    print('===>',email,'@@@@@@@',email_database)
    if password == password_database and email == email_database:
        # session["name"] = obj.name
        # session["login"] = "login"
        return redirect("/")
    # else:
    #     # flash("Incorrect password or email!")
    #     return redirect('/loginpage')


@app.route("/vendorpage")
def create_vendor():
    """Vendor page"""
    return render_template('create_vendor_account.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

