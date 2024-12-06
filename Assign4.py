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
    """Load and process airport and flight data from text files"""
    try:
        # Clear existing data before loading
        all_airports.clear()
        all_flights.clear()

        # Process airport file
        with open(airport_file, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    # Parse airport data and create Airport object
                    code, country, city = [x.strip() for x in line.split('-')]
                    all_airports.append(Airport(code, city, country))

        # Process flight file
        with open(flight_file, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    # Parse flight data
                    flight_no, orig_code, dest_code, duration = [x.strip() for x in line.split('-')]
                    try:
                        # Get airport objects and create Flight
                        origin = get_airport_by_code(orig_code)
                        destination = get_airport_by_code(dest_code)
                        new_flight = Flight(flight_no, origin, destination, float(duration))
                        
                        # Store flight in dictionary under origin airport
                        if orig_code not in all_flights:
                            all_flights[orig_code] = []
                        all_flights[orig_code].append(new_flight)
                    except ValueError:
                        continue  # Skip invalid flights
        return True
    except Exception:
        return False

def find_all_city_flights(city):
    """Find all flights involving specified city as origin or destination"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            # Case-insensitive city comparison
            if (flight.get_origin().get_city().lower() == city.lower() or 
                flight.get_destination().get_city().lower() == city.lower()):
                matches.append(flight)
    return matches

def find_all_country_flights(country):
    """Find all flights involving specified country as origin or destination"""
    matches = []
    for flights in all_flights.values():
        for flight in flights:
            # Case-insensitive country comparison
            if (flight.get_origin().get_country().lower() == country.lower() or 
                flight.get_destination().get_country().lower() == country.lower()):
                matches.append(flight)
    return matches

def find_flight_between(orig_airport, dest_airport):
    """Find direct or connecting flights between two airports"""
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    # Check for direct flights
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination().get_code() == dest_code:
                return f"Direct Flight: {orig_code} to {dest_code}"
    
    # Check for connecting flights
    connecting_airports = set()
    if orig_code in all_flights:
        for first_flight in all_flights[orig_code]:
            connecting_code = first_flight.get_destination().get_code()
            if connecting_code in all_flights:
                for second_flight in all_flights[connecting_code]:
                    if second_flight.get_destination().get_code() == dest_code:
                        connecting_airports.add(connecting_code)
    
    if connecting_airports:
        return connecting_airports
    
    raise ValueError(f"There are no direct or single-hop connecting flights from {orig_code} to {dest_code}")

def shortest_flight_from(orig_airport):
    """Find shortest duration flight from specified airport"""
    orig_code = orig_airport.get_code()
    if orig_code not in all_flights or not all_flights[orig_code]:
        return None
    return min(all_flights[orig_code], key=lambda x: x.get_duration())

def find_return_flight(first_flight):
    """Find return flight for given flight"""
    dest_code = first_flight.get_destination().get_code()
    orig_code = first_flight.get_origin().get_code()
    
    # Check if return flights exist from destination
    if dest_code not in all_flights:
        raise ValueError(f"There is no flight from {dest_code} to {orig_code}")
    
    # Search for matching return flight
    for flight in all_flights[dest_code]:
        if flight.get_destination().get_code() == orig_code:
            return flight
    
    raise ValueError(f"There is no flight from {dest_code} to {orig_code}")

if __name__ == "__main__":
    pass
