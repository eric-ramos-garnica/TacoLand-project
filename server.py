from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from model import Vendor
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


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

