# Introduction

This settings manager tool is to help with keeping your settings in a single location
Clone this module into your project and simply access the settings manager through:

```
from settingsManager import settingsManager

settingsManager.get_setting("someValue")

# for nested json lookup, simply just use a slash to access the parameter
settingsManager.get_setting("redis/host")
settingsManager.get_setting("redis/port")
```

The settingsManager will by default look for a `settings.json` file in your home directory and parse as soon as the import happens. If you wish to parse a file in a different location, simply call settingsManager.loadSettings("path/to/filename").

A sample format of the configuration file is provided in the settings.sample.json file.
Copy and modify this and store it at the root directory of your project as "settings.json"

## Some notes on the settings.json format

### createDirs

A list of dictionaries containing "path" (required), "key" (optional) keys. On load, the settingsManager will create these directories if they do not exist and index them by the basename if no "key" information is provided. 

### dirs

A list of dictionaries containing "path" (required), "key" (optional) keys. Use this if you do not intend on creating these directories

### files

A list of files containing "path" (required), "key" (optional) keys. Use this if you do not intend on creating these directories

### Getting paths to directories or files
To get the path call `settingsManager.getDir(key)` to get the directory or `settingsManager.getFile(key)` to get the path to a file.
 