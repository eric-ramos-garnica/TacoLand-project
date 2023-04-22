from flask import Flask, render_template, request, flash, session, redirect,url_for
from model import connect_to_db, db
from model import Vendor,User,Rating
import cloudinary.uploader
import os
import requests
import json
import secrets

from jinja2 import StrictUndefined
#added the part after comma
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# importing cloudinary 
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dkyhrd8xs"
YELP_API_KEY = os.environ['YELP_API_KEY']
ENDPOINT = "https://api.yelp.com/v3/businesses/search"



# Replace this with routes and view functions!
@app.route("/")
def homepage(): 
    return render_template('homepage.html')

@app.route("/mexicanRestaurants")
def restaurants():
    #I used this so it wont give me an error when the form submits to get the api
    mexican_restaurants_data = ""
    return render_template("restaurants.html", mexican_restaurants_data=mexican_restaurants_data)

@app.route("/mexicanRestaurantsApi")
def restaurants_api():
    location = request.args.get("restaurantsLocation")
    
    HEADERS = {'Authorization': 'bearer %s' % YELP_API_KEY}

    #defines the parameters 
    PARAMETERS = { 
        'term':'Mexican restaurants',
        'limit': 6,
        'radius': 10000,
        'location': location
    }
    
    response = requests.get(url = ENDPOINT, params= PARAMETERS, headers= HEADERS)

    #convert to json string to a dictionary
    mexican_restaurants_data = response.json()
   #render to template with json
    return render_template("restaurants.html", mexican_restaurants_data = mexican_restaurants_data)
    # return mexican_restaurants_data
@app.route("/restaurantInfo/<id>")
def restaurant_info(id):
    # Make a GET request to the Yelp API to retrieve information for the specific restaurant with the given id
    headers = {'Authorization': 'bearer %s' % YELP_API_KEY}
    url = f'https://api.yelp.com/v3/businesses/{id}'
    response = requests.get(url, headers=headers)
    
    # Parse the response JSON to extract the relevant information
    # restaurant_data = json.loads(response.text)
    restaurant_data = response.json()
    name = restaurant_data['name']
    image_url = restaurant_data['image_url']
    rating = restaurant_data['rating']
    phone = restaurant_data['phone']
    address = ', '.join(restaurant_data['location']['display_address'])
    url = restaurant_data['url']
    coordinates = restaurant_data['coordinates']

    # Pass the extracted information to the template
    return render_template('restaurant_info.html', name=name, image_url=image_url, rating=rating, phone=phone, address=address, url=url, coordinates=coordinates)


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

@app.route("/filterByZipcodeAndCity")
def filter_zipcode_city():
    zipcode = request.args.get("zipcode")
    city = request.args.get("city")
    business_type = request.args.get("business_type_filter")
    if not zipcode:
        zipcode = None
    if not city:
        city = None
    # Rating average
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
    # checks for requirements
    if zipcode is None and city is None:
        vendors = Vendor.get_businesses_by_user_business_type(business_type)
    if zipcode is None and city is None and business_type == "all" :
        vendors = Vendor.get_vendor()
    if zipcode is not None and city is None:
        vendors = Vendor.get_businesses_by_zipcode_and_business_type(zipcode,business_type)
    if zipcode is not None and city is None and business_type == "all" :
        vendors = Vendor.get_businesses_by_zipcode(zipcode)
    if city is not None and zipcode is None:
        vendors = Vendor.get_businesses_by_city_and_business_type(city,business_type)
    if city is not None and zipcode is None and business_type == "all" :
        vendors = Vendor.get_businesses_by_city(city)
    if zipcode is not None and city is not None:
        vendors = Vendor.get_businesses_by_zipcode_city_business_type(zipcode,city,business_type)
    if zipcode is not None and city is not None and business_type == "all" :
        vendors = Vendor.get_businesses_by_zipcode_and_city(zipcode,city)

    return render_template('vendorspage.html',vendors=vendors,rating_dic=rating_dic)
    
