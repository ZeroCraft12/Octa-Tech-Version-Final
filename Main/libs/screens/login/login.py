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

# Mengatur ukuran window
Window.size = (1000, 600)

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
            source= "D:\Project Pemdas Octatech test\Assets\loginpage\Latarbelakang.jpg",
            radius=[0, 0, 0, 0]
        )

        logo = Image(
            source = "D:\Project Pemdas Octatech test\Assets\loginpage\LogoText.png",
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
            text_color=(0.1, 0.1, 0.1, 1)
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
            text_color=(1, 1, 1, 1)
        )
        
        subtitle_label = MDLabel(
            text="Masukkan username dan password untuk melanjutkan",
            font_style="Body",
            role="small",
            halign="left",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            size_hint_y=None
        )
        subtitle_label.height = subtitle_label.texture_size[1] # Trik agar tinggi label pas

        # Input Username
        username_field = MDTextField(
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
        )
        username_hint = MDTextFieldHintText(
            text="Username",
            text_color_normal=(0.5, 0.5, 0.5, 1)
        )
        username_field.add_widget(username_hint)

        # Input Password
        password_field = MDTextField(
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
            # password=True # (Opsional: tambahkan ini jika ingin bintang-bintang)
        )
        password_hint = MDTextFieldHintText(
            text="Password",
            text_color_normal=(0.5, 0.5, 0.5, 1)
        )
        password_field.add_widget(password_hint)

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
        btn_signin.bind(on_release=self.login_action) # Hubungkan ke fungsi
        
        btn_text = MDButtonText(
            text="Sign In",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": .5, "center_y": .5},
            font_style="Title",
            role="medium"
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
            halign="right",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.8, 1),
            font_style="Body",
            role="small"
        )
        
        # Tombol Sign Up (Text Button)
        btn_signup = MDButton(style="text")
        btn_signup_text = MDButtonText(
            text="Sign Up",
            theme_text_color="Custom",
            pos_hint={"center_x": .5, "center_y": .5},
            text_color=(1, 0.8, 0, 1),
            bold=True
        )
        btn_signup.add_widget(btn_signup_text)
        btn_signup.bind(on_release = self.go_to_signup)
        
        footer_box.add_widget(footer_label)
        footer_box.add_widget(btn_signup)

        # Menyusun Bagian Kanan
        form_box.add_widget(title_label)
        form_box.add_widget(subtitle_label)
        form_box.add_widget(username_field)
        form_box.add_widget(password_field)
        form_box.add_widget(Widget(size_hint_y=None, height=dp(10))) # Spacer
        form_box.add_widget(btn_signin)
        form_box.add_widget(footer_box)
        
        right_layout.add_widget(form_box)

        # Gabungkan Kiri dan Kanan ke Layout Utama
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Masukkan Layout Utama ke Screen
    def go_to_signup(self, instance):
        # Fungsi untuk pindah layar
        self.manager.current = "signup_screen"
        self.manager.transition.direction = "left"    
        
        

    def login_action(self, instance):
        print("Login button pressed!")

