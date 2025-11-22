from libs.screens.login.login import log
l = Log


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
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(SignupScreen(name="signup_screen"))
        
        return sm

if __name__ == "__main__":
    OctaTechApp().run()



