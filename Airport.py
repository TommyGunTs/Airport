"""
*************************************
CS 1026A - Assignment 4 - Air Travel
Code by: Thomas Tyndorf
Student ID: ttyndor3
File created: November 26th, 2024
*************************************
This file implements an Airport class that manages individual airport data within the air travel system. 
It handles the storage and retrieval of essential airport information including the three-letter airport code, 
city name, and country. The class provides methods to compare airports, access their properties, 
and display airport information in a formatted string. This file serves as a fundamental building block for the
entire system, as airports are the key locations between which flights operate.
"""

class Airport:
    """Class representing an airport with code, city, and country information"""
    
    def __init__(self, code, city, country):
        """Initialize airport with code and location"""
        self._code = code
        self._city = city
        self._country = country

    def __str__(self):
        """Return formatted airport string"""
        return f"{self._code} ({self._city}, {self._country})"

    def __eq__(self, other):
        """Compare airports based on code"""
        if not isinstance(other, Airport):
            return False
        return self._code == other._code

    def get_code(self):
        return self._code

    def get_city(self):
        return self._city

    def get_country(self):
        return self._country

    def set_city(self, city):
        self._city = city

    def set_country(self, country):
        self._country = country
