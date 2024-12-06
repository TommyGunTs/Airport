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
    def __init__(self, flight_no, origin, dest, dur):
        # Strict type checking
        if not isinstance(origin, Airport) or not isinstance(dest, Airport):
            raise TypeError("Origin and destination must be Airport objects")
        if not isinstance(dur, (int, float)) and not isinstance(dur, str):
            raise TypeError("Duration must be numeric or string convertible to float")
            
        self._flight_no = str(flight_no)
        self._origin = origin
        self._destination = dest
        # Ensure duration is float
        try:
            self._duration = float(dur)
        except ValueError:
            raise ValueError("Invalid duration format")

    def __str__(self):
        flight_type = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({int(round(self._duration))}h) [{flight_type}]"

    def __eq__(self, other):
        if not isinstance(other, Flight):
            return False
        return (self._origin.get_code() == other._origin.get_code() and 
                self._destination.get_code() == other._destination.get_code())

    def __add__(self, other):
        # Strict validation for flight combination
        if not isinstance(other, Flight):
            raise TypeError("Can only combine with another Flight object")
        if self._destination.get_code() != other._origin.get_code():
            raise ValueError("Flights cannot be combined - destination and origin don't match")
        return Flight(
            self._flight_no,
            self._origin,
            other._destination,
            self._duration + other._duration
        )

    # Getters
    def get_flight_no(self): return self._flight_no
    def get_origin(self): return self._origin
    def get_destination(self): return self._destination
    def get_duration(self): return self._duration
    
    def is_domestic(self):
        return self._origin.get_country().lower() == self._destination.get_country().lower()
