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

# Global containers for storing airport and flight data
all_airports = []          # List of all Airport objects
all_flights = {}           # Dictionary mapping airport codes to lists of departing flights

def load_data(airport_file, flight_file):
    """Load data from files"""
    try:
        all_airports.clear()
        all_flights.clear()
        
        # Step 1: Load airports first
        with open(airport_file, 'r') as f:
            for line in f:
                if line.strip():
                    code, country, city = [x.strip() for x in line.split('-')]
                    all_airports.append(Airport(code, city, country))

        # Step 2: Load flights
        with open(flight_file, 'r') as f:
            for line in f:
                if line.strip():
                    flight_no, orig_code, dest_code, duration = [x.strip() for x in line.split('-')]
                    origin = get_airport_by_code(orig_code)
                    dest = get_airport_by_code(dest_code)
                    flight = Flight(flight_no, origin, dest, float(duration))
                    
                    if orig_code not in all_flights:
                        all_flights[orig_code] = []
                    all_flights[orig_code].append(flight)
        return True
    except Exception as e:
        print(f"Error: {e}")  # For debugging
        return False

def get_airport_by_code(code):
    """Find airport by code"""
    for airport in all_airports:
        if airport.get_code().upper() == code.upper():  # Case-insensitive
            return airport
    raise ValueError(f"No airport with the given code: {code}")

def find_all_city_flights(city):
    """Find flights by city"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            origin_city = flight.get_origin().get_city().lower()
            dest_city = flight.get_destination().get_city().lower()
            if city.lower() in (origin_city, dest_city):
                matches.append(flight)
    return matches

def find_all_country_flights(country):
    """Find flights by country"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            origin_country = flight.get_origin().get_country().lower()
            dest_country = flight.get_destination().get_country().lower()
            if country.lower() in (origin_country, dest_country):
                matches.append(flight)
    return matches

def find_flight_between(orig_airport, dest_airport):
    """Find direct or connecting flights"""
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    # Direct flight check
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination().get_code() == dest_code:
                return f"Direct Flight: {orig_code} to {dest_code}"

    # Connecting flight check
    connecting = set()
    for first_leg in all_flights.get(orig_code, []):
        mid_code = first_leg.get_destination().get_code()
        for second_leg in all_flights.get(mid_code, []):
            if second_leg.get_destination().get_code() == dest_code:
                connecting.add(mid_code)

    if connecting:
        return connecting

    raise ValueError(f"There are no direct or single-hop connecting flights from {orig_code} to {dest_code}")

if __name__ == "__main__":
    pass
