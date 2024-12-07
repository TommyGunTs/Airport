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

# Global containers for storing all airport and flight data
all_airports = []  # List to store Airport objects
all_flights = {}   # Dictionary mapping airport codes to lists of departing flights

def load_data(airport_file, flight_file):
    """
    Load and parse airport and flight data from text files.
    Args:
        airport_file (str): Name of airports data file
        flight_file (str): Name of flights data file
    Returns:
        bool: True if loading successful, False if any errors occur
    """
    try:
        # Process airports file
        with open(airport_file, 'r') as file:
            for line in file:
                # Split line and clean whitespace
                airport_code, country, city = [x.strip() for x in line.split('-')]
                new_airport = Airport(airport_code, city, country)
                all_airports.append(new_airport)

        # Process flights file
        with open(flight_file, 'r') as file:
            for line in file:
                # Split line and clean whitespace
                flight_code, origin_code, dest_code, flight_duration = [x.strip() for x in line.split('-')]
                
                # Get airport objects for origin and destination
                origin_airport = get_airport_by_code(origin_code)
                dest_airport = get_airport_by_code(dest_code)
                
                # Create new flight object
                new_flight = Flight(flight_code, origin_airport, dest_airport, flight_duration)
                
                # Store flight in dictionary under origin airport code
                if origin_code not in all_flights:
                    all_flights[origin_code] = []
                all_flights[origin_code].append(new_flight)
                
        return True
    except Exception:
        return False

def get_airport_by_code(code):
    """
    Find airport object by its code.
    Args:
        code (str): 3-letter airport code
    Returns:
        Airport: Matching airport object
    Raises:
        ValueError: If no airport found with given code
    """
    for airport in all_airports:
        if airport.get_code() == code:
            return airport
    raise ValueError(f"No airport with the given code: {code}")

def find_all_city_flights(city):
    """
    Find all flights involving a specific city.
    Args:
        city (str): City name to search for
    Returns:
        list: List of Flight objects involving the city
    """
    matching_flights = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city() == city or 
                flight.get_destination().get_city() == city):
                matching_flights.append(flight)
    return matching_flights

def find_all_country_flights(country):
    """
    Find all flights involving a specific country.
    Args:
        country (str): Country name to search for
    Returns:
        list: List of Flight objects involving the country
    """
    matching_flights = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country() == country or 
                flight.get_destination().get_country() == country):
                matching_flights.append(flight)
    return matching_flights

def find_flight_between(orig_airport, dest_airport):
    """
    Find direct or connecting flights between two airports.
    Args:
        orig_airport (Airport): Departure airport
        dest_airport (Airport): Arrival airport
    Returns:
        str: Message for direct flight
        set: Set of connecting airport codes
    Raises:
        ValueError: If no valid route found
    """
    # Check for direct flights
    if orig_airport.get_code() in all_flights:
        for flight in all_flights[orig_airport.get_code()]:
            if flight.get_destination() == dest_airport:
                return f"Direct Flight: {orig_airport.get_code()} to {dest_airport.get_code()}"
    
    # Check for connecting flights
    connecting_airports = set()
    if orig_airport.get_code() in all_flights:
        for first_flight in all_flights[orig_airport.get_code()]:
            connecting_code = first_flight.get_destination().get_code()
            if connecting_code in all_flights:
                for second_flight in all_flights[connecting_code]:
                    if second_flight.get_destination() == dest_airport:
                        connecting_airports.add(connecting_code)
    
    if connecting_airports:
        return connecting_airports
        
    raise ValueError(f"There are no direct or single-hop connecting flights from {orig_airport.get_code()} to {dest_airport.get_code()}")

def shortest_flight_from(orig_airport):
    """
    Find shortest flight from given airport.
    Args:
        orig_airport (Airport): Departure airport
    Returns:
        Flight: Flight object with shortest duration, or None if no flights
    """
    if orig_airport.get_code() not in all_flights:
        return None
    return min(all_flights[orig_airport.get_code()], key=lambda x: x.get_duration())

def find_return_flight(first_flight):
    """
    Find return flight for given flight.
    Args:
        first_flight (Flight): Original flight to find return for
    Returns:
        Flight: Matching return flight
    Raises:
        ValueError: If no return flight exists
    """
    dest_code = first_flight.get_destination().get_code()
    if dest_code not in all_flights:
        raise ValueError(f"There is no flight from {dest_code} to {first_flight.get_origin().get_code()}")
    
    for flight in all_flights[dest_code]:
        if flight.get_destination() == first_flight.get_origin():
            return flight
            
    raise ValueError(f"There is no flight from {dest_code} to {first_flight.get_origin().get_code()}")

if __name__ == "__main__":
    # Test code can be added here
    pass
