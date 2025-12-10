import os
import sqlite3
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.widget import Widget
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.app import MDApp
from kivy.uix.image import Image

# --- SETUP PATH ---
current_file_path = os.path.abspath(__file__)
screens_dir = os.path.dirname(current_file_path)
libs_dir = os.path.dirname(screens_dir)
MAIN_DIR = os.path.dirname(libs_dir)
ASSETS_DIR = os.path.join(MAIN_DIR, "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "Images")

# --- DATABASE ---
DB_NAME = "user_data.db"

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login_screen"

    def on_enter(self):
        # Mencegah duplikasi layout saat bolak-balik screen
        if not self.children:
            self.build()

    def build(self):
        self.theme_cls.theme_style = "Light"
        
        # 1. Layout Utama (Horizontal)
        main_layout = MDBoxLayout(orientation='horizontal')
        
        # --- BAGIAN KIRI (GAMBAR & LOGO) ---
        left_layout = MDFloatLayout(size_hint_x=0.6)
        
        # Gambar Background
        bg_path = os.path.join(IMG_DIR, "login page.jpg")
        if os.path.exists(bg_path):
            bg_image = FitImage(source=bg_path)
        else:
            bg_image = MDLabel(text="BG Missing", halign="center")

        # Logo
        logo_path = os.path.join(IMG_DIR, "LogoText.png")
        if os.path.exists(logo_path):
            logo = Image(
                source=logo_path,
                size=(dp(700), dp(700)),
                size_hint=(None, None),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            )
        else:
            logo = Widget()
        
        # Overlay Biru Transparan
        overlay = MDBoxLayout(md_bg_color=(0, 0.5, 1, 0.1))
        
        tagline = MDLabel(
            text="Recommended Gadget for Student",
            halign="center",
            pos_hint={"center_x": .5, "center_y": 0.3},
            font_style="Headline",
            role="medium",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            # font_name="poppins_bold" # Pastikan font terload di main.py
        )

        left_layout.add_widget(bg_image)
        left_layout.add_widget(overlay)
        left_layout.add_widget(tagline)
        left_layout.add_widget(logo)

        # --- BAGIAN KANAN (FORM LOGIN) ---
        right_layout = MDFloatLayout(
            size_hint_x=0.4,
            md_bg_color=(11/255, 20/255, 54/255, 1) # Warna Navy sesuai desainmu
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
            font_style="Display",
            role="medium",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            # font_name="LeaguaeSpartan_Bold"
        )
        
        subtitle_label = MDLabel(
            text="Masukkan username dan password untuk melanjutkan",
            font_style="Body",
            role="small",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            size_hint_y=None,
            adaptive_height=True
            # font_name="poppins_bold"
        )

        # --- INPUT USERNAME (FIX: Rounded & White) ---
        username_container = MDCard(
            size_hint=(None, None),
            size=(dp(350), dp(56)), # Lebar disesuaikan dengan desain Desktop (1920x1080)
            pos_hint={'center_x': .5},
            radius=[25, 25, 25, 25],
            md_bg_color=(1, 1, 1, 1), # Putih Solid
            elevation=0,
        )
        
        self.username_field = MDTextField(
            mode="outlined",
            size_hint=(1, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            radius=[25, 25, 25, 25],
            theme_bg_color="Custom",
            fill_color_normal=(0, 0, 0, 0),
            fill_color_focus=(0, 0, 0, 0),
            line_color_normal=(0, 0, 0, 0), # Hapus border bawaan
            line_color_focus=(0, 0, 0, 0),
        )
        
        username_hint = MDTextFieldHintText(
            text="Username",
            text_color_normal=(0.5, 0.5, 0.5, 1),
            # font_name="roboto_light"
        )
        self.username_field.add_widget(username_hint)
        username_container.add_widget(self.username_field) # Masukkan field ke container

        # --- INPUT PASSWORD (FIX: Rounded & White) ---
        password_container = MDCard(
            size_hint=(None, None),
            size=(dp(350), dp(56)),
            pos_hint={'center_x': .5},
            radius=[25, 25, 25, 25],
            md_bg_color=(1, 1, 1, 1), # Putih Solid
            elevation=0,
        )

        self.password_field = MDTextField(
            mode="outlined",
            size_hint=(1, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            radius=[25, 25, 25, 25],
            theme_bg_color="Custom",
            fill_color_normal=(0, 0, 0, 0),
            fill_color_focus=(0, 0, 0, 0),
            line_color_normal=(0, 0, 0, 0),
            line_color_focus=(0, 0, 0, 0),
            password=True
        )
        
        password_hint = MDTextFieldHintText(
            text="Password",
            text_color_normal=(0.5, 0.5, 0.5, 1),
            # font_name="roboto_light"
        )
        self.password_field.add_widget(password_hint)
        password_container.add_widget(self.password_field) # Masukkan field ke container

        # Tombol Sign In
        btn_signin = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0, 0.47, 0.8, 1),
            theme_width="Custom",
            size_hint_x=None,
            width=dp(350), # Samakan lebar dengan input
            radius=[dp(10)],
            pos_hint={"center_x": .5}
        )
        btn_signin.bind(on_release=self.do_login)
        
        btn_text = MDButtonText(
            text="Sign In",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": .5, "center_y": .5},
            font_style="Title",
            role="medium",
            # font_name="monserrat-arabic-semisbold.otf"
        )
        btn_signin.add_widget(btn_text)

        # Footer (Link Sign Up)
        footer_box = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(5),
            pos_hint={'center_x': .5}
        )
        footer_label = MDLabel(
            text="Belum punya akun?",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            font_style="Body",
            role="small",
            # font_name="monserrat-arabic-semisbold.otf"
        )
        
        btn_signup = MDButton(style="text")
        btn_signup_text = MDButtonText(
            text="Sign Up",
            theme_text_color="Custom",
            text_color=(1, 0.8, 0, 1),
            bold=True,
            pos_hint={"center_x": .5, "center_y": .5},
            # font_name="roboto_light"
        )
        btn_signup.add_widget(btn_signup_text)
        btn_signup.bind(on_release=self.go_to_signup)
        
        footer_box.add_widget(footer_label)
        footer_box.add_widget(btn_signup)

        # Tombol Kembali
        btn_back = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0, 0.47, 0.8, 1),
            theme_width="Custom",
            size_hint_x=None,
            width=dp(350),
            radius=[dp(10)],
            pos_hint={"center_x": .5}
        )
        btn_text_back = MDButtonText(
            text="Kembali",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": .5, "center_y": .5},
            font_style="Title",
            role="medium",
            # font_name="monserrat-arabic-semisbold.otf"
        )
        btn_back.add_widget(btn_text_back)
        btn_back.bind(on_release=self.bat_to_firstpage)

        # MENYUSUN FORM (Urutan yang benar agar tidak error)
        form_box.add_widget(title_label)
        form_box.add_widget(subtitle_label)
        form_box.add_widget(username_container) # Masukkan Container (Bukan Field langsung)
        form_box.add_widget(password_container) # Masukkan Container (Bukan Field langsung)
        form_box.add_widget(Widget(size_hint_y=None, height=dp(10)))
        form_box.add_widget(btn_signin)
        form_box.add_widget(btn_back)
        form_box.add_widget(footer_box)
        
        right_layout.add_widget(form_box)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def do_login(self, instance):
        username = self.username_field.text
        password = self.password_field.text

        db_path = os.path.join(MAIN_DIR, "user_data.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT,
                        username TEXT UNIQUE,
                        password TEXT
                    )
                """)
                cursor.execute("SELECT * FROM user_data WHERE username = ? AND password = ?", (username, password))
                result = cursor.fetchone()

            if result:
                nama_user = result[1]
                username_user = result[2]
                app = MDApp.get_running_app()
                app.user_nama = nama_user
                app.username = username_user
                
                if self.manager.has_screen("home_screen"):
                    self.manager.current = "home_screen"
                else:
                    self.show_snackbar("Error: Home Screen tidak ditemukan")
                self.password_field.text = ""
            else:
                self.show_snackbar("Gagal Login! Username atau Password Salah.")
        except Exception as e:
            print(f"DB Error: {e}")
            self.show_snackbar("Database Error.")

    def go_to_signup(self, instance):
        if self.manager.has_screen("signup_screen"):
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

    def bat_to_firstpage(self, instance):
        # Kembali ke Hero Screen
        if self.manager.has_screen("hero_screen"):
            self.manager.current = "hero_screen"
            self.manager.transition.direction = "right"