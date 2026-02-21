[app]
title = Sistem_Hizmeti
package.name = sys_service
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,pyTelegramBotAPI,requests,certifi,idna,urllib3,charset-normalizer
orientation = portrait
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.permissions = INTERNET,ACCESS_NETWORK_STATE
[buildozer]
log_level = 2
warn_on_root = 1
