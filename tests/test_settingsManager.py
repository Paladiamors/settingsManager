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

from __init__ import settingsManager


class Test(unittest.TestCase):

    def test_settingsManager(self):
        settingsManager.loadSettings("tests/settings.json")
        self.assertTrue(settingsManager.settings, "settings should exist")

        basePath = settingsManager.basePath

        self.assertTrue(os.path.exists(os.path.join(basePath, "dataDir")))
        self.assertTrue(os.path.exists(os.path.join(basePath, "dataDir/something")))
        self.assertTrue(settingsManager.getPath("dataDir"))
        self.assertTrue(settingsManager.getPath("something"))
        self.assertTrue(settingsManager.getFilePath("file.txt"))
        self.assertTrue(settingsManager.getFilePath("file2"))

        self.assertTrue(settingsManager.getSetting("env"), "prod")
        self.assertTrue(settingsManager.getSetting("somethingElse"), "someValue")
        self.assertTrue(settingsManager.getSetting("redis/host"), "localhost")
        self.assertTrue(settingsManager.getSetting("redis/port"), 8000)
        shutil.rmtree(settingsManager.getPath("dataDir"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_settingsManager']
    unittest.main()
