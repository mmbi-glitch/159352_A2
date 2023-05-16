# views defines all the main website routes
# and the views they reference

from flask import Blueprint, render_template, request, flash, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import *

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/flights")
def flights():
    return render_template("flights.html")

@views.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        # get post data
        booking_ref = request.form.get("booking_ref")
        last_name = request.form.get("last_name")
        # preliminary checks
        if len(last_name) < 2:
            flash("Invalid last name. Please try again.", category="error")
        elif len(booking_ref) != 6:
            flash("Booking reference is 6 characters long. Please try again.", category="error")
        else:
            # query customers table by last name
            customers = Customer.query.filter_by(last_name=last_name).all()
            print(customers)
            if customers:
                for customer in customers:
                    if check_password_hash(customer.booking_ref, booking_ref):
                        flash("Successfully logged in!", category="success")
                        login_user(customer, remember=True)
                        return redirect(url_for("views.booking"))
                flash("Incorrect booking reference. Please try again.", category="error")
            else:
                flash("This last name does not exist.", category="error")
    return render_template("manage.html")

@views.route("/about_us")
def about_us():
    return render_template("about.html")

@views.route("/help")
def help_me():
    return render_template("help.html")
