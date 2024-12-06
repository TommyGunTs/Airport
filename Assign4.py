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

# Global collections
all_airports = []  # List to store Airport objects
all_flights = {}   # Dictionary mapping airport codes to list of departing flights

def load_data(airport_file, flight_file):
    """
    Load airport and flight data from files.
    Args:
        airport_file (str): Path to airport data file
        flight_file (str): Path to flight data file
    Returns:
        bool: True if loading successful, False otherwise
    """
    try:
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
                        flight = Flight(flight_no, origin, dest, float(duration))
                        
                        if orig_code not in all_flights:
                            all_flights[orig_code] = []
                        all_flights[orig_code].append(flight)
                    except ValueError:
                        continue
        return True
    except:
        return False

def get_airport_by_code(code):
    """
    Find airport by its code.
    Args:
        code (str): Airport code to search for
    Returns:
        Airport: Matching airport object
    Raises:
        ValueError: If no matching airport found
    """
    for airport in all_airports:
        if airport.get_code().upper() == code.upper():
            return airport
    raise ValueError(f"No airport found with code: {code}")

def find_all_city_flights(city):
    """
    Find all flights involving given city.
    Args:
        city (str): City name to search for
    Returns:
        list: List of Flight objects involving the city
    """
    result = []
    city = city.lower().strip()
    for flights in all_flights.values():
        for flight in flights:
            if (city == flight.get_origin().get_city().lower().strip() or 
                city == flight.get_destination().get_city().lower().strip()):
                result.append(flight)
    return result

def find_all_country_flights(country):
    """
    Find all flights involving given country.
    Args:
        country (str): Country name to search for
    Returns:
        list: List of Flight objects involving the country
    """
    result = []
    country = country.lower().strip()
    for flights in all_flights.values():
        for flight in flights:
            if (country == flight.get_origin().get_country().lower().strip() or 
                country == flight.get_destination().get_country().lower().strip()):
                result.append(flight)
    return result

def find_flight_between(orig_airport, dest_airport):
    """
    Find direct or connecting flights between airports.
    Args:
        orig_airport (Airport): Origin airport
        dest_airport (Airport): Destination airport
    Returns:
        str or set: Direct flight string or set of connecting airports
    Raises:
        ValueError: If no route found
    """
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
    """
    Find shortest duration flight from given airport.
    Args:
        orig_airport (Airport): Origin airport
    Returns:
        Flight or None: Shortest flight or None if no flights exist
    """
    code = orig_airport.get_code()
    if code not in all_flights or not all_flights[code]:
        return None
    return min(all_flights[code], key=lambda x: float(x.get_duration()))

def find_return_flight(first_flight):
    """
    Find return flight for given flight.
    Args:
        first_flight (Flight): Original flight to find return for
    Returns:
        Flight: Matching return flight
    Raises:
        ValueError: If no return flight found
    """
    dest_code = first_flight.get_destination().get_code()
    orig_code = first_flight.get_origin().get_code()
    
    if dest_code not in all_flights:
        raise ValueError(f"No return flights from {dest_code} to {orig_code}")
    
    for flight in all_flights[dest_code]:
        if flight.get_destination().get_code() == orig_code:
            return flight
    
    raise ValueError(f"No return flights from {dest_code} to {orig_code}")

if __name__ == "__main__":
    # Test code here
    pass
