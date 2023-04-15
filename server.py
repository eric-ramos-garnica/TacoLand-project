from flask import Flask, render_template, request, flash, session, redirect,url_for
from model import connect_to_db, db
from model import Vendor,User,Rating
import cloudinary.uploader
import os

from jinja2 import StrictUndefined
#added the part after comma
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# importing cloudinary 
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dkyhrd8xs"





# Replace this with routes and view functions!
@app.route("/")
def homepage():  
    return render_template('homepage.html')

@app.route("/tacovendors")
def vendors():
    """view all vendors """
    vendors = Vendor.get_vendor()
    #rating object
    ratings =Rating.get_ratings()
    rating_dic ={}
    rating_set =set()
    for obj in ratings:
        rating_set.add(obj.vendor_id)

    for vendor_id in rating_set:
        vendor_ratings =Rating.get_vendor_rating_by_id(vendor_id)
        if vendor_ratings:
            rating_sum = 0
            for rating in vendor_ratings:
                rating_sum += rating.score
            average=  rating_sum/len(vendor_ratings)
            round_rating = round(average)
            rating_dic[vendor_id] = round_rating
    
    # filter by all vendors,taco trucks,taco stands 
    
    return render_template('vendorspage.html',vendors=vendors,rating_dic=rating_dic)
        

@app.route("/tacovendors/<vendor_id>")
def vendor_business(vendor_id):
    """Views a specific vendor """
    #returns all vendor objects with specific vendor id
    vendor_info = Vendor.get_vendor_by_id(vendor_id)
    
   #returns all rating objects with specific vendor id
    vendor_ratings =Rating.get_vendor_rating_by_id(vendor_id)
    #getting average for rating

    if vendor_ratings:
        rating_sum = 0
        for rating in vendor_ratings:
            rating_sum += rating.score
        average=  rating_sum/len(vendor_ratings)
        round_rating = round(average)
    else:
        round_rating = 0

    if vendor_info is None:
        return render_template('vendor_information.html',vendor_info=vendor_info,rating=round_rating)
    
    return render_template('vendor_information.html',vendor_info=vendor_info,rating=round_rating)

@app.route("/filtervendors/<filter_choice>")
def filters(filter_choice):
    ratings =Rating.get_ratings()
    rating_dic ={}
    rating_set =set()
    for obj in ratings:
        rating_set.add(obj.vendor_id)

    for vendor_id in rating_set:
        vendor_ratings =Rating.get_vendor_rating_by_id(vendor_id)
        if vendor_ratings:
            rating_sum = 0
            for rating in vendor_ratings:
                rating_sum += rating.score
            average=  rating_sum/len(vendor_ratings)
            round_rating = round(average)
            rating_dic[vendor_id] = round_rating
    if filter_choice == 'taco stand' or filter_choice == 'taco truck':
        vendors = Vendor.get_businesses_by_user_business_type(filter_choice)
    elif filter_choice == 'all':
        vendors = Vendor.get_vendor()
    return render_template('vendorspage.html',vendors=vendors,rating_dic=rating_dic)

    
@app.route("/rating/<vendor_id>")
def rating(vendor_id):
    """Will display rating page"""
    vendor_info = Vendor.get_vendor_by_id(vendor_id)
    return render_template('ratingpage.html',vendor_info=vendor_info)
    

@app.route("/ratingSubmission/<vendor_id>", methods=["GET", "POST"])
def rating_submission(vendor_id):
    if request.method == "POST":
        score = request.form.get("rating")
        # save the rating to database or do something with it
        if "login" in session:
            Rating.create(session['id'],vendor_id,score)
        else:
            Rating.create(None,vendor_id,score)
        return render_template('ratingSubmission.html')

    # return redirect(url_for("rating", vendor_id=vendor_id)) //i dont know if i need it but everything works without
    
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
        session['id'] = obj.user_id
        session['login'] = "login"
        session['email'] = obj.email
        return redirect("/")
    
@app.route("/logout")
def logout():
    if 'login' in session:
        session.clear()
    return redirect('/')
    
@app.route("/sellerPage")
def seller_page():
    """Will display vendor sign up and vendor Info"""
    return render_template('seller_page.html')

@app.route("/vendorpage")
def create_vendor():
    """Vendor page"""
    if 'login' in session:
        return render_template('create_vendor_account.html')
    else:
        flash("Need to login to sign up")
        return redirect('/sellerPage')

@app.route("/vendorpage", methods=["POST"])
def vendor_info():
    if 'login' in session:
        vendorname = request.form.get('vendorName')
        location = request.form.get('address')
        workinghours = request.form.get('hours')  
        zipcode = request.form.get('zipcode')
        state = request.form.get('state')
        city = request.form.get('city')
        coords = request.form.get('coordinates')
        my_file = request.files.get('my-file')
        result = cloudinary.uploader.upload(my_file,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME)
        img_url = result['secure_url']
        business_type = request.form.get('business_type')
    
        vendor = Vendor.create(vendorname, location, workinghours, img_url, zipcode, state, city,session['id'],coords,business_type)
        if vendor:    
            flash("Account created successfully!")
            return redirect('/vendorpage')
    else:
        flash("Need to login to create a vendor account")
        return redirect("/vendorpage")
    

     
@app.route("/vendorInfo")
def vendor_account():
    """Will show all business from owner/user """
    if 'login' in session:
        user_businesses = Vendor.get_businesses_by_user_id(session['id'])
        return render_template('vendor_info_by_owner.html',user_businesses=user_businesses)
    else:
        flash("Need to login to see vendor info")
        return redirect('/sellerPage')
    
@app.route("/BusinessEdit/<vendor_id>")
def edit(vendor_id):
    if "login" in session:
        session['edit'] = True
        session['vendor_id'] = vendor_id
        # return redirect('/vendorpage')
        return render_template( "edit.html")
    
@app.route("/editpage", methods=["POST"])
def edit_page():
    if 'login' in session and 'edit' in session and session['edit'] == True:

        vendorname = request.form.get('vendorName')
        location = request.form.get('address')
        workinghours = request.form.get('hours')  
        zipcode = request.form.get('zipcode')
        state = request.form.get('state')
        city = request.form.get('city')
        coords = request.form.get('coordinates')
        my_file = request.files.get('my-file')
        result = cloudinary.uploader.upload(my_file,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME)
        img_url = result['secure_url']
        business_type = request.form.get('business_type')

        # updating vendor information
        vendor = Vendor.get_vendor_by_id(session['vendor_id'])
        vendor.vendor_name = vendorname
        vendor.location = location
        vendor.working_hours = workinghours
        vendor.zipcode = zipcode
        vendor.state = state
        vendor.city = city
        vendor.image = img_url
        vendor.coords = coords
        vendor.business_type = business_type
        del session['edit']
        del session['vendor_id']
        db.session.commit()
        return redirect('/vendorInfo')
    
@app.route("/deleteVendorAccount")
def delete():
    """Deletes vendor account"""
    if 'login' in session:
        vendor = Vendor.get_vendor_by_id(session['vendor_id'])
        db.session.delete(vendor)
        db.session.commit()
        return redirect("/vendorInfo")
# 


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
