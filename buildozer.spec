[app]
# (str) Title of your application
title = GoFishMobile

# (str) Package name
package.name = gofishmobile

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ogcardgames.app

# (str) Source code where main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,kv,ttf,png,jpg,txt,atlas,json

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = setuptools<70, cython>=3.1.0, python3, kivy==2.3.1, pillow==9.0.0, materialyoucolor, exceptiongroup, asyncgui, asynckivy, https://github.com/kivymd/KivyMD/archive/master.zip

# (str) Icon of the application
icon.filename = Icon.png

# (list) Supported orientations
orientation = portrait

# (int) Target Android API
android.api = 31

android.ndk = 27b

# (int) Minimum API your APK supports
android.minapi = 28

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Use --private data storage (True) or public storage (False)
android.private_storage = True

# (str) Android SDK/NDK paths

# (bool) Skip SDK/NDK updates (we preinstalled them)
#android.skip_update = True

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (str) Format used to package the app for debug
android.debug_artifact = apk

p4a.url = https://github.com/kivy/python-for-android.git
p4a.branch = develop
p4a.python_version = 3.10

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
