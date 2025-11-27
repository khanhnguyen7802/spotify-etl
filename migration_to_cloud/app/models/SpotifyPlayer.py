class SpotifyPlayer:
    def __init__(self, track_id, album_id, played_at):
      self.track_id = track_id
      self.album_id = album_id
      self.played_at = played_at
    
    # getters and setters
    @property
    def track_id(self):
        return getattr(self, "_track_id", None)
    @track_id.setter
    def track_id(self, value):
        self._track_id = value

    @property
    def album_id(self):
        return getattr(self, "_album_id", None)
    @album_id.setter
    def album_id(self, value):
        self._album_id = value
    
    @property
    def played_at(self):
        return getattr(self, "_played_at", None)
    @played_at.setter
    def played_at(self, value):
        self._played_at = value

    def to_dict(self):
      return {
        "track_id": self.track_id,
        "album_id": self.album_id,
        "played_at": self.played_at
      }