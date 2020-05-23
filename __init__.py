###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

import os
import json


class SettingsManager:
    """
    settings manager class
    use this to setup settings
    default location for the settings file is 
    settings.json
    """
    def __init__(self):

        self.pathDict = {}
        self.fileDict = {}
        self.settings = {}
        self.settingsFileName = "settings.json"

        # ensure to install this package at the first level of the project
        self.basePath = self.getBasePath()
        self.loadSettings()

    def getBasePath(self):
        """
        if the dirname of the root directory is settingsManager
        return that directory.
        Otherwise return one level lower as we expect this code 
        to be cloned into a project
        """
        basename, dirname = os.path.split(os.path.dirname(__file__))
        if dirname == "settingsManager":
            return os.path.dirname(__file__)
        else:
            return basename

    def loadSettings(self, settingsFileName=None):
        """
        load settings, if the settings file is located in a different location
        then call load settings again with the name of the file to load 
        """
        if settingsFileName:
            self.settingsFileName = settingsFileName

        settingsPath = os.path.join(self.basePath, self.settingsFileName)

        if os.path.exists(settingsPath):
            with open(settingsPath) as handle:
                settings = json.load(handle)

                self.parseSettings(settings)

    def parseSettings(self, settings):
        self.setupPaths(settings)
        self.settings = settings["settings"]

    def setupPaths(self, settings):
        """
        sets up the file directories file paths
        """

        for pathInfo in settings["createDirs"]:
            os.makedirs(os.path.join(self.basePath, pathInfo["path"]), exist_ok=True)
            pathKey = pathInfo.get("key") or os.path.basename(pathInfo["path"])
            self.pathDict[pathKey] = os.path.join(self.basePath, pathInfo["path"])

        for pathInfo in settings["dirs"]:
            pathKey = pathInfo.get("key") or os.path.basename(pathInfo["path"])
            self.pathDict[pathKey] = os.path.join(self.basePath, pathInfo["path"])

        for fileInfo in settings["files"]:
            filename = os.path.basename(fileInfo["path"])
            fileKey = fileInfo.get("key") or filename
            self.fileDict[fileKey] = os.path.join(self.basePath, fileInfo["path"])

    def getDir(self, key):
        return self.pathDict[key]

    def getFile(self, key):
        return self.fileDict[key]

    def getSetting(self, key):
        """
        takes a string of key1/key2
        and returns the value of self.settings["key1"]["key2"]
        if the value exists, otherwise returns None

        key: (str)
            the key can be of the form key1/key2
            and the setting with traverse the dictionary
            to get the setting.
        """

        keys = key.split("/")
        value = self.settings
        for key in keys:
            value = value.get(key)
            if not value:
                return None
        return value


settingsManager = SettingsManager()
