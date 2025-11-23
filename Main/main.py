import sys
import os

# Jika file dijalankan langsung (python Main/main.py), tambahkan folder project root
# ke sys.path supaya impor absolut `Main.*` ditemukan.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Main.libs.screens.login import LoginScreen
from Main.libs.screens.signup import SignupPage
from Main.libs.screens.firstpage import GadgetHomeScreen


from kivy.core.window import Window
import sqlite3
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel

#module code



Window.size = (1000, 600)

class OctaTechApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        #init_db() # Pastikan DB siap

        # SCREEN MANAGER: Pengatur lalu lintas halaman
        sm = MDScreenManager()
        
        # Tambahkan layar-layar ke manager
        sm.add_widget(GadgetHomeScreen(name ="first_page"))

        sm.add_widget(LoginScreen(name="login_screen"))

        sm.add_widget(SignupPage(name="signup_screen"))
        
        return sm

if __name__ == "__main__":
    OctaTechApp().run()



