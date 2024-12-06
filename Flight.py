from Airport import *

class Flight:
    def __init__(self, flight_no, origin, dest, dur):
        if not isinstance(origin, Airport) or not isinstance(dest, Airport):
            raise TypeError("The origin and destination must be Airport objects")
        self._flight_no = flight_no
        self._origin = origin
        self._destination = dest
        self._duration = float(dur)

    def __str__(self):
        flight_type = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({int(round(self._duration))}h) [{flight_type}]"

    def __eq__(self, other):
        if not isinstance(other, Flight):
            return False
        return self._origin == other._origin and self._destination == other._destination

    def __add__(self, conn_flight):
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

    def set_origin(self, origin):
        self._origin = origin

    def set_destination(self, destination):
        self._destination = destination
