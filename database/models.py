import pendulum as pdl
from . import db
from flask_login import UserMixin


# ----------- models-related stuff --------------- #

def icao_to_loc(code):
    match code:
        case "NZNE":
            return "Dairy Flat"
        case "YMHB":
            return "Hobart"
        case "NZRO":
            return "Rotorua"
        case "NZCI":
            return "Tuuta"
        case "NZGB":
            return "Claris"
        case "NZTL":
            return "Lake Tekapo"


class Flight(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    price = db.Column(db.Integer)
    max_seats = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    origin = db.Column(db.String(20))
    dest = db.Column(db.String(20))
    origin_code = db.Column(db.String(4))
    dest_code = db.Column(db.String(4))
    leave_dt = db.Column(db.TIMESTAMP(timezone=True))
    arrival_dt = db.Column(db.TIMESTAMP(timezone=True))
    operator = db.Column(db.String(20), default="MilkRun Airways")
    aircraft_model = db.Column(db.String(20))
    stopover = db.Column(db.String(20))

    def __init__(self, flight_id=None, max_seats=None, price=None, origin_code=None, dest_code=None, leave_dt=None, arrival_dt=None,
                 stopover=None, aircraft_model=None):
        self.id = flight_id
        self.max_seats = max_seats
        self.seats = max_seats
        self.price = price
        self.origin_code = origin_code
        self.dest_code = dest_code
        self.origin = icao_to_loc(origin_code)
        self.dest = icao_to_loc(dest_code)
        self.leave_dt = leave_dt
        self.arrival_dt = arrival_dt
        self.stopover = icao_to_loc(stopover)
        self.aircraft_model = aircraft_model

    def __repr__(self):
        return f"Flight('ID:{self.id}', 'ORG:{self.origin}', 'DEST:{self.dest}', OUT_DT:'{self.leave_dt}', 'IN_DT:{self.arrival_dt}')"


class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.String(20), db.ForeignKey("flight.id"))

    def __init__(self, flight_id):
        self.flight_id = flight_id


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_ref = db.Column(db.String(20))
    outbound_flight_id = db.Column(db.String(20), db.ForeignKey("flight.id"))
    inbound_flight_id = db.Column(db.String(20), db.ForeignKey("flight.id"))
    outbound_flight = db.relationship("Flight", foreign_keys=[inbound_flight_id])
    inbound_flight = db.relationship("Flight", foreign_keys=[outbound_flight_id])

    def __init__(self, booking_ref=None, outbound_flight_id=None, outbound_flight=None,
                 inbound_flight_id=None, inbound_flight=None):
        print(booking_ref, outbound_flight_id, inbound_flight_id, outbound_flight, inbound_flight)
        self.booking_ref = booking_ref
        self.outbound_flight_id = outbound_flight_id
        self.inbound_flight_id = inbound_flight_id
        self.outbound_flight = outbound_flight
        self.inbound_flight = inbound_flight

    def __repr__(self):
        return f"Booking('{self.booking_ref}', '{self.outbound_flight_id}', '{self.inbound_flight_id}')"


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    booking_ref = db.Column(db.String(20), db.ForeignKey("booking.booking_ref"))
    booking = db.relationship("Booking", foreign_keys=[booking_ref])

    def __init__(self, title, first_name, last_name, email, mobile, booking_ref, booking):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile = mobile
        self.booking_ref = booking_ref
        self.booking = booking

    def __repr__(self):
        return f"Customer('{self.first_name}', '{self.last_name}', '{self.booking_ref}')"


# ------------- test data (for entirety of 2023) ---------------- #

def get_dates_of_certain_day(start_date: pdl.DateTime, certain_day: pdl.constants):
    dates = list()
    date_object = start_date

    if date_object.weekday() != (certain_day - 1) % 7:
        date_object = date_object.next(certain_day)

    while date_object.year == start_date.year:
        dates.append(date_object)
        date_object = date_object.add(days=7)

    return dates


# ------------ outbound flights ------------------ #

outbound_flights = list()
outbound_count = 100

# 1st Service - syberjet plane
outbound_dates = get_dates_of_certain_day(pdl.today("Pacific/Auckland"), pdl.FRIDAY)

for date in outbound_dates:
    # print(date)
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=8, minute=30, tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(hours=3, minutes=50)).in_tz("Australia/Hobart")
    outbound_flights.append(
        Flight("NH" + str(outbound_count), 6, 320, "NZNE", "YMHB", outbound_dt, inbound_dt, "NZRO", "SyberJet SJ30i"))
    outbound_count += 1

# 2nd service - 1st cirrus plane

outbound_dates.clear()

for day in [pdl.MONDAY, pdl.TUESDAY, pdl.WEDNESDAY, pdl.THURSDAY, pdl.FRIDAY]:
    outbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in outbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=7, minute=45, tz="Pacific/Auckland")
    outbound_dt_2 = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=17, minute=15,
                                 tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(minutes=45))
    outbound_flights.append(
        Flight("NR" + str(outbound_count), 4, 70, "NZNE", "NZRO", outbound_dt, inbound_dt, "", "Cirrus SF50"))
    outbound_count += 1
    inbound_dt = (outbound_dt_2.add(minutes=45))
    outbound_flights.append(
        Flight("NR" + str(outbound_count), 4, 70, "NZNE", "NZRO", outbound_dt_2, inbound_dt, "", "Cirrus SF50"))
    outbound_count += 1

