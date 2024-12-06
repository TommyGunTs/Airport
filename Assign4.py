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
    try:
        all_airports.clear()
        all_flights.clear()
        
        with open(airport_file, 'r') as f:
            for line in f:
                if not line.strip(): continue
                parts = line.strip().split('-')
                if len(parts) != 3: continue
                code, country, city = [p.strip() for p in parts]
                all_airports.append(Airport(code, city, country))

        with open(flight_file, 'r') as f:
            for line in f:
                if not line.strip(): continue
                parts = line.strip().split('-')
                if len(parts) != 4: continue
                flight_no, orig_code, dest_code, duration = [p.strip() for p in parts]
                try:
                    origin = get_airport_by_code(orig_code)
                    dest = get_airport_by_code(dest_code)
                    flight = Flight(flight_no, origin, dest, float(duration))
                    
                    if orig_code not in all_flights:
                        all_flights[orig_code] = []
                    all_flights[orig_code].append(flight)
                except (ValueError, TypeError):
                    continue
        return True
    except Exception:
        return False

def get_airport_by_code(code):
    for airport in all_airports:
        if airport.get_code().upper() == code.upper():
            return airport
    raise ValueError(f"No airport with code: {code}")

def find_all_city_flights(city):
    matches = []
    city = city.lower()
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city().lower() == city or 
                flight.get_destination().get_city().lower() == city):
                matches.append(flight)
    return sorted(matches, key=lambda x: x.get_duration())

def find_all_country_flights(country):
    matches = []
    country = country.lower()
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country().lower() == country or 
                flight.get_destination().get_country().lower() == country):
                matches.append(flight)
    return sorted(matches, key=lambda x: x.get_duration())

def find_flight_between(orig_airport, dest_airport):
    orig_code = orig_airport.get_code()
    dest_code = dest_airport.get_code()

    if orig_code in all_flights:
        for flight in all_flights[orig_code]:
            if flight.get_destination().get_code() == dest_code:
                return f"Direct Flight: {orig_code} to {dest_code}"

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
    orig_code = orig_airport.get_code()
    if orig_code not in all_flights or not all_flights[orig_code]:
        return None
    return min(all_flights[orig_code], key=lambda x: float(x.get_duration()))

def find_return_flight(first_flight):
    dest_code = first_flight.get_destination().get_code()
    orig_code = first_flight.get_origin().get_code()
    
    if dest_code not in all_flights:
        raise ValueError(f"There is no flight from {dest_code} to {orig_code}")
        
    for flight in all_flights[dest_code]:
        if flight.get_destination().get_code() == orig_code:
            return flight
            
    raise ValueError(f"There is no flight from {dest_code} to {orig_code}")

if __name__ == "__main__":
    pass
