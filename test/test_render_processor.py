import io
import os
import unittest
import bpy
from Cython.Tests import xmlrunner

import test
from autoblender.renderer_processor import RendererProcessor

TEST_PATH = os.path.dirname(test.__file__)

class TestRendererProcessor(unittest.TestCase):
    def test_applied_parameters_when_correct_parameters(self):
        parameters = {
            'scene': {
                'render': {
                    'resolution_x': 2154,
                    'resolution_y': 42
                }
            }
        }
        processor = RendererProcessor(f"{TEST_PATH}{os.sep}resources{os.sep}basic.blend", parameters, available_settings_file=f"{TEST_PATH}{os.sep}resources{os.sep}available_settings_correct.yml")
        processor.apply_parameters_from_settings()
        self.assertEqual(bpy.context.scene.render.resolution_x, 2154)
        self.assertEqual(bpy.context.scene.render.resolution_y, 42)

    def test_applied_parameters_when_unexisting_parameters(self):
        parameters = {
            'scene': {
                'render': {
                    'doesntexists': 10,
                }
            }
        }
        processor = RendererProcessor(f"{TEST_PATH}{os.sep}resources{os.sep}basic.blend", parameters, available_settings_file=f"{TEST_PATH}{os.sep}resources{os.sep}available_settings_correct.yml")
        with self.assertRaises(Exception):
            processor.apply_parameters_from_settings()


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)