from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
# Import Widget Baru untuk KivyMD 2.0.0
from kivymd.uix.textfield import (
    MDTextField, 
    MDTextFieldHintText, 
    MDTextFieldTrailingIcon, 
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp

# Mengatur ukuran window agar mirip tampilan mobile
Window.size = (1000, 600)

class SignupPage(MDApp):
    def build(self):
        # 1. Tema Dasar
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        screen = MDScreen()

        # 2. Background Image
        # Pastikan ada file gambar atau hapus baris ini jika error gambar
        bg_image = FitImage(
            source="D:\Project Pemdas Octatech test\Assets\Sigup.py\latar.jpg",
            radius=[0, 0, 0, 0]
            
            ) 
        screen.add_widget(bg_image) 
        
        # Jika tidak ada gambar, kita beri warna background gelap manual agar terlihat
        screen.md_bg_color = (0.1, 0.1, 0.1, 1) 

        layout_utama = FloatLayout()

        # 3. Membuat Card
        card = MDCard(
            style="elevated",
            size_hint=(None, None),
            size=("300dp", "500dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(13/255, 23/255, 42/255, 1), # Warna Biru Gelap Hex #0D172A
            padding="20dp",
            radius=[30],
        )

        # 4. Konten dalam Card
        card_content = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            adaptive_height=True
        )

        # --- WIDGETS (Syntax KivyMD 2.0) ---

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

        # Input Nama (Struktur Baru)
        input_nama = MDTextField(
            MDTextFieldHintText(text="Nama"),
            MDTextFieldTrailingIcon(icon="account"),
            mode="outlined",
        )

        # Input Username
        input_username = MDTextField(
            MDTextFieldHintText(text="Username"),
            MDTextFieldTrailingIcon(icon="at"),
            mode="outlined",
        )

        # Input Password
        input_password = MDTextField(
            MDTextFieldHintText(text="Password"),
            MDTextFieldTrailingIcon(icon="eye-off"),
            mode="outlined",
            password=True # (Fitur password native mungkin berbeda di 2.0 dev, 
            # biasanya perlu logic tambahan untuk masking, tapi kita biarkan default dulu)
        )

        # Tombol Buat Akun (Struktur Baru: MDButton)
        # style="filled" memberikan warna solid sesuai primary color
        btn_signup = MDButton(
            MDButtonText(
                text="Buat Akun",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1), # Teks putih
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            ),
            style="filled",
            pos_hint={"center_x": 0.5},
            height="40dp",
            size_hint_x=1, # Lebar penuh
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

        card.add_widget(card_content)
        layout_utama.add_widget(card)
        screen.add_widget(layout_utama)

        return screen

if __name__ == "__main__":
    SignupPage().run()