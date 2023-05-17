# views defines all the main website routes
# and the views they reference

import json, random
from database import db
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from database.models import Flight, Customer, Temp, Booking

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/flights/search", methods=["GET", "POST"])
def flights_search():
    if request.method == "POST":
        # get post data
        origin_code = request.form.get("origin")
        dest_code = request.form.get("dest")
        outbound_dt = request.form.get("leave_dt")
        inbound_dt = request.form.get("return_dt")
        # print(origin_code, dest_code, outbound_dt, inbound_dt)
        # perform preliminary checks
        if origin_code == dest_code:
            flash("Origin and destination locations are the same. Please try again.", category="error")
        else:
            # print(Flight.query.all())
            # outbound flights
            flights_out = Flight.query.filter(Flight.leave_dt.startswith(outbound_dt),
                                              Flight.origin_code.startswith(origin_code),
                                              Flight.dest_code.startswith(dest_code)).all()
            flights_in = Flight.query.filter(Flight.leave_dt.startswith(inbound_dt),
                                             Flight.origin_code.startswith(dest_code),
                                             Flight.dest_code.startswith(origin_code)).all()
            # print(flights_out)
            # print(flights_in)
            # TODO: problematic - this should ideally be a redirect
            return flights_found(out_flights=flights_out, in_flights=flights_in)
    return render_template("flights_search.html")


@views.route("/flights/found", methods=["GET", "POST"])
def flights_found(out_flights=None, in_flights=None):
    # now, we need display found flights
    return render_template("flights_found.html", outbound_flights=out_flights, inbound_flights=in_flights)


@views.route("/flights/book", methods=["GET", "POST"])
def flights_book():
    if request.method == "POST":
        # this is form data
        if request.form:
            title = request.form.get("title")
            f_name = request.form.get("first_name")
            l_name = request.form.get("last_name")
            email = request.form.get("email")
            mobile = request.form.get("mobile")
            outbound_flight_id = Temp.query.all()[0].flight_id
            inbound_flight_id = Temp.query.all()[1].flight_id
            outbound_flight = Flight.query.filter_by(id=outbound_flight_id).first()
            inbound_flight = Flight.query.filter_by(id=inbound_flight_id).first()

            # function to get a random booking ref
            def random_booking_ref():
                return chr(random.randint(65, 90)) + chr(random.randint(65, 90)) + chr(
                    random.randint(65, 90)) + str(
                    random.randint(0, 9)) + str(random.randint(0, 9)) + chr(random.randint(65, 90))

            # first, let's see we can find the customer first (email, mobile unique)

            customer = Customer.query.filter_by(email=email, mobile=mobile).first()
            if customer:
                # found the customer, now let's see if they have a booking
                if Booking.query.filter_by(booking_ref=customer.booking_ref).first():
                    flash("You already have an existing booking.", category="error")
                    flash("Want to change? Cancel the existing booking first.", category="info")
                # customer is there, but no booking, create one
                else:
                    # get a new booking reference
                    booking_ref = random_booking_ref()

                    while Booking.query.filter_by(booking_ref=booking_ref).all():
                        booking_ref = random_booking_ref()

                    new_booking = Booking(booking_ref, outbound_flight_id, inbound_flight_id,
                                          outbound_flight,
                                          inbound_flight)

                    db.session.add(new_booking)
                    customer.booking_ref = booking_ref
                    customer.booking = new_booking
                    db.session.commit()
                    flash("Booking confirmed: " + booking_ref + ". Thanks for booking with us!", category="success")
                    flash("To access your booking, login via the Manage page", category="info")

            # create a new booking and customer
            else:

                # get a new booking reference
                booking_ref = random_booking_ref()

                while Booking.query.filter_by(booking_ref=booking_ref).all():
                    booking_ref = random_booking_ref()

                new_booking = Booking(booking_ref, outbound_flight_id, inbound_flight_id, outbound_flight, inbound_flight)
                new_customer = Customer(title, f_name, l_name, email, mobile, booking_ref, new_booking)
                db.session.add(new_customer)
                db.session.add(new_booking)
                db.session.commit()
                flash("Booking confirmed: " + booking_ref + ". Thanks for booking with us!", category="success")
                flash("To access your booking, login via the Manage page", category="info")

            print(Booking.query.all())
            print(Customer.query.all())

            print("NOT EMPTY:", request.form)

        # ok so we're saving the latest flights selection in this temporary database
        else:
            db.session.query(Temp).delete()
            db.session.commit()
            selected_flights = json.loads(request.data)
            outbound_flight_id = selected_flights['outFlightId']
            inbound_flight_id = selected_flights['inFlightId']
            db.session.add(Temp(outbound_flight_id))
            db.session.add(Temp(inbound_flight_id))
            db.session.commit()
            print("EMPTY", request.form)

    return render_template("make_booking.html")


@views.route("/select_flights", methods=["GET", "POST"])
def make_booking():
    return redirect(url_for("views.flights_book"), code=307)


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
                    if customer.booking_ref == booking_ref:
                        flash("Successfully logged in!", category="success")
                        login_user(customer, remember=True)
                        return redirect(url_for("views.manage_booking"))
                flash("Incorrect booking reference. Please try again.", category="error")
            else:
                flash("This last name does not exist.", category="error")
    return render_template("manage.html")


@views.route("/manage/booking")
@login_required
def manage_booking():
    return render_template("manage_booking.html", user=current_user)

@views.route("/cancel_booking", methods=["POST"])
@login_required
def cancel_booking():
    booking = json.loads(request.data)
    booking_id = booking["bookingId"]
    booking_to_cancel = Booking.query.get(booking_id)
    if booking_to_cancel:
        if current_user.booking_ref == booking_to_cancel.booking_ref:
            db.session.delete(booking_to_cancel)
            current_user.booking = None
            db.session.commit()
            flash(f"Booking {booking_id} canceled!", category="error")
    return jsonify({})


@views.route("/exit")
@login_required
def exit_booking():
    logout_user()
    return redirect(url_for("views.manage"))

@views.route("/about_us")
def about_us():
    return render_template("about.html")


@views.route("/help")
def help_me():
    return render_template("help.html")