@app.route("/rating/<vendor_id>")
def rating(vendor_id):
    """Will display rating page"""

    # User can rate one time per custumer, if user not login user will not be able to rate.
    if 'login' in session:                                              
        vendor_info = Vendor.get_vendor_by_id(vendor_id)
        # rating_obj = Rating.get_vendor_rating_by_user_id_and_vendor_id(session['id'],vendor_id)
        reviews = Rating.get_vendor_rating_by_id(vendor_id)
        
        # if rating_obj:
        #     flash("You can only rate one time per vendor")
        #     return redirect(f'/tacovendors/{vendor_id}')
        # else:
        return render_template('ratingpage.html',vendor_info=vendor_info,reviews=reviews)
    else:
        flash("Need to be logged in to rate!")
        return redirect(f'/tacovendors/{vendor_id}')
    
    
    

@app.route("/ratingSubmission/<vendor_id>", methods=["GET", "POST"])
def rating_submission(vendor_id):
    if request.method == "POST":
        score = request.form.get("rating")
        review = request.form.get("review")
        # save the rating to database or do something with it
        if "login" in session:
            rating_obj = Rating.get_vendor_rating_by_user_id_and_vendor_id(session['id'],vendor_id)
            if rating_obj:
                flash("You can only rate one time per vendor")
                return redirect(f'/rating/{vendor_id}')
            else:
                Rating.create(session['id'],vendor_id,score,review)
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
 
@app.route('/userRatingTopFive')
def user_rating_top_five():
    if 'login' in session:
        
        all_ratings_by_user = Rating.get_all_ratings_dec_sorted_scores_by_user_id(session['id'])
        # if all_ratings_by_user:
        #will store top 5 ratings in decending order
        top_five_array = []
        #will store top 5 vendor obj so we can use vendor info
        top_five_vendors_from_user = []
        #will store average rating by vendor
        top_five_vendors_rate = []
        
        for i in range(len(all_ratings_by_user)):
            top_five_array.append(all_ratings_by_user[i])
            vendor = Vendor.get_vendor_by_id(all_ratings_by_user[i].vendor_id)
            top_five_vendors_from_user.append(vendor)
            #calculating average
            vendor_ratings =Rating.get_vendor_rating_by_id(all_ratings_by_user[i].vendor_id)
            if vendor_ratings:
                rating_sum = 0
                for rating in vendor_ratings:
                    rating_sum += rating.score
                average=  rating_sum/len(vendor_ratings)
                round_rating = round(average)
                top_five_vendors_rate.append(round_rating)
        
        return render_template('user_rating_top_five.html', top_five_array=top_five_array,top_five_vendors_from_user=top_five_vendors_from_user,top_five_vendors_rate=top_five_vendors_rate)
        
@app.route('/userProfile')
def user_profile():
    user_info = User.get_user_info_by_user_id(session['id'])
    return render_template('user_profile.html',user_info=user_info)

@app.route('/userProfileEdit',methods=["POST"])
def profile_edit():

    user_info = User.get_user_info_by_user_id(session['id'])

    if 'login' in session:

        #gets image from user
        if 'my-file' in request.files:
            my_file = request.files.get('my-file')
            result = cloudinary.uploader.upload(my_file,
                    api_key=CLOUDINARY_KEY,
                    api_secret=CLOUDINARY_SECRET,
                    cloud_name=CLOUD_NAME)
            img_url = result['secure_url']
            
            if img_url:
                user_info.user_image = img_url
                db.session.commit()

        # gets phone # from user
        phone = request.form.get('user-phone-value')
        if phone:
            user_info.phone = phone
            db.session.commit()
        
        #gets gender from user
        gender = request.form.get('gender-value')
        if gender:
            user_info.gender = gender
            db.session.commit()
        
        #gets updated name
        fname = request.form.get('name')
        lname = request.form.get('lastname')

        if fname and lname:
            user_info.fname = fname
            user_info.lname = lname
            db.session.commit()

        return render_template('user_profile.html',user_info=user_info)

@app.route('/deleteAccount')
def delete_account():
    if 'login' in session:
        account_to_delete = User.get_user_info_by_user_id(session['id'])
        db.session.delete(account_to_delete)
        session.clear()
        db.session.commit()
        return render_template('deleteAccount.html')

    



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
