from app.models.SpotifyAlbum import SpotifyAlbum

class SpotifyTrack:
    def __init__(self, id, album: SpotifyAlbum, artists, duration_ms, name:str, popularity):
      self.id = id
      self.name = name
      self.album = album
      self.artists = artists
      self.duration_ms = duration_ms
      self.popularity = popularity
    
    # getters and setters
    @property
    def id(self):
        return getattr(self, "_id", None) 
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return getattr(self, "_name", None)
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def album(self):
        return getattr(self, "_album", None)

    @album.setter
    def album(self, value):
        self._album = value

    @property
    def artists(self):
        return getattr(self, "_artists", None)

    @artists.setter
    def artists(self, value):
        self._artists = value

    @property
    def duration_ms(self):
        return getattr(self, "_duration_ms", None)

    @duration_ms.setter
    def duration_ms(self, value):
        self._duration_ms = value


    @property
    def popularity(self):
        return getattr(self, "_popularity", None)

    @popularity.setter
    def popularity(self, value):
        self._popularity = value

    def to_dict(self):
      return {
        "id": self.id,
        "name": self.name,
        "album": self.album.to_dict(),
        "artists": [artist.to_dict() for artist in self.artists],
        "duration_ms": self.duration_ms,
        "popularity": self.popularity
      }