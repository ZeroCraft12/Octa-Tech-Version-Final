from kivy.core.window import Window

# 1. Set Ukuran Layar
 #Window.size = (1000, 600)

from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior

# Komponen KivyMD 2.0+
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
# Tambahkan import ini
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

# Buat Class Tombol Gambar Sendiri (Lebih Stabil daripada MDIconButton untuk Logo)
class LogoButton(ButtonBehavior, Image):
    pass

# --- WARNA ---
COLOR_OCTA_BLUE = get_color_from_hex("#1A2B58") # Biru Tua Pekat
COLOR_BG_GREY = get_color_from_hex("#F5F5F5")   # Abu-abu Background
COLOR_WHITE = get_color_from_hex("#FFFFFF")     # Putih Bersih


class LogoButton(ButtonBehavior, Image):
    pass
# --- 1. HEADER BUTTON ---
class HeaderButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, icon_name, text_label, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.adaptive_width = True
        self.spacing = dp(4)
        self.padding = dp(4)
        self.callback = callback_func
        
        btn_icon = MDIconButton(
            icon=icon_name,
            theme_icon_color="Custom",
            icon_color=COLOR_WHITE,
            pos_hint={"center_x": 0.5},
            font_size="30sp", 
        )
        
        lbl_text = MDLabel(
            text=text_label,
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            font_style="Label",
            role="small",
            adaptive_height=True
        )
        self.add_widget(btn_icon)
        self.add_widget(lbl_text)
    
    def on_release(self):
        """Override on_release untuk panggil callback dengan self"""
        if self.callback:
            self.callback(self)

# --- 2. MENU CARD (FIX WARNA) ---
class MenuCard(MDCard):
    def __init__(self, icon_name, title_text, on_tap=None, **kwargs):
        super().__init__(**kwargs)
        
        # --- PERBAIKAN UTAMA ---
        # Kita JANGAN pakai style="elevated" karena itu memaksa jadi putih.
        # Kita kosongkan style atau pakai "outlined" tapi border 0 agar warna custom masuk.
        
        self.theme_bg_color = "Custom"      # Aktifkan mode custom
        self.md_bg_color = COLOR_OCTA_BLUE  # Paksa Warna Biru
        
        # Tambahan agar tetap cantik (radius & bayangan)
        self.radius = [dp(15), dp(15), dp(15), dp(15)]
        self.padding = dp(20)
        self.size_hint_y = None
        self.height = dp(160)
        self.ripple_behavior = True
        self.elevation = 2 # Tambah bayangan manual
        
        layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        # IKON PUTIH
        icon = MDIconButton(
            icon=icon_name,
            theme_icon_color="Custom",
            icon_color=COLOR_WHITE,    
            pos_hint={"center_x": 0.5},
            font_size="56sp", 
        )
        
        # TEKS PUTIH
        label = MDLabel(
            text=title_text,
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            bold=True,
            font_style="Title",
            adaptive_height=True
        )
        
        layout.add_widget(MDLabel()) # Spacer
        layout.add_widget(icon)
        layout.add_widget(label)
        layout.add_widget(MDLabel()) # Spacer
        
        self.add_widget(layout)
        
        # Bind click handler if provided
        if on_tap:
            self.bind(on_release=on_tap)

