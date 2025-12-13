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
        
        # 1. Main Layout (Split Screen)
        main_layout = MDBoxLayout(orientation='horizontal')
        
        # --- LEFT SIDE (BRANDING) ---
        # 40% Width for Desktop Feel
        left_layout = MDFloatLayout(
            size_hint_x=0.45,
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Background Image with Overlay
        bg_path = os.path.join(IMG_DIR, "bg1.jpg")
        if os.path.exists(bg_path):
            bg_image = FitImage(source=bg_path)
            left_layout.add_widget(bg_image)
            


        # Branding Content
        branding_box = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing="16dp",
            padding="40dp"
        )
        
        logo_path = os.path.join(IMG_DIR, "LogoText.png")
        if os.path.exists(logo_path):
            logo = Image(
                source=logo_path,
                size_hint=(None, None),
                size=(dp(500), dp(500)),
                pos_hint={'center_x': 0.5}
            )
            branding_box.add_widget(logo)

        tagline = MDLabel(
            text="Recommended Gadget\nfor Student",
            halign="center",
            font_style="Headline",
            role="medium",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.17, 0.35, 1),
            adaptive_height=True
        )
        branding_box.add_widget(tagline)
        
        sub_tagline = MDLabel(
            text="Temukan laptop impianmu dengan mudah dan cepat bersama Octa Tech.",
            font_name="Poppins-Bold",
            halign="center",
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=(0.1, 0.17, 0.35, 1),
            adaptive_height=True
        )
        branding_box.add_widget(sub_tagline)
        
        left_layout.add_widget(branding_box)


        # --- RIGHT SIDE (FORM) ---
        right_layout = MDFloatLayout(
            size_hint_x=0.55,
            md_bg_color=(1, 1, 1, 1) # White clean background
        )
        
        # Scrollable Form Container (for smaller screens protection)
        form_container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            pos_hint={"center_x": .5, "center_y": .5},
            padding="60dp",
            spacing="24dp",
            size_hint_x=0.8
        )
        
        # 1. Header Text
        header_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="8dp")
        welcome_label = MDLabel(
            text="Welcome Back!",
            font_name="Poppins-Bold",
            font_style="Display",
            role="small",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.17, 0.35, 1), # Navy
            adaptive_height=True
        )
        subtitle_label = MDLabel(
            text="Masukkan detail akun kamu untuk login.",
            font_name="Poppins",
            font_style="Body",
            role="large",
            theme_text_color="Secondary",
            adaptive_height=True
        )
        header_box.add_widget(welcome_label)
        header_box.add_widget(subtitle_label)
        form_container.add_widget(header_box)

        # 2. Inputs
        self.username_field = MDTextField(
            MDTextFieldHintText(text="Username"),
            mode="outlined",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color_normal=(0.2, 0.2, 0.2, 1),
        )
        form_container.add_widget(self.username_field)

        self.password_field = MDTextField(
            MDTextFieldHintText(text="Password"),
            mode="outlined",
            size_hint_x=1,
            password=True
        )
        form_container.add_widget(self.password_field)

        # 3. Actions (Forgot Password? etc - Placeholder)
        
        # 4. Buttons
        button_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="16dp")
        
        btn_signin = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.31, 0.27, 0.9, 1), # Indigo #4F46E5
            size_hint_x=1,
            height="54dp",
            radius=[12]
        )
        btn_signin.bind(on_release=self.do_login)
        btn_signin.add_widget(MDButtonText(
            text="Sign In",
            pos_hint={"center_x": .5, "center_y": .5},
            bold=True,
            theme_text_color="Custom",
            text_color=(1,1,1,1)
        ))
        button_box.add_widget(btn_signin)
        
        # 5. Footer (Sign Up Link)
        footer_box = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True, 
            spacing="6dp",
            pos_hint={"center_x": .5}
        )
        footer_box.add_widget(MDLabel(
            text="Belum punya akun?",
            adaptive_width=True,
            theme_text_color="Secondary",
            font_style="Body",
            role="medium"
        ))
        
        btn_signup = MDButton(style="text")
        btn_signup.bind(on_release=self.go_to_signup)
        btn_signup.add_widget(MDButtonText(
            text="Daftar Sekarang",
            theme_text_color="Custom",
            text_color=(0.31, 0.27, 0.9, 1),
            bold=True
        ))
        footer_box.add_widget(btn_signup)
        button_box.add_widget(footer_box)
        
        form_container.add_widget(button_box)

        # Add form to right layout
        right_layout.add_widget(form_container)

        # Add navigation back (Corner)
        btn_back = MDButton(
            style="text",
            pos_hint={"top": 0.95, "right": 0.95},
        )
        btn_back.bind(on_release=self.bat_to_firstpage)
        btn_back.add_widget(MDButtonText(text="Kembali", theme_text_color="Secondary"))
        right_layout.add_widget(btn_back)

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