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

# Global containers
all_airports = []  # List of Airport objects
all_flights = {}   # Dictionary: airport_code -> list of flights

def load_data(airport_file, flight_file):
    """Load airport and flight data from files."""
    all_airports.clear()
    all_flights.clear()
    
    try:
        # Load airports
        with open(airport_file, 'r') as file:
            for line in file:
                if line.strip():
                    code, country, city = [x.strip() for x in line.split('-')]
                    all_airports.append(Airport(code, city, country))

        # Load flights
        with open(flight_file, 'r') as file:
            for line in file:
                if line.strip():
                    flight_no, origin, dest, duration = [x.strip() for x in line.split('-')]
                    origin_airport = get_airport_by_code(origin)
                    dest_airport = get_airport_by_code(dest)
                    
                    flight = Flight(flight_no, origin_airport, dest_airport, duration)
                    
                    if origin not in all_flights:
                        all_flights[origin] = []
                    all_flights[origin].append(flight)
        return True
    except:
        return False
def get_airport_by_code(code):
    """Find airport by code."""
    for airport in all_airports:
        if airport.get_code() == code:
            return airport
    raise ValueError(f"No airport with the given code: {code}")

def improved_find_all_city_flights(city):
    """Find all flights involving the given city (case-insensitive)."""
    city = city.strip().lower()
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city().lower() == city or 
                flight.get_destination().get_city().lower() == city):
                result.append(flight)
    return result

def improved_find_all_country_flights(country):
    """Find all flights involving the given country (case-insensitive)."""
    country = country.strip().lower()
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country().lower() == country or 
                flight.get_destination().get_country().lower() == country):
                result.append(flight)
    return result

def improved_find_flight_between(orig_airport, dest_airport):
    """Find direct or connecting flights between two airports."""
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    # Check for direct flights
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination() == dest_airport:
                return f"Direct Flight: {orig_code} to {dest_code}"
    
    # Check connecting flights
    connecting_flights = []
    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            connecting_code = flight.get_destination().get_code()
            if connecting_code in all_flights:
                for second_flight in all_flights[connecting_code]:
                    if second_flight.get_destination() == dest_airport:
                        connecting_flights.append((flight, second_flight))
    
    if connecting_flights:
        return connecting_flights  # Return list of connecting flights

    raise ValueError(f"No direct or single-hop connecting flights from {orig_code} to {dest_code}")
def improved_find_return_flight(first_flight):
    """Find a return flight for the given flight."""
    dest_code = first_flight.get_destination().get_code()
    origin_code = first_flight.get_origin().get_code()

    if dest_code in all_flights:
        for flight in all_flights[dest_code]:
            if flight.get_destination().get_code() == origin_code:
                return flight

    raise ValueError(f"No return flight from {dest_code} to {origin_code}")


def improved_shortest_flight_from(orig_airport):
    """Find the shortest flight originating from the given airport."""
    orig_code = orig_airport.get_code()

    if orig_code not in all_flights or not all_flights[orig_code]:
        return None  # No flights found

    # Find the flight with the minimum duration
    return min(all_flights[orig_code], key=lambda flight: flight.get_duration())


if __name__ == "__main__":
    pass
