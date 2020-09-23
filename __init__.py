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

    def __init__(self, env="dev", base_path=None):

        self.path_dict = {}
        self.file_dict = {}
        self.settings = {}
        self.settings_file_name = f"settings.{env}.json"

        # ensure to install this package at the first level of the project
        self.base_path = base_path or self.get_base_path()
        self.load_settings()

    def get_base_path(self):
        """
        Return one level lower as we expect this code
        to be cloned into a project
        """
        basename = os.path.dirname(os.path.dirname(__file__))
        return basename

    def load_settings(self, settings_file_name=None):
        """
        load settings, if the settings file is located in a different location
        then call load settings again with the name of the file to load
        """
        if settings_file_name:
            self.settings_file_name = settings_file_name

        settings_path = os.path.join(self.base_path, self.settings_file_name)

        if os.path.exists(settings_path):
            with open(settings_path) as handle:
                settings = json.load(handle)

                self.parse_settings(settings)

    def parse_settings(self, settings):
        self.setup_paths(settings)
        self.settings = settings["settings"]

    def setup_paths(self, settings):
        """
        sets up the file directories file paths
        """

        for path_info in settings.get("createDirs", []):
            os.makedirs(os.path.join(self.base_path, path_info["path"]), exist_ok=True)
            path_key = path_info.get("key") or os.path.basename(path_info["path"])
            self.path_dict[path_key] = os.path.join(self.base_path, path_info["path"])

        for path_info in settings.get("dirs", []):
            path_key = path_info.get("key") or os.path.basename(path_info["path"])
            self.path_dict[path_key] = os.path.join(self.base_path, path_info["path"])

        for fileInfo in settings.get("files", []):
            filename = os.path.basename(fileInfo["path"])
            file_key = fileInfo.get("key") or filename
            self.file_dict[file_key] = os.path.join(self.base_path, fileInfo["path"])

    def get_dir(self, key):
        return self.path_dict[key]

    def get_file(self, key):
        return self.file_dict[key]

    def get_setting(self, key, default=None):
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
                return default
        return value


settings = {}
default = {}


def get_settings(env=None, base_path=None) -> SettingsManager:

    if not default and not env:
        try:
            from env import env as imported_env
            env = imported_env
        except ImportError:
            raise RuntimeError("env must be specified or defined in env.py")
    if not default:
        default["env"] = env
    if not env:
        env = default["env"]
    if env not in settings:
        settings[env] = SettingsManager(env=env, base_path=base_path)

    return settings[env]
