class SpotifyAlbum:
    def __init__(self, id:str, name, release_date:str, album_type:str, total_tracks:int):
        self.id = id
        self.name = name
        self.release_date = release_date
        self.album_type = album_type
        self.total_tracks = total_tracks
    
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
    def release_date(self):
      return getattr(self, "_release_date", None)

    @release_date.setter
    def release_date(self, value):
      self._release_date = value
      
    @property
    def album_type(self):
      return getattr(self, "_album_type", None)

    @album_type.setter
    def album_type(self, value):
      self._album_type = value

    @property
    def total_tracks(self):
      return getattr(self, "_total_tracks", None)

    @total_tracks.setter
    def total_tracks(self, value):
      self._total_tracks = value

    def to_dict(self):
      return {
        "id": self.id,
        "name": self.name,
        "release_date": self.release_date,
        "album_type": self.album_type,
        "total_tracks": self.total_tracks
      }
    