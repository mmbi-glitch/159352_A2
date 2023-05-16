# views defines all the main website routes
# and the views they reference

from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/flights")
def flights():
    return render_template("flights.html")

@views.route("/manage")
def manage():
    return render_template("manage.html")

@views.route("/about_us")
def about_us():
    return render_template("about.html")

@views.route("/help")
def help():
    return render_template("help.html")
