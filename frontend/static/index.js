function selectFlight(current_flight, list_of_flights) {
    for (let child of list_of_flights.children) {
        if (child.className.includes("active")) {
            child.className = "list-group-item list-group-item-action";
        }
    }
    current_flight.className = "list-group-item list-group-item-action active"
}

function bookFlights(outbound_flights, inbound_flights) {
    let selOutFlight = undefined;
    let selInFlight = undefined;
    for (let child of outbound_flights.children) {
        if (child.className.includes("active")) {
            selOutFlight = child;
        }
    }
    for (let child of inbound_flights.children) {
        if (child.className.includes("active")) {
            selInFlight = child;
        }
    }
    if ((selOutFlight !== undefined) && (selInFlight !== undefined)) {
        let outFlightId = selOutFlight.querySelector('.card-title').innerText;
        let inFlightId = selInFlight.querySelector('.card-title').innerText;
        if ((outFlightId !== undefined) && (inFlightId !== undefined)) {
            fetch("/select_flights", {
                method: "POST",
                body: JSON.stringify({
                    outFlightId: outFlightId.replace("Flight ", ""),
                    inFlightId: inFlightId.replace("Flight ", "")
                })
            }).then(r => {
                console.log(r.url);
                location.replace(r.url);
            });
        }
    }
}