# --- HALAMAN UTAMA ---
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = COLOR_BG_GREY
        
        root_layout = MDBoxLayout(orientation='vertical')
        
        # HEADER (Biru Tua)
        header_container = MDCard(
            radius=[0, 0, dp(30), dp(30)], 
            md_bg_color=COLOR_OCTA_BLUE,
            theme_bg_color="Custom", 
            elevation=0,
            size_hint_y=None,
            height=dp(110)
        )
        
        header_content = MDBoxLayout(
            orientation='horizontal', 
            padding=[dp(20), dp(10), dp(20), dp(10)]
        )
        
        # Logo Kiri
        # Jangan gunakan adaptive_width=True di logo_box agar ukuran ikon bisa diatur eksplisit
        logo_box = MDBoxLayout(orientation='horizontal', spacing=dp(5))
        # Tetapkan ukuran eksplisit untuk ikon agar dapat diperbesar
        # --- GANTI BAGIAN LOGO_ICON DENGAN INI ---
        
        # Kita pakai LogoButton buatan sendiri agar ukuran bisa diatur bebas
        logo_icon = LogoButton(
            # Ganti backslash (\) dengan slash (/) agar tidak warning SyntaxError
            source="D:/Project Pemdas Octatech test/Main/Assets/Images/logonontext.png",
            
            # Ukuran tombol dan gambar
            size_hint=(None, None),
            size=(dp(60), dp(60)), 
            
            # Posisi
            pos_hint={"center_y": 0.5},
            
            # (Opsional) Jika ingin warna asli gambar, hapus baris color ini
            # Jika logo aslinya hitam dan mau jadi putih, biarkan ini:
            color=COLOR_WHITE 
        )
        
        # Tambahkan fungsi ketika diklik (jika perlu)
        logo_icon.on_release = lambda: print("Logo ditekan!")
        logo_text = MDLabel(
            text="Octa\nTech.",
            theme_text_color="Custom",
            text_color=COLOR_WHITE,
            bold=True,
            adaptive_size=True,
            pos_hint={"center_y": 0.5}
        )
        logo_box.add_widget(logo_icon)
        logo_box.add_widget(logo_text)
        
        # Menu Kanan
        btn_profile = HeaderButton("account-circle", "Nama", self.to_profile)
        btn_logout = HeaderButton("logout", "Log out", self.do_logout)
        
        
        right_menu = MDBoxLayout(orientation='horizontal', spacing=dp(10), adaptive_width=True)
        right_menu.add_widget(btn_profile)
        right_menu.add_widget(btn_logout)
        
        header_content.add_widget(logo_box)
        header_content.add_widget(MDLabel())
        header_content.add_widget(right_menu)
        
        header_container.add_widget(header_content)
        
        # BODY SCROLL
        scroll = ScrollView()
        
        body_content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            adaptive_height=True
        )
        
        body_content.add_widget(MDLabel(size_hint_y=None, height=dp(10)))
        
        self.lbl_hello = MDLabel(
            text="Halo, nama!",
            halign="center",
            font_style="Headline",
            role="medium",
            bold=True,
            adaptive_height=True,
            theme_text_color="Primary"
)

        lbl_desc = MDLabel(text="Selamat datang di aplikasi Octa Tech.\nSilakan pilih menu di bawah ini.", halign="center", theme_text_color="Secondary", adaptive_height=True)
        
        # GRID MENU (4 Kolom)
        menu_grid = MDGridLayout(
            cols=4,
            spacing=dp(20),
            adaptive_height=True,
            padding=[dp(10), dp(30), dp(10), dp(20)]
        )
        
        # ISI CARD (Harusnya sekarang Biru Tua)
        menu_grid.add_widget(MenuCard("checkbox-marked-circle-outline", "Rekomendasi", on_tap=self.to_rekomendasi))
        menu_grid.add_widget(MenuCard("piggy-bank-outline", "Tabungan", on_tap=self.to_savings))
        menu_grid.add_widget(MenuCard("star-outline", "Review", on_tap=self.to_review))
        menu_grid.add_widget(MenuCard("heart-outline", "Wishlist", on_tap=self.to_wishlist))
        
        body_content.add_widget(self.lbl_hello)
        body_content.add_widget(lbl_desc)
        body_content.add_widget(menu_grid)
        
        scroll.add_widget(body_content)
        
        root_layout.add_widget(header_container)
        root_layout.add_widget(scroll)
        
        self.add_widget(root_layout)

    def to_profile(self, instance):
        print(f"DEBUG: to_profile dipanggil, manager = {self.manager}")
        if self.manager:
            self.manager.current = "profile_screen"
            self.manager.transition.direction = "left"
            print("DEBUG: Navigasi ke profile_screen berhasil")
        else:
            print("DEBUG: ERROR - manager None!")
    
    def to_rekomendasi(self, instance):
        """Navigate to the recommendation screen."""
        if self.manager:
            self.manager.current = "rekomendasi_gadget"
            self.manager.transition.direction = "left"
            
    def to_review(self, instance):
        """Navigate to the review screen."""
        if self.manager:
            self.manager.current = "review_screen"
            self.manager.transition.direction = "left"

    def to_savings(self, instance):
        """Navigate to the savings screen."""
        if self.manager:
            self.manager.current = "savings_screen"
            self.manager.transition.direction = "left"
    
    def to_wishlist(self, instance):
        """Navigate to the wishlist screen."""
        if self.manager:
            self.manager.current = "wishlist_screen"
            self.manager.transition.direction = "left"

    def do_logout(self, instance):
        print("Logout...")
        MDApp.get_running_app().stop()

    def on_pre_enter(self):
       app = MDApp.get_running_app()
       if hasattr(app, "user_nama"):
        self.lbl_hello.text = f"Halo, {app.user_nama}!"


