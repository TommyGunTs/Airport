from Airport import *

class Flight:
    """
    A class representing a flight between two airports.
    Attributes:
        _flight_no (str): Unique flight identifier (ABC-123 format)
        _origin (Airport): Departure airport object
        _destination (Airport): Arrival airport object
        _duration (float): Flight duration in hours
    """

    def __init__(self, flight_no, origin, dest, dur):
        """
        Initialize a new Flight object.
        Args:
            flight_no (str): Flight identifier
            origin (Airport): Departure airport
            dest (Airport): Destination airport
            dur (float): Flight duration in hours
        Raises:
            TypeError: If origin or destination aren't Airport objects
        """
        if not isinstance(origin, Airport) or not isinstance(dest, Airport):
            raise TypeError("The origin and destination must be Airport objects")
        self._flight_no = flight_no
        self._origin = origin
        self._destination = dest
        self._duration = float(dur)

    def __str__(self):
        """
        Returns string representation of flight.
        Returns:
            str: Formatted string with cities, duration, and flight type
        """
        flight_type = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({int(round(self._duration))}h) [{flight_type}]"

    def __eq__(self, other):
        """
        Compare two flights for equality based on origin and destination.
        Args:
            other: Another flight object to compare with
        Returns:
            bool: True if flights have same origin and destination
        """
        if not isinstance(other, Flight):
            return False
        return self._origin == other._origin and self._destination == other._destination

    def __add__(self, conn_flight):
        """
        Combine two flights into a single connecting flight.
        Args:
            conn_flight (Flight): The connecting flight
        Returns:
            Flight: New combined flight object
        Raises:
            TypeError: If conn_flight isn't a Flight object
            ValueError: If flights can't be connected
        """
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
        if self._destination != conn_flight._origin:
            raise ValueError("These flights cannot be combined")
        return Flight(self._flight_no, self._origin, conn_flight._destination, 
                     self._duration + conn_flight._duration)

    def get_flight_no(self):
        """Return flight number."""
        return self._flight_no

    def get_origin(self):
        """Return departure airport."""
        return self._origin

    def get_destination(self):
        """Return arrival airport."""
        return self._destination

    def get_duration(self):
        """Return flight duration in hours."""
        return self._duration

    def is_domestic(self):
        """
        Check if flight is within same country.
        Returns:
            bool: True if domestic flight, False if international
        """
        return self._origin.get_country() == self._destination.get_country()

    def set_origin(self, origin):
        """Update departure airport."""
        self._origin = origin

    def set_destination(self, destination):
        """Update arrival airport."""
        self._destination = destination
