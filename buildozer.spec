[app]
title = SchoolTracker
package.name = schooltracker
package.domain = org.tracker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 0.1

# Указываем стабильный Python 3.11 и нужные библиотеки
requirements = python3==3.11.6,kivy==2.3.0,requests,certifi,urllib3,idna,charset-normalizer,plyer

orientation = portrait
fullscreen = 0

# Разрешения Android (интернет обязателен для бота/запросов)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,FOREGROUND_SERVICE

# Фиксируем проверенные версии SDK и NDK, чтобы сборка не падала
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
