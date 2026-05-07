import requests
import os
from dotenv import load_dotenv

load_dotenv() #Load .env file

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") #Read API Key and save it.

ROUTES = [
    {"origin": "MAD", "destination": "BCN", "target_price": 900},
    {"origin": "LON", "destination": "PAR", "target_price": 800},
    {"origin": "FRA", "destination": "ROM", "target_price": 850}
]

def print_round_trip_summary(flight):
    print("----- ITINERARY DETAILS -----")

    price = flight.get("price", {}).get("amount")
    print("PRICE:", price)

    print("OUTBOUND:")
    print_segments(flight.get("outbound", {}).get("sectorSegments", []))

    print("INBOUND:")
    print_segments(flight.get("inbound", {}).get("sectorSegments", []))


def print_segments(segments):
    for index, segment_wrapper in enumerate(segments):
        segment = segment_wrapper.get("segment", {})

        source = segment.get("source", {})
        destination = segment.get("destination", {})

        source_station = source.get("station", {})
        destination_station = destination.get("station", {})

        print(f"  Segment {index + 1}:")
        print("  From:", source_station.get("name"), source_station.get("code"))
        print("  To:", destination_station.get("name"), destination_station.get("code"))
        print("  Departure:", source.get("localTime"))
        print("  Arrival:", destination.get("localTime"))


def get_first_airport_code(flight, direction):
    segments = flight.get(direction, {}).get("sectorSegments", [])
    if len(segments) == 0:
        return None
    first_segment = segments[0].get("segment", {})
    return first_segment.get("source", {}).get("station", {}).get("code")


def get_last_airport_code(flight, direction):
    segments = flight.get(direction, {}).get("sectorSegments", [])
    if len(segments) == 0:
        return None
    last_segment = segments[-1].get("segment", {})
    return last_segment.get("destination", {}).get("station", {}).get("code")


def flight_matches_search(flight, origin, destination):
    outbound_origin = get_first_airport_code(flight, "outbound")
    outbound_destination = get_last_airport_code(flight, "outbound")

    inbound_origin = get_first_airport_code(flight, "inbound")
    inbound_destination = get_last_airport_code(flight, "inbound")

    return (
        outbound_origin == origin #otbound flight origin
        and outbound_destination == destination #outbound flight destination
        and inbound_origin == destination #inbound flight origin
        and inbound_destination == origin #inbound flight destination
    )



def get_real_price(origin, destination):
    url = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"

    querystring = {
        "source": origin,
        "destination": destination,
        "outboundDepartmentDateStart": "2026-06-01T00:00:00",
        "outboundDepartmentDateEnd": "2026-07-31T23:59:59",
        "inboundDepartureDateStart": "2026-06-25T00:00:00",
        "inboundDepartureDateEnd": "2026-09-30T23:59:59",
        "currency": "usd",
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "kiwi-com-cheap-flights.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    print('STATUS: ', response.status_code)
    data = response.json()
    #import json
    #with open('respuesta_api.json', 'w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=2, ensure_ascii=False)
    try:
        itineraries = data["itineraries"]
        if len(itineraries) == 0:
            print("API responded, but no flights found for this route/date.")
            return None
        cheapest_flight = None
        cheapest_price = None

        for flight in itineraries:
            if flight_matches_search(flight, origin, destination):
                amount = flight.get("price", {}).get("amount")

                if amount is None:
                    continue
                
                price = float(amount)

                if cheapest_price is None or price < cheapest_price:
                    cheapest_price = price
                    cheapest_flight = flight

        if cheapest_flight is None:
            print(f"API returned flights but none match {origin} → {destination}.")
            return None

        print_round_trip_summary(cheapest_flight)
        return cheapest_price
    
    except Exception as error:
        print('ERROR READING PRICE: ', error)
        return None

def check_route(route):
    origin = route["origin"]
    destination = route["destination"]
    target_price = route["target_price"]

    price = get_real_price(origin, destination)

    if price is None:
        print(f"{origin} → {destination}: no flights found")
        return

    print(f"{origin} → {destination}: {price} €")

    if price <= target_price:
        print(f"🔥 ALERT: cheap flight: {origin} → {destination} for {price} €")

def main():
    print("Real flight search started")

    for route in ROUTES:
        check_route(route)


if __name__ == "__main__":  #"Execute main() only if this is run directly"
    main()

