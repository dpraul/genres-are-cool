from sqlalchemy import Column, Integer, String, Float

from genres import Base


class Song(Base):
    __tablename__ = 'songs'
    
    track_id = Column(String(18), primary_key=True)
    song_id = Column(String(18))
    spotify_id = Column(String(22))

    # Information from GenreTags
    genre = Column(String(15))

    # Information in MSD and on Spotify
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    tempo = Column(Float)
    time_signature = Column(Integer)

    # Information on Spotify
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    duration_ms = Column(Integer)
    liveness = Column(Float)
    speechiness = Column(Float)
    valence = Column(Float)

    def __init__(self, track_id):
        self.track_id = track_id

    def __repr__(self):
        return '<Song %r>' % self.track_id
