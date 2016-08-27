"""
Re-implementation of https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py
"""

import tables


class SongEntries(object):
    def __init__(self, filename, songidx=0):
        """
        Open an existing H5 in read mode.
        Same function as in hdf5_utils, here so we avoid one import
        """
        self.h5 = tables.openFile(filename, mode='r')
        self.songidx = songidx

    @property
    def num_songs(self):
        """
        Return the number of songs contained in this h5 file, i.e. the number of rows
        for all basic informations like name, artist, ...
        """
        return self.h5.root.metadata.songs.nrows

    @property
    def artist_familiarity(self):
        """
        Get artist familiarity from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_familiarity[self.songidx]

    @property
    def artist_hotttnesss(self):
        """
        Get artist hotttnesss from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_hotttnesss[self.songidx]

    @property
    def artist_id(self):
        """
        Get artist id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_id[self.songidx]

    @property
    def artist_mbid(self):
        """
        Get artist musibrainz id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_mbid[self.songidx]

    @property
    def artist_playmeid(self):
        """
        Get artist playme id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_playmeid[self.songidx]

    @property
    def artist_7digitalid(self):
        """
        Get artist 7digital id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_7digitalid[self.songidx]

    @property
    def artist_latitude(self):
        """
        Get artist latitude from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_latitude[self.songidx]

    @property
    def artist_longitude(self):
        """
        Get artist longitude from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_longitude[self.songidx]

    @property
    def artist_location(self):
        """
        Get artist location from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_location[self.songidx]

    @property
    def artist_name(self):
        """
        Get artist name from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.artist_name[self.songidx]

    @property
    def release(self):
        """
        Get release from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.release[self.songidx]

    @property
    def release_7digitalid(self):
        """
        Get release 7digital id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.release_7digitalid[self.songidx]

    @property
    def song_id(self):
        """
        Get song id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.song_id[self.songidx]

    @property
    def song_hotttnesss(self):
        """
        Get song hotttnesss from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.song_hotttnesss[self.songidx]

    @property
    def title(self):
        """
        Get title from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.title[self.songidx]

    @property
    def track_7digitalid(self):
        """
        Get track 7digital id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.metadata.songs.cols.track_7digitalid[self.songidx]

    @property
    def similar_artists(self):
        """
        Get similar artists array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.metadata.songs.nrows == self.songidx + 1:
            return self.h5.root.metadata.similar_artists[self.h5.root.metadata.songs.cols.idx_similar_artists[self.songidx]:]
        return self.h5.root.metadata.similar_artists[self.h5.root.metadata.songs.cols.idx_similar_artists[self.songidx]:
                                                     self.h5.root.metadata.songs.cols.idx_similar_artists[self.songidx + 1]]

    @property
    def artist_terms(self):
        """
        Get artist terms array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.metadata.songs.nrows == self.songidx + 1:
            return self.h5.root.metadata.artist_terms[self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:]
        return self.h5.root.metadata.artist_terms[self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:
                                                  self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx + 1]]

    @property
    def artist_terms_freq(self):
        """
        Get artist terms array frequencies. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.metadata.songs.nrows == self.songidx + 1:
            return self.h5.root.metadata.artist_terms_freq[self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:]
        return self.h5.root.metadata.artist_terms_freq[self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:
                                                       self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx + 1]]

    @property
    def artist_terms_weight(self):
        """
        Get artist terms array frequencies. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.metadata.songs.nrows == self.songidx + 1:
            return self.h5.root.metadata.artist_terms_weight[
                   self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:]
        return self.h5.root.metadata.artist_terms_weight[self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx]:
                                                         self.h5.root.metadata.songs.cols.idx_artist_terms[self.songidx + 1]]

    @property
    def analysis_sample_rate(self):
        """
        Get analysis sample rate from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.analysis_sample_rate[self.songidx]

    @property
    def audio_md5(self):
        """
        Get audio MD5 from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.audio_md5[self.songidx]

    @property
    def danceability(self):
        """
        Get danceability from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.danceability[self.songidx]

    @property
    def duration(self):
        """
        Get duration from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.duration[self.songidx]

    @property
    def end_of_fade_in(self):
        """
        Get end of fade in from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.end_of_fade_in[self.songidx]

    @property
    def energy(self):
        """
        Get energy from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.energy[self.songidx]

    @property
    def key(self):
        """
        Get key from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.key[self.songidx]

    @property
    def key_confidence(self):
        """
        Get key confidence from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.key_confidence[self.songidx]

    @property
    def loudness(self):
        """
        Get loudness from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.loudness[self.songidx]

    @property
    def mode(self):
        """
        Get mode from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.mode[self.songidx]

    @property
    def mode_confidence(self):
        """
        Get mode confidence from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.mode_confidence[self.songidx]

    @property
    def start_of_fade_out(self):
        """
        Get start of fade out from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.start_of_fade_out[self.songidx]

    @property
    def tempo(self):
        """
        Get tempo from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.tempo[self.songidx]

    @property
    def time_signature(self):
        """
        Get signature from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.time_signature[self.songidx]

    @property
    def time_signature_confidence(self):
        """
        Get signature confidence from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.time_signature_confidence[self.songidx]

    @property
    def track_id(self):
        """
        Get track id from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.analysis.songs.cols.track_id[self.songidx]

    @property
    def segments_start(self):
        """
        Get segments start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_start[self.h5.root.analysis.songs.cols.idx_segments_start[self.songidx]:]
        return self.h5.root.analysis.segments_start[self.h5.root.analysis.songs.cols.idx_segments_start[self.songidx]:
                                                    self.h5.root.analysis.songs.cols.idx_segments_start[self.songidx + 1]]

    @property
    def segments_confidence(self):
        """
        Get segments confidence array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_confidence[
                   self.h5.root.analysis.songs.cols.idx_segments_confidence[self.songidx]:]
        return self.h5.root.analysis.segments_confidence[
               self.h5.root.analysis.songs.cols.idx_segments_confidence[self.songidx]:
               self.h5.root.analysis.songs.cols.idx_segments_confidence[self.songidx + 1]]

    @property
    def segments_pitches(self):
        """
        Get segments pitches array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_pitches[
                   self.h5.root.analysis.songs.cols.idx_segments_pitches[self.songidx]:, :]
        return self.h5.root.analysis.segments_pitches[self.h5.root.analysis.songs.cols.idx_segments_pitches[self.songidx]:
                                                      self.h5.root.analysis.songs.cols.idx_segments_pitches[self.songidx + 1], :]

    @property
    def segments_timbre(self):
        """
        Get segments timbre array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_timbre[self.h5.root.analysis.songs.cols.idx_segments_timbre[self.songidx]:,
                                                         :]
        return self.h5.root.analysis.segments_timbre[self.h5.root.analysis.songs.cols.idx_segments_timbre[self.songidx]:
                                                     self.h5.root.analysis.songs.cols.idx_segments_timbre[self.songidx + 1], :]

    @property
    def segments_loudness_max(self):
        """
        Get segments loudness max array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_loudness_max[
                   self.h5.root.analysis.songs.cols.idx_segments_loudness_max[self.songidx]:]
        return self.h5.root.analysis.segments_loudness_max[
               self.h5.root.analysis.songs.cols.idx_segments_loudness_max[self.songidx]:
               self.h5.root.analysis.songs.cols.idx_segments_loudness_max[self.songidx + 1]]

    @property
    def segments_loudness_max_time(self):
        """
        Get segments loudness max time array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_loudness_max_time[
                   self.h5.root.analysis.songs.cols.idx_segments_loudness_max_time[self.songidx]:]
        return self.h5.root.analysis.segments_loudness_max_time[
               self.h5.root.analysis.songs.cols.idx_segments_loudness_max_time[self.songidx]:
               self.h5.root.analysis.songs.cols.idx_segments_loudness_max_time[self.songidx + 1]]

    @property
    def segments_loudness_start(self):
        """
        Get segments loudness start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.segments_loudness_start[
                   self.h5.root.analysis.songs.cols.idx_segments_loudness_start[self.songidx]:]
        return self.h5.root.analysis.segments_loudness_start[
               self.h5.root.analysis.songs.cols.idx_segments_loudness_start[self.songidx]:
               self.h5.root.analysis.songs.cols.idx_segments_loudness_start[self.songidx + 1]]

    @property
    def sections_start(self):
        """
        Get sections start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.sections_start[self.h5.root.analysis.songs.cols.idx_sections_start[self.songidx]:]
        return self.h5.root.analysis.sections_start[self.h5.root.analysis.songs.cols.idx_sections_start[self.songidx]:
                                                    self.h5.root.analysis.songs.cols.idx_sections_start[self.songidx + 1]]

    @property
    def sections_confidence(self):
        """
        Get sections confidence array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.sections_confidence[
                   self.h5.root.analysis.songs.cols.idx_sections_confidence[self.songidx]:]
        return self.h5.root.analysis.sections_confidence[
               self.h5.root.analysis.songs.cols.idx_sections_confidence[self.songidx]:
               self.h5.root.analysis.songs.cols.idx_sections_confidence[self.songidx + 1]]

    @property
    def beats_start(self):
        """
        Get beats start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.beats_start[self.h5.root.analysis.songs.cols.idx_beats_start[self.songidx]:]
        return self.h5.root.analysis.beats_start[self.h5.root.analysis.songs.cols.idx_beats_start[self.songidx]:
                                                 self.h5.root.analysis.songs.cols.idx_beats_start[self.songidx + 1]]

    @property
    def beats_confidence(self):
        """
        Get beats confidence array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.beats_confidence[
                   self.h5.root.analysis.songs.cols.idx_beats_confidence[self.songidx]:]
        return self.h5.root.analysis.beats_confidence[self.h5.root.analysis.songs.cols.idx_beats_confidence[self.songidx]:
                                                      self.h5.root.analysis.songs.cols.idx_beats_confidence[self.songidx + 1]]

    @property
    def bars_start(self):
        """
        Get bars start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.bars_start[self.h5.root.analysis.songs.cols.idx_bars_start[self.songidx]:]
        return self.h5.root.analysis.bars_start[self.h5.root.analysis.songs.cols.idx_bars_start[self.songidx]:
                                                self.h5.root.analysis.songs.cols.idx_bars_start[self.songidx + 1]]

    @property
    def bars_confidence(self):
        """
        Get bars start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.bars_confidence[self.h5.root.analysis.songs.cols.idx_bars_confidence[self.songidx]:]
        return self.h5.root.analysis.bars_confidence[self.h5.root.analysis.songs.cols.idx_bars_confidence[self.songidx]:
                                                     self.h5.root.analysis.songs.cols.idx_bars_confidence[self.songidx + 1]]

    @property
    def tatums_start(self):
        """
        Get tatums start array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.tatums_start[self.h5.root.analysis.songs.cols.idx_tatums_start[self.songidx]:]
        return self.h5.root.analysis.tatums_start[self.h5.root.analysis.songs.cols.idx_tatums_start[self.songidx]:
                                                  self.h5.root.analysis.songs.cols.idx_tatums_start[self.songidx + 1]]

    @property
    def tatums_confidence(self):
        """
        Get tatums confidence array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.analysis.songs.nrows == self.songidx + 1:
            return self.h5.root.analysis.tatums_confidence[
                   self.h5.root.analysis.songs.cols.idx_tatums_confidence[self.songidx]:]
        return self.h5.root.analysis.tatums_confidence[self.h5.root.analysis.songs.cols.idx_tatums_confidence[self.songidx]:
                                                       self.h5.root.analysis.songs.cols.idx_tatums_confidence[self.songidx + 1]]

    @property
    def artist_mbtags(self):
        """
        Get artist musicbrainz tag array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.musicbrainz.songs.nrows == self.songidx + 1:
            return self.h5.root.musicbrainz.artist_mbtags[
                   self.h5.root.musicbrainz.songs.cols.idx_artist_mbtags[self.songidx]:]
        return self.h5.root.musicbrainz.artist_mbtags[self.h5.root.metadata.songs.cols.idx_artist_mbtags[self.songidx]:
                                                      self.h5.root.metadata.songs.cols.idx_artist_mbtags[self.songidx + 1]]

    @property
    def artist_mbtags_count(self):
        """
        Get artist musicbrainz tag count array. Takes care of the proper indexing if we are in aggregate
        file. By default, return the array for the first song in the h5 file.
        To get a regular numpy ndarray, cast the result to: numpy.array( )
        """
        if self.h5.root.musicbrainz.songs.nrows == self.songidx + 1:
            return self.h5.root.musicbrainz.artist_mbtags_count[
                   self.h5.root.musicbrainz.songs.cols.idx_artist_mbtags[self.songidx]:]
        return self.h5.root.musicbrainz.artist_mbtags_count[self.h5.root.metadata.songs.cols.idx_artist_mbtags[self.songidx]:
                                                            self.h5.root.metadata.songs.cols.idx_artist_mbtags[self.songidx + 1]]

    @property
    def year(self):
        """
        Get release year from a HDF5 song file, by default the first song in it
        """
        return self.h5.root.musicbrainz.songs.cols.year[self.songidx]
