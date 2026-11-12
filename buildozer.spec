
[app]

title = SchoolTracker
package.name = schooltracker
package.domain = org.tracker

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,db,txt

version = 0.1

requirements = requirements = python3,kivy==2.3.0,requests,certifi,urllib3,idna,charset-normalizer,plyer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,FOREGROUND_SERVICE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
