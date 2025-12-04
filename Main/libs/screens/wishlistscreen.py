import json
import os
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
# [PERBAIKAN] Import MDWidget ditambahkan di sini
from kivymd.uix.widget import MDWidget
from kivy.uix.image import Image

# --- KONFIGURASI WARNA ---
COLOR_BG_CARD = get_color_from_hex("#D0D3F0") # Ungu muda pucat
COLOR_TEXT_PRIMARY = get_color_from_hex("#000000")

# ==========================================
# WISHLIST MANAGER (LOGIC)
# ==========================================
class WishlistManager:
    def __init__(self, filename="wishlist_data.json"):
        self.filename = filename
        self.wishlist = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return []

    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.wishlist, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan wishlist: {e}")

    def add_item(self, item_data):
        # Cek duplikasi
        for item in self.wishlist:
            if item.get("Nama") == item_data.get("Nama"):
                return False 
        
        self.wishlist.append(item_data)
        self.save_data()
        return True

    def remove_item(self, index):
        if 0 <= index < len(self.wishlist):
            del self.wishlist[index]
            self.save_data()

    def get_items(self):
        return self.wishlist

wishlist_manager = WishlistManager()

# ==========================================
# CUSTOM CARD COMPONENT
# ==========================================
class WishlistCard(MDCard):
    def __init__(self, index, item_data, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = (dp(160), dp(220)) # Ukuran Card
        self.radius = [dp(12), dp(12), dp(12), dp(12)]
        self.md_bg_color = COLOR_BG_CARD
        self.theme_bg_color = "Custom"
        self.padding = dp(8)
        self.spacing = dp(5)
        self.elevation = 1

        # 1. Gambar
        img_source = item_data.get("Image", "assets/images/laptop_placeholder.png")
        # Validasi path gambar
        if not img_source or (not os.path.exists(img_source) and "http" not in img_source):
             img_source = "assets/images/laptop_default.png" # Pastikan file ini ada atau ganti nama file

        img_box = MDBoxLayout(
            size_hint_y=0.6, 
            md_bg_color=[1,1,1,1], 
            radius=[dp(8), dp(8), dp(8), dp(8)]
        )
        
        self.image = Image(source=img_source, keep_ratio=True, allow_stretch=True)
        img_box.add_widget(self.image)
        
        # 2. Nama Produk
        lbl_name = MDLabel(
            text=f"{item_data.get('Brand','')} {item_data.get('Nama','')}"[:30],
            font_style="Label",
            role="large",
            bold=True,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
            halign="left"
        )

        # 3. Harga & Tombol Hapus
        bottom_box = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        
        lbl_price = MDLabel(
            text=f"Rp {item_data.get('Harga', '0')}",
            font_style="Label",
            role="medium",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
            pos_hint={"center_y": 0.5}
        )

        btn_delete = MDIconButton(
            icon="trash-can-outline",
            style="standard",
            theme_icon_color="Error",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: delete_callback(index)
        )

        bottom_box.add_widget(lbl_price)
        bottom_box.add_widget(btn_delete)

        self.add_widget(img_box)
        self.add_widget(lbl_name)
        self.add_widget(MDWidget()) # Spacer vertical (Sekarang sudah aman karena sudah di-import)
        self.add_widget(bottom_box)

# ==========================================
# UI LAYOUT (KV)
# ==========================================
WISHLIST_KV = '''
<WishlistScreen>:
    name: "wishlist_screen"
    md_bg_color: [0.95, 0.95, 0.95, 1] 

    MDBoxLayout:
        orientation: 'vertical'
        
        # HEADER
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "70dp"
            padding: [20, 10]
            spacing: "10dp"
            md_bg_color: [0.95, 0.95, 0.95, 1]

            MDIconButton:
                icon: "arrow-left"
                pos_hint: {"center_y": .5}
                on_release: app.root.current = "home_screen"

            MDBoxLayout:
                orientation: 'vertical'
                pos_hint: {"center_y": .5}
                adaptive_height: True
                MDLabel:
                    text: "Octa Tech."
                    font_style: "Title"
                    bold: True
                    role: "large"
                    adaptive_height: True
            
            MDWidget: 

            MDLabel:
                text: "Wishlist Kerenn"
                halign: "center"
                font_style: "Headline"
                role: "small"
                bold: True
                pos_hint: {"center_y": .5}
                adaptive_width: True

            MDWidget: 

            MDIconButton:
                icon: "filter-variant"
                pos_hint: {"center_y": .5}
            
            MDIconButton:
                icon: "sort"
                pos_hint: {"center_y": .5}

        # CONTENT GRID
        MDScrollView:
            do_scroll_x: False
            do_scroll_y: True
            
            MDGridLayout:
                id: grid_wishlist
                cols: 2
                spacing: "15dp"
                padding: "20dp"
                adaptive_height: True
                row_default_height: "240dp"
                row_force_default: False 
'''

# Load String KV Global
Builder.load_string(WISHLIST_KV)

class WishlistScreen(MDScreen):
    def on_enter(self):
        self.refresh_list()

    def refresh_list(self):
        grid = self.ids.grid_wishlist
        grid.clear_widgets()
        
        items = wishlist_manager.get_items()

        if not items:
            lbl = MDLabel(
                text="Belum ada item di wishlist", 
                halign="center", 
                pos_hint={"center_y":0.5},
                adaptive_height=True
            )
            # Trik spacer agar label di tengah
            temp_box = MDBoxLayout(size_hint_y=None, height=dp(100))
            temp_box.add_widget(lbl)
            
            grid.cols = 1
            grid.add_widget(temp_box)
        else:
            grid.cols = 2 
            for i, item in enumerate(items):
                card = WishlistCard(i, item, self.delete_item)
                grid.add_widget(card)

    def delete_item(self, index):
        wishlist_manager.remove_item(index)
        self.refresh_list()