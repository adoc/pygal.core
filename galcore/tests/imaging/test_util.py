import io
import pkgutil
import unittest

import PIL.PngImagePlugin
import PIL.JpegImagePlugin

import galcore.imaging.util


class TestUtil(unittest.TestCase):
    def setUp(self):
        self.test_img_1 = io.BytesIO(pkgutil.get_data('galcore',
                                                'tests/data/test_img_1.png'))
        self.test_img_2 = io.BytesIO(pkgutil.get_data('galcore',
                                                'tests/data/test_img_2.jpg'))

    def test_read_image(self):
        pil_image_1 = galcore.imaging.util.read_image(self.test_img_1)
        pil_image_2 = galcore.imaging.util.read_image(self.test_img_2)

        self.assertIsInstance(pil_image_1, PIL.PngImagePlugin.PngImageFile)
        self.assertIsInstance(pil_image_2, PIL.JpegImagePlugin.JpegImageFile)

        # TODO: Probably some other tests that could be written here.

    def test_preserve_aspect(self):
        self.assertEqual(
            galcore.imaging.util.preserve_aspect(1024,768, 512), (512, 384))
        self.assertEqual(
            galcore.imaging.util.preserve_aspect(1024,768, None, 384),
                        (512, 384))
        self.assertEqual(
            galcore.imaging.util.preserve_aspect(1024,768, 256, 384),
                         (256, 192))

    def test_resize_image(self):
        pil_image_1 = galcore.imaging.util.read_image(self.test_img_1)
        pil_image_2 = galcore.imaging.util.read_image(self.test_img_2)

        self.assertEqual(
            galcore.imaging.util.resize_image(pil_image_1, 512).size[0], 512)
        self.assertEqual(
            galcore.imaging.util.resize_image(pil_image_1, None, 512).size[1],
                         512)

        self.assertEqual(
            galcore.imaging.util.resize_image(pil_image_2, 256).size[0], 256)
        self.assertEqual(
            galcore.imaging.util.resize_image(pil_image_1, None, 256).size[1],
                         256)