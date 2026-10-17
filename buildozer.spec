[app]
title = Austin Proxy
package.name = austinproxy
package.domain = org.aqualeaks
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer,pysocks
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
