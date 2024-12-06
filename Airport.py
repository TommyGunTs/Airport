class Airport:
    """
    A class representing an airport with its identifying code and location details.
    Attributes:
        _code (str): 3-letter airport identifier code
        _city (str): City where airport is located
        _country (str): Country where airport is located
    """
    
    def __init__(self, code, city, country):
        """
        Initialize a new Airport object.
        Args:
            code (str): 3-letter airport code
            city (str): City name
            country (str): Country name
        """
        self._code = code
        self._city = city
        self._country = country

    def __str__(self):
        """
        Returns string representation of airport.
        Returns:
            str: Formatted string with code, city, and country
        """
        return f"{self._code} ({self._city}, {self._country})"

    def __eq__(self, other):
        """
        Compare two airports for equality based on their codes.
        Args:
            other: Another airport object to compare with
        Returns:
            bool: True if airports have same code, False otherwise
        """
        if not isinstance(other, Airport):
            return False
        return self._code == other._code

    def get_code(self):
        """Return airport's 3-letter code."""
        return self._code

    def get_city(self):
        """Return airport's city location."""
        return self._city

    def get_country(self):
        """Return airport's country location."""
        return self._country

    def set_city(self, city):
        """
        Update airport's city.
        Args:
            city (str): New city name
        """
        self._city = city

    def set_country(self, country):
        """
        Update airport's country.
        Args:
            country (str): New country name
        """
        self._country = country
