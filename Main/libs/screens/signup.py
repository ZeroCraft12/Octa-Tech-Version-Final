import os

# Nama file database, pastikan sesuai dengan file yang digunakan aplikasi Anda
current_file_path_db = os.path.abspath(__file__)
MAIN_DIR_DB = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path_db)))
DB_NAME = os.path.join(MAIN_DIR_DB, "user_data.db")

# Inisialisasi database: buat tabel jika belum ada
def init_db():
    import sqlite3
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            conn.commit()
    except Exception as e:
        print(f"DB Init Error: {e}")

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
import sqlite3
from kivy.metrics import dp 
# Import Widget KivyMD 2.0.0
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldTrailingIcon,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.text import LabelBase
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



# --- CLASS HALAMAN (MDScreen) ---
class SignupPage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Main Layout
        main_layout = MDBoxLayout(orientation='horizontal')
        
        # --- LEFT SIDE (BRANDING) ---
        # Reuse text/images or change slightly for variety
        # Path Correction
        current_file_path = os.path.abspath(__file__)
        MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        IMG_DIR = os.path.join(MAIN_DIR, "assets", "Images")

        left_layout = MDFloatLayout(
            size_hint_x=0.45
        )
        
        # Use specific signup BG
        bg_path = os.path.join(IMG_DIR, "bg2.jpg") 
        if os.path.exists(bg_path):
            bg_image = FitImage(source=bg_path)
            left_layout.add_widget(bg_image)
            


        branding_box = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing="16dp",
            padding="40dp"
        )
        
        tagline = MDLabel(
            text="Join Octa Tech\nCommunity",
            halign="center",
            font_style="Headline",
            role="medium",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            adaptive_height=True
        )
        branding_box.add_widget(tagline)
        
        sub_tagline = MDLabel(
            text="Dapatkan rekomendasi gadget terbaik dan diskusikan dengan pengguna lain.",
            halign="center",
            font_style="Body",
            font_name="Popins-Bold",
            role="medium",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            adaptive_height=True
        )
        branding_box.add_widget(sub_tagline)
        left_layout.add_widget(branding_box)


        # --- RIGHT SIDE (FORM) ---
        right_layout = MDFloatLayout(
            size_hint_x=0.55,
            md_bg_color=(1, 1, 1, 1) # White clean background
        )
        
        form_container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            pos_hint={"center_x": .5, "center_y": .5},
            padding="60dp",
            spacing="20dp",
            size_hint_x=0.8
        )

        # Header
        header_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="8dp")
        title_label = MDLabel(
            text="Buat akun",
            font_name="Popins-Bold",
            font_style="Display",
            role="small",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.17, 0.35, 1),
            adaptive_height=True
        )
        subtitle_label = MDLabel(
            text="Lengkapi data diri untuk mendaftar.",
            font_style="Body",
            font_name="Popins-Bold",
            role="large",
            theme_text_color="Secondary",
            adaptive_height=True
        )
        header_box.add_widget(title_label)
        header_box.add_widget(subtitle_label)
        form_container.add_widget(header_box)

        # Inputs
        self.input_nama = MDTextField(
            MDTextFieldHintText(text="Nama Lengkap",font_name="Popins-Bold"),
            mode="outlined",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color_normal=(0.2, 0.2, 0.2, 1),
        )
        form_container.add_widget(self.input_nama)

        self.input_username = MDTextField(
            MDTextFieldHintText(text="Username",font_name="Popins-Bold"),
            mode="outlined",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color_normal=(0.2, 0.2, 0.2, 1),
        )
        form_container.add_widget(self.input_username)

        self.input_password = MDTextField(
            MDTextFieldHintText(text="Password",font_name="Popins-Bold"),
            mode="outlined",
            size_hint_x=1,
            password=True,
            theme_text_color="Custom",
            text_color_normal=(0.2, 0.2, 0.2, 1),
        )
        form_container.add_widget(self.input_password)

        # Buttons
        button_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="16dp")
        
        btn_signup = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.31, 0.27, 0.9, 1),
            size_hint_x=1,
            height="54dp",
            radius=[12]
        )
        btn_signup.bind(on_release=self.do_signup)
        btn_signup.add_widget(MDButtonText(
            text="Sign Up",
            font_name="Popins",
            pos_hint={"center_x": .5, "center_y": .5},
            bold=True,
            theme_text_color="Custom",
            text_color=(1,1,1,1)
        ))
        button_box.add_widget(btn_signup)
        
        # Footer
        footer_box = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True, 
            spacing="6dp",
            pos_hint={"center_x": .5}
        )
        footer_box.add_widget(MDLabel(
            text="Sudah punya akun?",
            adaptive_width=True,
            theme_text_color="Secondary",
            font_style="Body",
            role="medium"
        ))
        
        btn_login = MDButton(style="text")
        btn_login.bind(on_release=self.back_to_login)
        btn_login.add_widget(MDButtonText(
            text="Login Sekarang",
            theme_text_color="Custom",
            text_color=(0.31, 0.27, 0.9, 1),
            bold=True
        ))
        footer_box.add_widget(btn_login)
        button_box.add_widget(footer_box)

        form_container.add_widget(button_box)
        right_layout.add_widget(form_container)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        
        self.add_widget(main_layout)
    

    def do_signup(self, instance):
        # LOGIKA DB ADA DI SINI SEKARANG
        nama = self.input_nama.text
        username = self.input_username.text
        password = self.input_password.text

        if not username or not password:
            self.show_snackbar("Isi semua kolom!")
            return

        try:
            # Buka koneksi lokal di fungsi ini
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_data (nama,username, password) VALUES (?,?,?)", (nama,username, password))
                conn.commit()
            
            self.show_snackbar("Sukses! Silakan Login.")
            # Reset field
            self.input_username.text = ""
            self.input_password.text = ""
            # Pindah screen
            self.manager.current = "login_screen"
            
        except sqlite3.IntegrityError:
            self.show_snackbar("Username sudah ada!")

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def back_to_login(self, instance):
        # Cek apakah ScreenManager ada sebelum mengaksesnya
        if self.manager:
            self.manager.current = "login_screen"
            self.manager.transition.direction = "right"
        else:
            print("Screen Manager belum dipasang, tombol diklik.")
    def show_snackbar(self, text):
        snackbar = MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        snackbar.open()
    