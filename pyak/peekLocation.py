# File: peekLocation.py
# Yak Peek Location Model

class PeekLocation:
  def __init__(self, raw):
    self.id = raw['peekID']
    self.canSubmit = bool(raw['canSubmit'])
    self.name = raw['location']

    lat = raw['latitude']
    lon = raw['longitude']
    d = raw['delta']

    # TODO: figure out exactly how delta works
    self.location = Location(lat, lon, d)
