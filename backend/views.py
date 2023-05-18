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
    return render_template("home.html", user=current_user)


@views.route("/flights")
def flights_services():
    return render_template("flights_services.html", user=current_user)

@views.route("/flights/search", methods=["GET", "POST"])
def flights_search():
    return render_template("flights_search.html", user=current_user)


@views.route("/flights/found", methods=["GET", "POST"])
def flights_found():
    if request.method == "POST":
        # get post data
        origin_code = request.form.get("origin")
        dest_code = request.form.get("dest")
        outbound_dt = request.form.get("leave_dt")
        inbound_dt = request.form.get("return_dt")
        trip_type = request.form.get("trip_type")
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
            print("FLIGHTS_OUT:", flights_out)
            print("FLIGHTS_IN:", flights_in)
            if trip_type == "OneWay":
                return render_template("flights_found.html", outbound_flights=flights_out, round_trip=False, user=current_user)
            return render_template("flights_found.html", outbound_flights=flights_out, inbound_flights=flights_in,
                                   round_trip=True, user=current_user)
    # now, we need display found flights
    return render_template("flights_found.html", user=current_user)


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

            inbound_flight_id = ""
            inbound_flight = Flight()
            outbound_flight_id = Temp.query.all()[0].flight_id
            if Temp.query.count() == 2:
                inbound_flight_id = Temp.query.all()[1].flight_id
            outbound_flight = Flight.query.filter_by(id=outbound_flight_id).first()
            if Temp.query.count() == 2:
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
                    # differentiate
                    if Temp.query.count() == 2:
                        new_booking = Booking(booking_ref, outbound_flight_id,
                                                           outbound_flight, inbound_flight_id,
                                                           inbound_flight)
                        outbound_flight.seats -= 1
                        inbound_flight.seats -= 1
                    else:
                        new_booking = Booking(booking_ref, outbound_flight_id, outbound_flight)
                        outbound_flight.seats -= 1

                    db.session.add(new_booking)
                    customer.booking_ref = booking_ref
                    customer.booking = new_booking
                    db.session.commit()
                    flash("Booking confirmed: " + booking_ref + ". Thanks for booking with us!", category="success")
                    flash("To access your booking, login via the Manage page", category="info")

            # create a new booking and customer
            else:

                # customer email, mobile must be unique

                if Customer.query.filter_by(email=email).first():
                    flash("This email already exists.", category="error")
                elif Customer.query.filter_by(mobile=mobile).first():
                    flash("This mobile number already exists.", category="error")
                else:

                    # get a new booking reference
                    booking_ref = random_booking_ref()

                    while Booking.query.filter_by(booking_ref=booking_ref).all():
                        booking_ref = random_booking_ref()

                    # differentiate
                    if Temp.query.count() == 2:
                        new_booking = Booking(booking_ref, outbound_flight_id,
                                              outbound_flight, inbound_flight_id,
                                              inbound_flight)
                        outbound_flight.seats -= 1
                        inbound_flight.seats -= 1
                    else:
                        new_booking = Booking(booking_ref, outbound_flight_id, outbound_flight)
                        outbound_flight.seats -= 1

                    new_customer = Customer(title, f_name, l_name, email, mobile, booking_ref, new_booking)
                    db.session.add(new_booking)
                    db.session.add(new_customer)
                    db.session.commit()
                    flash("Booking confirmed: " + booking_ref + ". Thanks for booking with us!", category="success")
                    flash("To access your booking, login via the Manage page", category="info")

            print(Booking.query.all())
            print(Customer.query.all())

            print("NOT EMPTY:", request.form)

    return render_template("make_booking.html", user=current_user)


@views.route("/select_flights", methods=["GET", "POST"])
def flights_select():
    # ok so we're saving the latest flights selection in this temporary database
    selected_flights = json.loads(request.data)
    print("JSON_DATA: ", selected_flights)
    # if there is no data, then one or more flights not selected correctly
    if not selected_flights:
        flash("No outbound and/or inbound flights selected!", category="error")
        return jsonify({})
    else:
        # delete entries in temp table
        db.session.query(Temp).delete()
        db.session.commit()
        round_trip = selected_flights['roundTrip']
        if not round_trip:
            outbound_flight_id = selected_flights['outFlightId']
            db.session.add(Temp(outbound_flight_id))
            db.session.commit()
            print("Round Trip")
        else:
            outbound_flight_id = selected_flights['outFlightId']
            inbound_flight_id = selected_flights['inFlightId']
            db.session.add(Temp(outbound_flight_id))
            db.session.add(Temp(inbound_flight_id))
            db.session.commit()
            print("One-Way Trip")
        print(Temp.query.all())
        return redirect(url_for("views.flights_book"))


@views.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        # get post data
        booking_ref = request.form.get("booking_ref")
        email = request.form.get("email_req")
        # preliminary checks
        if len(booking_ref) != 6:
            flash("Booking reference is 6 characters long. Please try again.", category="error")
        else:
            # query customers table by last name
            customers = Customer.query.filter_by(email=email).all()
            print(customers)
            if customers:
                for customer in customers:
                    if customer.booking_ref == booking_ref:
                        flash("Successfully logged in!", category="success")
                        login_user(customer, remember=True)
                        return redirect(url_for("views.manage_booking"))
                flash("Incorrect booking reference. Please try again.", category="error")
            else:
                flash("This email does not exist.", category="error")
    return render_template("manage.html", user=current_user)


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
            flash(f"Booking {booking_to_cancel.booking_ref} canceled!", category="error")
            if booking_to_cancel.inbound_flight:
                booking_to_cancel.outbound_flight.seats += 1
                booking_to_cancel.inbound_flight.seats += 1
            else:
                booking_to_cancel.outbound_flight.seats += 1
            db.session.delete(booking_to_cancel)
            current_user.booking = None
            db.session.commit()

    return jsonify({})


@views.route("/exit")
@login_required
def exit_booking():
    logout_user()
    return redirect(url_for("views.manage"))