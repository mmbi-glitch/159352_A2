function hideReturnDate(changeElement, currentElement) {
    changeElement.style.display = currentElement.value === "Return" ? 'block' : 'none';
    document.getElementById("return_dt").required = currentElement.value === "Return";
}

function selectFlight(current_flight, list_of_flights) {
    for (let child of list_of_flights.children) {
        if (child.className.includes("active")) {
            child.className = "list-group-item list-group-item-action";
        }
    }
    current_flight.className = "list-group-item list-group-item-action active"
}

function bookFlights(outbound_flights, inbound_flights, round_trip) {
    let selOutFlight = undefined;
    let selInFlight = undefined;
    // search for outbound flights
    for (let child of outbound_flights.children) {
        if (child.className.includes("active")) {
            selOutFlight = child;
        }
    }
    // search for inbound flights, only if it's defined!
    if (round_trip === true) {
        for (let child of inbound_flights.children) {
            if (child.className.includes("active")) {
                selInFlight = child;
            }
        }
    }

    if ((selOutFlight !== undefined)) {
        let outFlightId = selOutFlight.querySelector('.card-title').innerText;
        let inFlightId = undefined;
        if ((selInFlight !== undefined)) {
            inFlightId = selInFlight.querySelector('.card-title').innerText;
        }
        if (outFlightId !== undefined && inFlightId !== undefined) {
            fetch("/select_flights", {
                method: "POST",
                body: JSON.stringify({
                    outFlightId: outFlightId.replace("Flight ", ""),
                    inFlightId: inFlightId.replace("Flight ", ""),
                    roundTrip: round_trip
                })
            }).then(r => {
                console.log(r.url);
                location.replace(r.url);
            });
        } else if (round_trip === false && outFlightId !== undefined) {
            fetch("/select_flights", {
                method: "POST",
                body: JSON.stringify({
                    outFlightId: outFlightId.replace("Flight ", ""),
                    roundTrip: round_trip
                })
            }).then(r => {
                console.log(r.url);
                location.replace(r.url);
            });
        } else {
            fetch("/select_flights", {
                method: "POST",
                body: JSON.stringify({})
            }).then(r => {
                console.log(r.url);
                window.location.reload();
            });
        }

    } else {
        fetch("/select_flights", {
            method: "POST",
            body: JSON.stringify({})
        }).then(r => {
            console.log(r.url);
            window.location.reload();
        });
    }
}

function cancelBooking(bookingId) {
    fetch('/cancel_booking', {
        method: "POST",
        body: JSON.stringify({bookingId: bookingId})
    }).then(() => window.location.reload())
}