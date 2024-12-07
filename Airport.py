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
    """Airport class representing an airport with code, city, and country."""
    
    def __init__(self, code, city, country):
        """Initialize Airport with code, city, and country."""
        self._code = code.strip()
        self._city = city.strip()
        self._country = country.strip()

    def __str__(self):
        """Return string representation: code (city, country)"""
        return f"{self._code} ({self._city}, {self._country})"

    def __eq__(self, other):
        """Compare airports based on code."""
        if not isinstance(other, Airport):
            return False
        return self._code == other._code

    def get_code(self):
        """Return airport code."""
        return self._code

    def get_city(self):
        """Return airport city."""
        return self._city

    def get_country(self):
        """Return airport country."""
        return self._country

    def set_city(self, city):
        """Set airport city."""
        self._city = city.strip()

    def set_country(self, country):
        """Set airport country."""
        self._country = country.strip()
