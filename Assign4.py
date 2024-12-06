"""
*************************************
CS 1026A - Assignment 4 - Air Travel
Code by: Thomas Tyndorf
Student ID: ttyndor3
File created: November 26th, 2024
*************************************
This file serves as the main program controller for the entire air travel system. 
It must read and parse airport and flight information from text files, storing them 
in appropriate data structures for efficient access. The program provides comprehensive 
search functionality including finding flights by city or country, locating direct and 
connecting flights between airports, identifying the shortest flights from specific airports, 
and finding return flight options. All results are validated and error-checked, with appropriate 
error messages provided when operations cannot be completed. This file acts as the central hub, 
utilizing both the Airport and Flight classes to create a complete flight management system.
"""

from Flight import *
from Airport import *

# Global data structures
all_airports = []
all_flights = {}

def load_data(airport_file, flight_file):
    """Load airport and flight data from files"""
    try:
        # Clear existing data
        all_airports.clear()
        all_flights.clear()

        # Load airports
        with open(airport_file, 'r') as f:
            for line in f:
                if line.strip():
                    code, country, city = [x.strip() for x in line.split('-')]
                    all_airports.append(Airport(code, city, country))

        # Load flights
        with open(flight_file, 'r') as f:
            for line in f:
                if line.strip():
                    flight_no, orig_code, dest_code, duration = [x.strip() for x in line.split('-')]
                    try:
                        origin = get_airport_by_code(orig_code)
                        dest = get_airport_by_code(dest_code)
                        flight = Flight(flight_no, origin, dest, duration)
                        
                        if orig_code not in all_flights:
                            all_flights[orig_code] = []
                        all_flights[orig_code].append(flight)
                    except ValueError:
                        continue
        return True
    except:
        return False

def get_airport_by_code(code):
    """Find airport by code"""
    for airport in all_airports:
        if airport.get_code() == code:
            return airport
    raise ValueError(f"No airport with code: {code}")

def find_all_city_flights(city):
    """Find all flights involving city"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city() == city or 
                flight.get_destination().get_city() == city):
                matches.append(flight)
    return matches

def find_all_country_flights(country):
    """Find all flights involving country"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country() == country or 
                flight.get_destination().get_country() == country):
                matches.append(flight)
    return matches

def find_flight_between(orig_airport, dest_airport):
    """Find direct or connecting flights"""
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    # Check direct flights
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination().get_code() == dest_code:
                return f"Direct Flight: {orig_code} to {dest_code}"

    # Check connecting flights
    connecting = set()
    if orig_code in all_flights:
        for first_flight in all_flights[orig_code]:
            mid_code = first_flight.get_destination().get_code()
            if mid_code in all_flights:
                for second_flight in all_flights[mid_code]:
                    if second_flight.get_destination().get_code() == dest_code:
                        connecting.add(mid_code)

    if connecting:
        return connecting

    raise ValueError(f"No flights from {orig_code} to {dest_code}")

def shortest_flight_from(orig_airport):
    """Find shortest flight from airport"""
    orig_code = orig_airport.get_code()
    if orig_code not in all_flights or not all_flights[orig_code]:
        return None
    return min(all_flights[orig_code], key=lambda x: x.get_duration())

def find_return_flight(first_flight):
    """Find return flight"""
    dest_code = first_flight.get_destination().get_code()
    orig_code = first_flight.get_origin().get_code()

    if dest_code not in all_flights:
        raise ValueError(f"No flights from {dest_code} to {orig_code}")

    for flight in all_flights[dest_code]:
        if flight.get_destination().get_code() == orig_code:
            return flight

    raise ValueError(f"No flights from {dest_code} to {orig_code}")

if __name__ == "__main__":
    pass
