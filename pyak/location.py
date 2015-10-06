"""location.py - Describes the location model of the API"""


class Location:

    def __init__(self, latitude, longitude, delta=None):
        self.latitude = latitude
        self.longitude = longitude
        if delta is None:
            delta = "0.030000"
        self.delta = delta

    def __str__(self):
        return "Location(%s, %s)" % (self.latitude, self.longitude)