# 3rd service - 2nd cirrus plane

outbound_dates.clear()

for day in [pdl.MONDAY, pdl.WEDNESDAY, pdl.FRIDAY]:
    outbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in outbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=10, minute=45,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(minutes=20))
    outbound_flights.append(
        Flight("NG" + str(outbound_count), 4, 70, "NZNE", "NZGB", outbound_dt, inbound_dt, "", "Cirrus SF50"))
    outbound_count += 1

# 4th service - 1st honda jet

outbound_dates.clear()

for day in [pdl.TUESDAY, pdl.FRIDAY]:
    outbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in outbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=14, minute=15,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(hours=2, minutes=15))
    outbound_flights.append(
        Flight("NC" + str(outbound_count), 5, 360, "NZNE", "NZCI", outbound_dt, inbound_dt, "", "HondaJet Elite"))
    outbound_count += 1

# 5th service - 2nd honda jet

outbound_dates.clear()

outbound_dates = get_dates_of_certain_day(pdl.today("Pacific/Auckland"), pdl.MONDAY)

for date in outbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=16, minute=35,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(hours=3, minutes=10))
    outbound_flights.append(
        Flight("NT" + str(outbound_count), 5, 120, "NZNE", "NZTL", outbound_dt, inbound_dt, "", "HondaJet Elite"))
    outbound_count += 1

print("outbound:", len(outbound_flights), outbound_count)

outbound_dates.clear()

# --------------- inbound flights ----------------------- #

inbound_flights = list()
inbound_count = 100

# 1st Service - syberjet plane
inbound_dates = get_dates_of_certain_day(pdl.today("Australia/Hobart"), pdl.SUNDAY)

for date in inbound_dates:
    # print(date)
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=14, minute=15,
                               tz="Australia/Hobart")
    inbound_dt = (outbound_dt.add(hours=3, minutes=50)).in_tz("Pacific/Auckland")
    inbound_flights.append(
        Flight("HN" + str(inbound_count), 6, 320, "YMHB", "NZNE", outbound_dt, inbound_dt, "", "SyberJet SJ30i"))
    inbound_count += 1

# 2nd service - 1st cirrus plane

inbound_dates.clear()

for day in [pdl.MONDAY, pdl.TUESDAY, pdl.WEDNESDAY, pdl.THURSDAY, pdl.FRIDAY]:
    inbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in inbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=12, tz="Pacific/Auckland")
    outbound_dt_2 = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=20, minute=15,
                                 tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(minutes=45))
    inbound_flights.append(
        Flight("RN" + str(inbound_count), 4, 70, "NZRO", "NZNE", outbound_dt, inbound_dt, "", "Cirrus SF50"))
    inbound_count += 1
    inbound_dt = (outbound_dt_2.add(minutes=45))
    inbound_flights.append(
        Flight("RN" + str(inbound_count), 4, 70, "NZRO", "NZNE", outbound_dt_2, inbound_dt, "", "Cirrus SF50"))
    inbound_count += 1

# 3rd service - 2nd cirrus plane

inbound_dates.clear()

for day in [pdl.TUESDAY, pdl.THURSDAY, pdl.SATURDAY]:
    inbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in inbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=10, minute=45,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(minutes=20))
    inbound_flights.append(
        Flight("GN" + str(inbound_count), 4, 70, "NZGB", "NZNE", outbound_dt, inbound_dt, "", "Cirrus SF50"))
    inbound_count += 1

# 4th service - 1st honda jet

inbound_dates.clear()

for day in [pdl.WEDNESDAY, pdl.SATURDAY]:
    inbound_dates.extend(get_dates_of_certain_day(pdl.today("Pacific/Auckland"), day))

for date in inbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=10, minute=15,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(hours=2, minutes=15))
    inbound_flights.append(
        Flight("CN" + str(inbound_count), 5, 360, "NZCI", "NZNE", outbound_dt, inbound_dt, "", "HondaJet Elite"))
    inbound_count += 1

# 5th service - 2nd honda jet

inbound_dates.clear()

inbound_dates = get_dates_of_certain_day(pdl.today("Pacific/Auckland"), pdl.TUESDAY)

for date in outbound_dates:
    outbound_dt = pdl.datetime(year=date.year, month=date.month, day=date.day, hour=17, minute=25,
                               tz="Pacific/Auckland")
    inbound_dt = (outbound_dt.add(hours=3, minutes=10))
    inbound_flights.append(
        Flight("TN" + str(inbound_count), 5, 320, "NZTL", "NZNE", outbound_dt, inbound_dt, "", "HondaJet Elite"))
    inbound_count += 1

print("inbound:", len(inbound_flights), inbound_count)

inbound_dates.clear()
flights = outbound_flights + inbound_flights
print("both:", len(flights))
