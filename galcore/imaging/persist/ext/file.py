"""
"""
import os
import io
import hashlib
import pickle

from galcore.imaging import persist
from galcore.imaging.persist import model

from PIL.ImageFile import ImageFile


class DataFile:
    def __init__(self, filepath, init_data={}):
        """Initialize or load a pickled data file. 
        """

        self._filepath = filepath

        try:
            fp = open(self._filepath, "rb")
        except FileNotFoundError:
            fp = open(self._filepath, "wb")
        else:
            try:
                self.data = pickle.load(fp)
            except EOFError:
                self.data = init_data

    def save(self):
        """
        """

        with open(self._filepath, "wb") as fp:
            pickle.dump(self.data, fp)


class Persistence:
    """
    """
    # Handles file location
    # Handles file saving
    # Handles file loading
    # Handles file metadata.
    #   Determine what metadata to allow in files. Some things like
    #   tags should require a relational DB or other mechanism than
    #   file storage.
    # Handles checksum file. 
    #   Give option for different hashalg.

    def __init__(self, directory, make_directory=True, checksum_filepath=None,
                 metadata_filepath=None):
        """
        """

        self.directory = directory

        if make_directory is True:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

        checksum_filepath = checksum_filepath or os.path.join([self.directory,
                                                               'checksum.dat'])
        self.checksum_file = DataFile(checksum_filepath)
        self.checksum_map = model.ChecksumMap(self.checksum_file.data)

        metadata_filepath = metadata_filepath or os.path.join([self.directory,
                                                               'metadata.dat'])
        self.metadata_file = DataFile(metadata_filepath)
        self.metadata = model.MetaData(self.metadata_file.data)

    def save(self, model):
        pass

    def load(self, ident):
        pass


class Image:
    """This is meant to be a model.
    """