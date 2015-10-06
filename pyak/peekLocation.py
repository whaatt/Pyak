"""peeklocation.py - Describes the peek location model of the API"""


class PeekLocation:

    def __init__(self, raw):
        self.id = raw['peekID']
        self.can_submit = bool(raw['canSubmit'])
        self.name = raw['location']
        lat = raw['latitude']
        lon = raw['longitude']
        d = raw['delta']
        self.location = Location(lat, lon, d)

