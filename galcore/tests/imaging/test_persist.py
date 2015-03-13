"""
"""

import os
import shutil
import uuid
import tempfile
import unittest


import galcore.imaging.persist.ext.file


class TestPersistExtFile(unittest.TestCase):
    """
    """

    def test_data_file(self):
        """
        """
        # TODO: Explore other unit test paths through the DataFile class.
        #           More test coverage required.
        tmp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4())+'.tmp')

        data_file = galcore.imaging.persist.ext.file.DataFile(tmp_path)

        data_file.data = {'foo': 'bar'}
        data_file.save()

        data_file = galcore.imaging.persist.ext.file.DataFile(tmp_path)
        self.assertEqual(data_file.data, {'foo': 'bar'})

        data_file.data.update({'bar': 'baz'})
        data_file.save()

        data_file = galcore.imaging.persist.ext.file.DataFile(tmp_path)
        self.assertEqual(data_file.data, {'foo': 'bar', 'bar': 'baz'})

        os.unlink(tmp_path)

    def test_persistence(self):
        tmp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

        persistence = galcore.imaging.persist.ext.file.Persistence(tmp_path)

        self.assertTrue(os.path.exists(os.path.join(tmp_path, 'checksum.dat')))
        self.assertTrue(os.path.exists(os.path.join(tmp_path, 'metadata.dat')))

        shutil.rmtree(tmp_path)
