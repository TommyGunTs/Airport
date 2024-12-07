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
all_airports = []
all_flights = {}

def load_data(airport_file, flight_file):
    all_airports.clear()
    all_flights.clear()
    
    try:
        # Process airports
        with open(airport_file, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    code, country, city = [x.strip() for x in line.split('-')]
                    all_airports.append(Airport(code, city, country))

        # Process flights
        with open(flight_file, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
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
    for airport in all_airports:
        if airport.get_code() == code:
            return airport
    raise ValueError(f"No airport found with code: {code}")

def find_all_city_flights(city):
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city().lower() == city.lower() or 
                flight.get_destination().get_city().lower() == city.lower()):
                result.append(flight)
    return result

def find_all_country_flights(country):
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country().lower() == country.lower() or 
                flight.get_destination().get_country().lower() == country.lower()):
                result.append(flight)
    return result

def find_flight_between(orig_airport, dest_airport):
    # Check direct flights
    if orig_airport.get_code() in all_flights:
        for flight in all_flights[orig_airport.get_code()]:
            if flight.get_destination() == dest_airport:
                return f"Direct Flight: {orig_airport.get_code()} to {dest_airport.get_code()}"
    
    # Check connecting flights
    connecting = set()
    if orig_airport.get_code() in all_flights:
        for first_flight in all_flights[orig_airport.get_code()]:
            connecting_code = first_flight.get_destination().get_code()
            if connecting_code in all_flights:
                for second_flight in all_flights[connecting_code]:
                    if second_flight.get_destination() == dest_airport:
                        connecting.add(connecting_code)
    
    if connecting:
        return connecting
    raise ValueError("No valid route found")

def shortest_flight_from(orig_airport):
    if orig_airport.get_code() not in all_flights:
        return None
    return min(all_flights[orig_airport.get_code()], 
              key=lambda x: float(x.get_duration()))

def find_return_flight(first_flight):
    dest_code = first_flight.get_destination().get_code()
    if dest_code not in all_flights:
        raise ValueError("No return flights available")
    
    for flight in all_flights[dest_code]:
        if flight.get_destination() == first_flight.get_origin():
            return flight
    raise ValueError("No return flights available")

if __name__ == "__main__":
    pass
