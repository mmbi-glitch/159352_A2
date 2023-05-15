## Assignment 2 - 159352 (Flight Booking System)

---

### Brief

Design a **Web/Internet application** that implements an *online booking system* for a new airline that operates out of Dairy Flat Airport. 
The airline operates a number of light jet planes, allowing it to provide a highly specialized point-to-point service with Dairy Flat as its hub.  Use any of the tools and frameworks 
that are being covered in the course. Note that it is OK to have a “development” version rather than a “production”
version.

---

### Routes

The airline operates the following routes from Dairy Flat Airport:

1. A weekly "prestige" service to Hobart (Tasmania) using the SyberJet aircraft. The
outbound flight departs Dairy Flat on Friday early morning with the return inbound
flight departing Hobart on Sunday mid-afternoon (their time). Note: the outbound
flight first stops at Rotorua to pick up passengers before continuing on to Hobart. The
inbound flight returns directly to Dairy Flat without stopping.  

2. A twice daily shuttle service to Rotorua using one of the Cirrus jets. These operate
every weekday Monday–Friday. The first flight departs Dairy Flat early morning with
the return flight departing from Rotorua at noon. After turnaround, the next flight
departs Dairy Flat late afternoon, with the return flight departing Rotorua in the
evening.
 
3. A three times weekly service to Claris airport in Great Barrier Island using the other
Cirrus. The outbound flight departs Dairy Flat in the morning every Monday, Wednesday, and 
Friday. The return flight departs Great Barrier Island in the morning every
Tuesday, Thursday, and Saturday.

4. A twice-weekly service to Tuuta Airport in the Chatham Islands using one of the
HondaJets. The outbound flights depart Dairy Flat on Tuesday and Friday, with the
return flights departing Tuuta on Wednesday and Saturday.

5. A weekly service to Lake Tekapo in the South Island using the other HondaJet. Departs
Dairy Flat on Monday with the return flight departing Tekapo on Tuesday.

NOTES: 

- You are free to decide on the prices of the various legs of these flights. You can also
decide on how to allocate flight numbers.

- You will need to decide on flight times between the end points. Just decide on any
reasonable values. Note that, in this part of the world, westbound flights usually take
longer than eastbound flights

- The different timezones involved: mainland New Zealand (UTC+12), the Chatham
Islands (UTC+12:45), and Hobart (UTC+10)

- You can use the Great Circle Mapper, http://www.gcmap.com, to draw the routes
using the 4 letter ICAO codes: Dairy Flat (NZNE), Hobart (YMHB), Rotorua (NZRO),
Tuuta (NZCI), Claris (NZGB), and Lake Tekapo (NZTL).

---

### Requirements

You will need to decide on a suitable design for the front and back ends to meet the following
requirements. Your application should...
- feature a landing page that functions as the entry point for your application
- provide a feature to search for flights
- provide a service to allow a user to select a scheduled flight and make a booking
- have the capability for a user to cancel a booking

---

### Points to consider

1. **Business logic and functionality**
   - Includes how you organize user/customer and flight information according to the airline
   description and requirements. 
   - The user should be provided with a unique booking reference. 
   - A booking should not be allowed on scheduled flights that are full up. 
   - Your application should work with real calendar dates and not just the named days of the week.

2. **Ease of use**
   - The front end should provide as much guidance to the user as possible. 
   - In particular, it should allow the user to conveniently search for desired flights. 
   - On making a booking, the user should be presented with an invoice page summarizing the details of the flight, i.e. price, departure date and time, arrival time, etc.

3. **Presentation**
   - The front end output should be displayed in an attractive manner—you should do more than
   just show plain text and vanilla HTML. 
   - Feel free to make use of the various presentation tools covered in the course. 
   - However, do not overdo the graphics to the point where your
   application becomes difficult to use (as with some real sites).

4. **Deployment**
   - Your application should be packaged as a Docker image and be deployable in a Docker
   container
