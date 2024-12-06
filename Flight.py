"""
*************************************
CS 1026A - Assignment 4 - Air Travel
Code by: Thomas Tyndorf
Student ID: ttyndor3
File created: November 26th, 2024
*************************************
This file implements a Flight class that manages individual flight connections between airports 
in the air travel system. It must handle flight information including flight numbers (in ABC-123 format), 
origin and destination airports, and flight durations. The class calculates whether flights are domestic 
or international based on country information, validates airport objects, and enables the combination of 
flights for connecting routes. The file depends on Airport.py as flights must operate between valid airport 
objects, and it includes comprehensive error checking for all operations.
"""

from Airport import *

class Flight:
    """Class to manage individual flights between airports with duration and route information"""

    def __init__(self, flight_no, origin, dest, dur):
        # Validate that both airports are valid Airport objects
        if not isinstance(origin, Airport) or not isinstance(dest, Airport):
            raise TypeError("The origin and destination must be Airport objects")
            
        # Initialize flight attributes
        self._flight_no = flight_no        # Unique flight identifier (ABC-123 format)
        self._origin = origin              # Departure airport object
        self._destination = dest           # Arrival airport object
        self._duration = float(dur)        # Flight duration in hours (as float)

    def __str__(self):
        # Create string representation with flight details and type
        flight_type = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({int(round(self._duration))}h) [{flight_type}]"

    def __eq__(self, other):
        # Compare flights based on origin and destination airports
        if not isinstance(other, Flight):
            return False
        return (self._origin.get_code() == other._origin.get_code() and 
                self._destination.get_code() == other._destination.get_code())

    def __add__(self, conn_flight):
        # Combine two flights for connecting routes
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
            
        # Verify flights can be connected (destination of first matches origin of second)
        if self._destination.get_code() != conn_flight._origin.get_code():
            raise ValueError("These flights cannot be combined")
            
        # Create new combined flight
        return Flight(
            self._flight_no,
            self._origin,
            conn_flight._destination,
            self._duration + conn_flight._duration
        )

    def get_flight_no(self):
        """Return flight number"""
        return self._flight_no

    def get_origin(self):
        """Return departure airport"""
        return self._origin

    def get_destination(self):
        """Return arrival airport"""
        return self._destination

    def get_duration(self):
        """Return flight duration"""
        return self._duration

    def is_domestic(self):
        """Check if flight is within same country"""
        return self._origin.get_country() == self._destination.get_country()

    def set_origin(self, origin):
        """Update departure airport"""
        self._origin = origin

    def set_destination(self, destination):
        """Update arrival airport"""
        self._destination = destination
