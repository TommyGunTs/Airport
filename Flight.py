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
    """Class representing a flight between airports"""
    
    def __init__(self, flight_no, origin, dest, dur):
        """Initialize flight with number, airports and duration"""
        if not isinstance(origin, Airport) or not isinstance(dest, Airport):
            raise TypeError("The origin and destination must be Airport objects")
        self._flight_no = flight_no
        self._origin = origin
        self._destination = dest
        self._duration = float(dur)

    def __str__(self):
        """Return formatted flight string"""
        flight_type = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({int(round(self._duration))}h) [{flight_type}]"

    def __eq__(self, other):
        """Compare flights based on airports"""
        if not isinstance(other, Flight):
            return False
        return self._origin == other._origin and self._destination == other._destination

    def __add__(self, conn_flight):
        """Combine two flights for connections"""
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
        if self._destination != conn_flight._origin:
            raise ValueError("These flights cannot be combined")
        return Flight(self._flight_no, self._origin, conn_flight._destination, 
                     self._duration + conn_flight._duration)

    def get_flight_no(self):
        return self._flight_no

    def get_origin(self):
        return self._origin

    def get_destination(self):
        return self._destination

    def get_duration(self):
        return self._duration

    def is_domestic(self):
        return self._origin.get_country() == self._destination.get_country()
