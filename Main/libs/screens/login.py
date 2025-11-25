from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivy.uix.image import Image
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.core.text import LabelBase
import os
# Nama file database, pastikan konsisten dengan signup.py
DB_NAME = "user_data.db"
import sqlite3

# Bangun path secara portable untuk menghindari escape sequence issues pada Windows
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_PATH = os.path.join(MAIN_DIR, "Assets", "fonts", "Montserrat-Bold.ttf")
FONT_PATH = os.path.join(MAIN_DIR, "Assets", "fonts", "Poppins-Bold.ttf")
FONT_PATH=os.path.join(MAIN_DIR,"Assets", "fonts","LeagueSpartan-Bold.ttf")
FONT_PATH=os.path.join(MAIN_DIR,"assets","fonts","Roboto-Light.ttf")
FONT_PATH=os.path.join(MAIN_DIR,"Assets","fonts","Montserrat-Arabic-SemiBold.otf")
LabelBase.register(name="LeaguaeSpartan_Bold",fn_regular=FONT_PATH)
LabelBase.register(name="Montserrat-Arabic-SemiBold.otf",fn_regular=FONT_PATH)
LabelBase.register(name="Roboto_Light",fn_regular=FONT_PATH)
LabelBase.register(name="montserrat", fn_regular=FONT_PATH)
LabelBase.register(name="poppins_bold",fn_regular=FONT_PATH)
# Mengatur ukuran window
#Window.size = (1000, 600)

class LoginScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build()


    def build(self):
        self.theme_cls.theme_style = "Light"
        
        # 1. Screen Utama
        

        # 2. Layout Utama (Horizontal)
        main_layout = MDBoxLayout(orientation='horizontal')
        
        # --- BAGIAN KIRI (GAMBAR) ---
        left_layout = MDFloatLayout(size_hint_x=0.6)
        
        # Gambar Background
        bg_image = FitImage(
            source= "D:\Project Pemdas Octatech test\Main\Assets\Images\login page.jpg",
            radius=[0, 0, 0, 0]
        )

        logo = Image(
            source = "D:\Project Pemdas Octatech test\Main\Assets\Images\LogoText.png",
            size = (dp(500), dp(500)),
            size_hint =(None,None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        
        # Overlay Biru Transparan
        overlay = MDBoxLayout(md_bg_color=(0, 0.5, 1, 0.1))
        
        # Logo Container
        logo_box = MDBoxLayout(
            orientation='vertical',
            pos_hint={"center_x": .5, "center_y": .5},
            adaptive_height=True,
            spacing=dp(10)
        )
        
        
        
        tagline = MDLabel(
            text="Recommended Gadget for Student",
            halign="center",
            pos_hint={"center_x": .5, "center_y": 0.3},
            font_style="Title",
            role="medium",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_name="poppins_bold"
        )

        # Menyusun Bagian Kiri
        
        left_layout.add_widget(bg_image)
        left_layout.add_widget(overlay)
        left_layout.add_widget(logo_box)
        left_layout.add_widget(tagline)
        left_layout.add_widget(logo)


        # --- BAGIAN KANAN (FORM LOGIN) ---
        right_layout = MDFloatLayout(
            size_hint_x=0.4,
            md_bg_color=(11/255, 20/255, 54/255, 1) # Warna Navy
        )
        
        # Container Form (Vertical)
        form_box = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            pos_hint={"center_x": .5, "center_y": .5},
            padding=dp(40),
            spacing=dp(20)
        )
        
        # Judul
        title_label = MDLabel(
            text="Login",
            font_style="Headline",
            role="medium",
            bold=True,
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_name="LeaguaeSpartan_Bold"
        )
        
        subtitle_label = MDLabel(
            text="Masukkan username dan password untuk melanjutkan",
            font_style="Body",
            role="small",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            size_hint_y=None,
            font_name = "poppins_bold"
        )
        subtitle_label.height = subtitle_label.texture_size[1] # Trik agar tinggi label pas

        # Input Username
        self.username_field = MDTextField(
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10],
            
        )
        username_hint = MDTextFieldHintText(
            text="Username",
            text_color_normal=(0.5, 0.5, 0.5, 1),
            font_name="roboto_light"
        )
        self.username_field.add_widget(username_hint)

        # Input Password
        self.password_field = MDTextField(
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10],
            password=True # (Opsional: tambahkan ini jika ingin bintang-bintang)
        )
        password_hint = MDTextFieldHintText(
            text="Password",
            text_color_normal=(0.5, 0.5, 0.5, 1),
            font_name="roboto_light"
        )
        self.password_field.add_widget(password_hint)



        # Tombol Sign In
        btn_signin = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0, 0.47, 0.8, 1),
            theme_width="Custom",
            size_hint_x=1,
            radius=[dp(10)],
            pos_hint={"center_x": .5}
        )
        btn_signin.bind(on_release=self.do_login) # Hubungkan ke fungsi
        
        btn_text = MDButtonText(
            text="Sign In",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": .5, "center_y": .5},
            font_style="Title",
            role="medium",
            font_name="monserrat-arabic-semisbold.otf"
        )
        btn_signin.add_widget(btn_text)
        btn_signin

        # Footer (Link Sign Up)
        footer_box = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(5),
            pos_hint={'center_x': .5}
        )
        footer_label = MDLabel(
            text="Belum punya akun?",
            halign="right",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            font_style="Body",
            role="small",
            font_name="monserrat-arabic-semisbold.otf"
        )
        
        # Tombol Sign Up (Text Button)
        btn_signup = MDButton(style="text")
        btn_signup_text = MDButtonText(
            text="Sign Up",
            theme_text_color="Custom",
            pos_hint={"center_x": .5, "center_y": .5},
            text_color=(1, 0.8, 0, 1),
            bold=True,
             font_name="roboto_light"
        )
        btn_signup.add_widget(btn_signup_text)
        btn_signup.bind(on_release = self.go_to_signup)
        
        footer_box.add_widget(footer_label)
        footer_box.add_widget(btn_signup)

        # Menyusun Bagian Kanan
        form_box.add_widget(title_label)
        form_box.add_widget(subtitle_label)
        form_box.add_widget(self.username_field)
        form_box.add_widget(self.password_field)
        form_box.add_widget(Widget(size_hint_y=None, height=dp(10))) # Spacer
        form_box.add_widget(btn_signin)
        form_box.add_widget(footer_box)
        
        right_layout.add_widget(form_box)

        # Gabungkan Kiri dan Kanan ke Layout Utama
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Masukkan Layout Utama ke Screen
        self.add_widget(main_layout)

    def do_login(self, instance):
        # LOGIKA DB ADA DI SINI
        username = self.username_field.text
        password = self.password_field.text

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

        if result:
            # Jika sukses, pindah ke screen data_app
            # result tuple: (id, nama, username, password)
            nama_user = result[1]
            # SIMPAN ke app untuk dikirim ke HomeScreen
            MDApp.get_running_app().user_nama = nama_user

            # Pindah ke home screen
            self.manager.current = "home_screen"
            self.password_field.text = ""
        else:
            self.show_snackbar("Gagal Login!")

    def go_to_signup(self, instance):
        # Fungsi untuk pindah layar
        self.manager.current = "signup_screen"
        self.manager.transition.direction = "left"    
        
    def show_snackbar(self, text):
        snackbar = MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        snackbar.open()    

 

