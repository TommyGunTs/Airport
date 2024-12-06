class Airport:
    def __init__(self, code, city, country):
        self._code = code
        self._city = city
        self._country = country

    def __str__(self):
        return f"{self._code} ({self._city}, {self._country})"

    def __eq__(self, other):
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
