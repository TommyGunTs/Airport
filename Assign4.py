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
from typing import List, Dict, Set, Optional, Union

# Global containers
all_airports: List[Airport] = []
all_flights: Dict[str, List[Flight]] = {}

def load_data(airport_file: str, flight_file: str) -> bool:
    """Load and parse airport and flight data from text files."""
    all_airports.clear()
    all_flights.clear()
    
    try:
        if not airport_file or not flight_file:
            raise ValueError("File paths cannot be empty")
            
        # Process airports file
        with open(airport_file, 'r') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    parts = [x.strip() for x in line.split('-')]
                    if len(parts) != 3:
                        raise ValueError(f"Invalid format at line {line_num}")
                    
                    airport_code, country, city = parts
                    new_airport = Airport(airport_code, city, country)
                    all_airports.append(new_airport)
                except ValueError as e:
                    print(f"Error in airport file, line {line_num}: {e}")
                    return False

        # Process flights file
        with open(flight_file, 'r') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    parts = [x.strip() for x in line.split('-')]
                    if len(parts) != 4:
                        raise ValueError(f"Invalid format at line {line_num}")
                    
                    flight_code, origin_code, dest_code, flight_duration = parts
                    origin_airport = get_airport_by_code(origin_code)
                    dest_airport = get_airport_by_code(dest_code)
                    
                    new_flight = Flight(flight_code, origin_airport, dest_airport, flight_duration)
                    
                    if origin_code not in all_flights:
                        all_flights[origin_code] = []
                    all_flights[origin_code].append(new_flight)
                except ValueError as e:
                    print(f"Error in flight file, line {line_num}: {e}")
                    return False
                    
        return True
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def get_airport_by_code(code: str) -> Airport:
    """Find airport object by its code."""
    if not isinstance(code, str) or len(code.strip()) != 3:
        raise ValueError("Invalid airport code format")
        
    for airport in all_airports:
        if airport.get_code() == code.upper():
            return airport
    raise ValueError(f"No airport found with code: {code}")

def find_all_city_flights(city: str) -> List[Flight]:
    """Find all flights involving a specific city."""
    if not city or not isinstance(city, str):
        raise ValueError("Invalid city name")
        
    matching_flights = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_city() == city or 
                flight.get_destination().get_city() == city):
                matching_flights.append(flight)
    return matching_flights

def find_all_country_flights(country: str) -> List[Flight]:
    """Find all flights involving a specific country."""
    if not country or not isinstance(country, str):
        raise ValueError("Invalid country name")
        
    matching_flights = []
    for flights in all_flights.values():
        for flight in flights:
            if (flight.get_origin().get_country() == country or 
                flight.get_destination().get_country() == country):
                matching_flights.append(flight)
    return matching_flights

def find_flight_between(orig_airport: Airport, dest_airport: Airport) -> Union[str, Set[str]]:
    """Find direct or connecting flights between two airports."""
    if not isinstance(orig_airport, Airport) or not isinstance(dest_airport, Airport):
        raise TypeError("Both arguments must be Airport objects")
        
    if orig_airport == dest_airport:
        raise ValueError("Origin and destination cannot be the same")

    # Check direct flights
    if orig_airport.get_code() in all_flights:
        for flight in all_flights[orig_airport.get_code()]:
            if flight.get_destination() == dest_airport:
                return f"Direct Flight: {orig_airport.get_code()} to {dest_airport.get_code()}"
    
    # Check connecting flights
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
        
    raise ValueError(f"No flights found from {orig_airport.get_code()} to {dest_airport.get_code()}")

def shortest_flight_from(orig_airport: Airport) -> Optional[Flight]:
    """Find shortest flight from given airport."""
    if not isinstance(orig_airport, Airport):
        raise TypeError("Argument must be an Airport object")
        
    if orig_airport.get_code() not in all_flights:
        return None
    return min(all_flights[orig_airport.get_code()], key=lambda x: x.get_duration())

def find_return_flight(first_flight: Flight) -> Flight:
    """Find return flight for given flight."""
    if not isinstance(first_flight, Flight):
        raise TypeError("Argument must be a Flight object")
        
    dest_code = first_flight.get_destination().get_code()
    if dest_code not in all_flights:
        raise ValueError(f"No flights from {dest_code}")
    
    for flight in all_flights[dest_code]:
        if flight.get_destination() == first_flight.get_origin():
            return flight
            
    raise ValueError(f"No return flight found to {first_flight.get_origin().get_code()}")

if __name__ == "__main__":
    pass
