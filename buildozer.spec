[app]

# (str) Title of your application
title = School Tracker

# (str) Package name
package.name = schooltracker

# (str) Package domain (needed for android packaging)
package.domain = org.tracker

# (list) Source files to include (let it include python files, graphics, etc.)
source.include_exts = py,png,jpg,kv,atlas

# (str) Source directory where the application files are located
source.dir = .

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Note: urllib3, certifi, idna, charset_normalizer подтягиваются через requests, 
# но для Android лучше явно указывать основные зависимости Python.
requirements = python3,kivy,plyer,requests,certifi

# (str) Supported orientations
orientation = portrait

# (int) Set fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android app theme, or use default
# android.theme = @android:style/Theme.NoTitleBar

# (bool) Use AndroidX for support libraries
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
