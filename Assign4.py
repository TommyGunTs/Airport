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

all_airports = []
all_flights = {}

def load_data(airport_file, flight_file):
    """Load and validate airport and flight data"""
    try:
        # Clear existing data
        all_airports.clear()
        all_flights.clear()

        # Load airports with validation
        with open(airport_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    code, country, city = [x.strip() for x in line.split('-')]
                    airport = Airport(code, city, country)
                    all_airports.append(airport)
                except:
                    continue

        # Load flights with validation
        with open(flight_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    flight_no, orig_code, dest_code, duration = [x.strip() for x in line.split('-')]
                    origin = get_airport_by_code(orig_code)
                    dest = get_airport_by_code(dest_code)
                    
                    # Create flight and store by origin
                    flight = Flight(flight_no, origin, dest, float(duration))
                    if orig_code not in all_flights:
                        all_flights[orig_code] = []
                    all_flights[orig_code].append(flight)
                except:
                    continue
        
        return bool(all_airports and all_flights)
    except:
        return False

def get_airport_by_code(code):
    """Find airport by code (case insensitive)"""
    code = code.upper()
    for airport in all_airports:
        if airport.get_code().upper() == code:
            return airport
    raise ValueError(f"No airport found with code: {code}")

def find_all_city_flights(city):
    """Find all flights involving a city"""
    result = []
    city = city.lower()
    for flights in all_flights.values():
        for flight in flights:
            orig_city = flight.get_origin().get_city().lower()
            dest_city = flight.get_destination().get_city().lower()
            if city in (orig_city, dest_city):
                result.append(flight)
    return sorted(result, key=lambda x: x.get_duration())

def find_all_country_flights(country):
    """Find all flights involving a country"""
    result = []
    country = country.lower()
    for flights in all_flights.values():
        for flight in flights:
            orig_country = flight.get_origin().get_country().lower()
            dest_country = flight.get_destination().get_country().lower()
            if country in (orig_country, dest_country):
                result.append(flight)
    return sorted(result, key=lambda x: x.get_duration())

def find_flight_between(orig_airport, dest_airport):
    """Find direct or connecting flights between airports"""
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    # Check direct flights
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination().get_code() == dest_code:
                return f"Direct Flight: {orig_code} to {dest_code}"

    # Check connecting flights
    connections = set()
    if orig_code in all_flights:
        for first_flight in all_flights[orig_code]:
            mid_code = first_flight.get_destination().get_code()
            if mid_code in all_flights:
                for second_flight in all_flights[mid_code]:
                    if second_flight.get_destination().get_code() == dest_code:
                        connections.add(mid_code)

    if connections:
        return connections

    raise ValueError(f"No flights available from {orig_code} to {dest_code}")

def shortest_flight_from(orig_airport):
    """Find shortest flight from given airport"""
    orig_code = orig_airport.get_code()
    if orig_code not in all_flights or not all_flights[orig_code]:
        return None
    return min(all_flights[orig_code], key=lambda x: float(x.get_duration()))

def find_return_flight(first_flight):
    """Find return flight for given flight"""
    orig_code = first_flight.get_origin().get_code()
    dest_code = first_flight.get_destination().get_code()
    
    if dest_code not in all_flights:
        raise ValueError(f"No return flights available from {dest_code} to {orig_code}")
        
    for flight in all_flights[dest_code]:
        if flight.get_destination().get_code() == orig_code:
            return flight
            
    raise ValueError(f"No return flights available from {dest_code} to {orig_code}")

if __name__ == "__main__":
    pass
