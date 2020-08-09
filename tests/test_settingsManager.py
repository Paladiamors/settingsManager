###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

import os
import shutil
import unittest
from pprint import pprint
from settings import get_settings


class Test(unittest.TestCase):

    def test_settings(self):

        base_path = os.path.dirname(__file__)
        settings = get_settings(base_path=base_path)
        settings.load_settings("settings.dev.json")
        self.assertTrue(settings.settings, "settings should exist")
        pprint(settings.settings)

        base_path = settings.base_path

        self.assertTrue(os.path.exists(os.path.join(base_path, "dataDir")))
        self.assertTrue(os.path.exists(os.path.join(base_path, "dataDir/something")))
        self.assertTrue(settings.get_dir("dataDir"))
        self.assertTrue(settings.get_dir("something"))
        self.assertTrue(settings.get_file("file.txt"))
        self.assertTrue(settings.get_file("file2"))

        self.assertTrue(settings.get_setting("env"), "prod")
        self.assertTrue(settings.get_setting("somethingElse"), "someValue")
        self.assertTrue(settings.get_setting("redis/host"), "localhost")
        self.assertTrue(settings.get_setting("redis/port"), 8000)
        shutil.rmtree(settings.get_dir("dataDir"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_settings']
    unittest.main()
