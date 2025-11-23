import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
# Import Widget KivyMD 2.0.0
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldTrailingIcon,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivy.uix.floatlayout import FloatLayout

# --- CLASS HALAMAN (MDScreen) ---
class SignupPage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Di dalam Screen, kita gunakan __init__, bukan build.

        # 1. Background Image
        # Saya pakai try-except agar kalau gambar tidak ada, app tidak crash (tetap jalan dengan background warna)
        
        bg_image = FitImage(
                # Gunakan r"..." (raw string) untuk path Windows agar backslash aman
            source=r"D:\Project Pemdas Octatech test\Main\Assets\Images\latar_belakang_signup.jpg",
            radius=[0, 0, 0, 0]
            )
        self.add_widget(bg_image) # Gunakan self, bukan screen
        
            # Fallback warna jika gambar gagal load
        self.md_bg_color = (0.1, 0.1, 0.1, 1)

        layout_utama = FloatLayout()

        # 2. Membuat Card
        card = MDCard(
            style="elevated",
            size_hint=(None, None),
            size=("300dp", "550dp"), # Tinggi sedikit ditambah agar muat
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_bg_color="Custom",
            md_bg_color="#106EBE",
            padding="20dp",
            radius=[30],
        )

        # 3. Konten dalam Card
        card_content = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            adaptive_height=True
        )

        # --- WIDGETS ---

        # Judul
        label_title = MDLabel(
            text="Sign Up",
            halign="center",
            font_style="Headline",
            role="medium",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
            adaptive_height=True
        )

        label_subtitle = MDLabel(
            text="Buat akunmu untuk mulai menjelajahi\nOctaTech",
            halign="center",
            font_style="Body",
            role="small",
            theme_text_color="Custom",
            text_color=(0.8, 0.8, 0.8, 1),
            adaptive_height=True
        )

        # Input Nama
        input_nama = MDTextField(
            MDTextFieldHintText(text="Nama"),
            MDTextFieldTrailingIcon(icon="account"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
        )

        # Input Username
        input_username = MDTextField(
            MDTextFieldHintText(text="Username"),
            MDTextFieldTrailingIcon(icon="at"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
            
        )

        # Input Password
        input_password = MDTextField(
            MDTextFieldHintText(text="Password"),
            MDTextFieldTrailingIcon(icon="key"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10],
            password=True
            
        )

        # Tombol Buat Akun
        btn_signup = MDButton(
            MDButtonText(
                text="Buat Akun",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            ),
            style="filled",
            pos_hint={"center_x": 0.5},
            height="40dp",
            size_hint_x=1,
        )

        # --- MENYUSUN LAYOUT ---
        card_content.add_widget(label_title)
        card_content.add_widget(label_subtitle)
        card_content.add_widget(MDLabel(text="", size_hint_y=None, height="10dp")) # Spacer
        
        card_content.add_widget(input_nama)
        card_content.add_widget(input_username)
        card_content.add_widget(input_password)
        
        card_content.add_widget(MDLabel(text="", size_hint_y=None, height="20dp")) # Spacer
        card_content.add_widget(btn_signup)

        # Tombol Kembali
        btn_back = MDButton(style="text", pos_hint={"center_x": .5})
        btn_back.add_widget(MDButtonText(text="Kembali ke Login", theme_text_color="Custom", text_color=(1,1,1,0.7)))
        btn_back.bind(on_release=self.back_to_login)
        card_content.add_widget(btn_back)

        card.add_widget(card_content)
        layout_utama.add_widget(card)
        
        # Masukkan layout utama ke dalam screen (self)
        self.add_widget(layout_utama)

    def back_to_login(self, instance):
        # Cek apakah ScreenManager ada sebelum mengaksesnya
        if self.manager:
            self.manager.current = "login_screen"
            self.manager.transition.direction = "right"
        else:
            print("Screen Manager belum dipasang, tombol diklik.")
    