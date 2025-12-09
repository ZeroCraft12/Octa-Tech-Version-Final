import json
import os
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.widget import MDWidget
from kivymd.uix.fitimage import FitImage 

# --- KONFIGURASI WARNA ---
COLOR_BG_CARD = get_color_from_hex("#FFFFFF")
COLOR_TEXT_PRIMARY = get_color_from_hex("#000000")

# ==========================================
# WISHLIST MANAGER
# ==========================================
class WishlistManager:
    def __init__(self, filename="wishlist_data.json"):
        self.filename = filename
        self.wishlist = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename): return []
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except: return []

    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.wishlist, f, indent=4)
        except Exception as e: print(f"Gagal save: {e}")

    def add_item(self, item_data):
        target_id = item_data.get("id")
        for item in self.wishlist:
            if target_id and item.get("id") == target_id: return False
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
# CUSTOM CARD (BISA DIKLIK)
# ==========================================
class WishlistCard(MDCard):
    def __init__(self, index, item_data, delete_callback, view_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, None) # Full width kolom
        self.height = dp(210)
        self.radius = [dp(8)]
        self.md_bg_color = COLOR_BG_CARD
        self.elevation = 1
        self.padding = dp(0)
        self.spacing = dp(0)
        
        # [PENTING] Aktifkan Ripple agar user tau bisa diklik
        self.ripple_behavior = True
        # Saat kartu diklik -> Panggil fungsi lihat detail
        self.on_release = lambda: view_callback(item_data)

        # --- 1. GAMBAR ---
        img_source = item_data.get("image", "")
        if not img_source or not os.path.exists(img_source):
             img_source = "assets/images/laptop_default.png"

        img_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(110), 
            radius=[dp(8), dp(8), 0, 0]
        )
        self.image = FitImage(source=img_source, radius=[dp(8), dp(8), 0, 0])
        img_box.add_widget(self.image)
        
        # --- 2. TEKS ---
        content_box = MDBoxLayout(
            orientation="vertical",
            padding=[dp(6), dp(6), dp(6), dp(4)],
            spacing=dp(2)
        )

        lbl_name = MDLabel(
            text=item_data.get("name", "Tanpa Nama"),
            font_style="Label", role="medium", bold=True,
            adaptive_height=True, max_lines=2, shorten=True,
            halign="left", font_size="12sp"
        )

        display_price = item_data.get("price_text", "Rp 0")
        lbl_price = MDLabel(
            text=display_price,
            font_style="Label", role="small",
            theme_text_color="Custom", text_color=[0.2, 0.6, 0.2, 1],
            adaptive_height=True, font_size="11sp"
        )

        # --- 3. TOMBOL HAPUS ---
        action_box = MDBoxLayout(adaptive_height=True)
        action_box.add_widget(MDWidget()) 
        
        btn_delete = MDIconButton(
            icon="trash-can",
            style="standard",
            theme_icon_color="Custom",
            icon_color=[1, 0, 0, 1],
            font_size=dp(20),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={"center_y": .5},
        )
        # [PENTING] Binding manual agar tidak bentrok dengan klik kartu
        btn_delete.bind(on_release=lambda x: delete_callback(index))
        
        action_box.add_widget(btn_delete)

        content_box.add_widget(lbl_name)
        content_box.add_widget(lbl_price)
        content_box.add_widget(MDWidget())
        content_box.add_widget(action_box)

        self.add_widget(img_box)
        self.add_widget(content_box)

# ==========================================
# UI LAYOUT
# ==========================================
WISHLIST_KV = '''
<WishlistScreen>:
    name: "wishlist_screen"
    md_bg_color: [0.96, 0.96, 0.96, 1] 

    MDBoxLayout:
        orientation: 'vertical'
        
        # HEADER
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "64dp"
            padding: [10, 0]
            spacing: "10dp"
            md_bg_color: [0.1, 0.17, 0.35, 1]

            MDIconButton:
                icon: "arrow-left"
                theme_icon_color: "Custom"
                icon_color: [1, 1, 1, 1]
                pos_hint: {"center_y": .5}
                on_release: app.root.current = "home_screen"

            MDLabel:
                text: "Wishlist Saya"
                font_style: "Title"
                bold: True
                role: "large"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]
                pos_hint: {"center_y": .5}

        # GRID CONTENT
        MDScrollView:
            do_scroll_x: False
            do_scroll_y: True
            bar_width: 0
            
            MDGridLayout:
                id: grid_wishlist
                cols: 3
                spacing: "8dp"
                padding: "8dp"
                adaptive_height: True
                size_hint_y: None
'''

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
                text="Wishlist Kosong", 
                halign="center", pos_hint={"center_y":0.5},
                adaptive_height=True
            )
            temp = MDBoxLayout(size_hint_y=None, height=dp(300)); temp.add_widget(lbl)
            grid.cols = 1; grid.add_widget(temp)
        else:
            grid.cols = 3 
            for i, item in enumerate(items):
                # Pass 2 fungsi: delete_item DAN view_item
                card = WishlistCard(i, item, self.delete_item, self.view_item)
                grid.add_widget(card)

    def delete_item(self, index):
        # Fungsi Hapus (Hanya dipanggil tombol sampah)
        wishlist_manager.remove_item(index)
        self.refresh_list()

    def view_item(self, item_data):
        # Fungsi Lihat Detail (Dipanggil saat kartu diklik)
        app = MDApp.get_running_app()
        
        # 1. Pindah screen ke Rekomendasi Gadget
        app.root.current = "rekomendasi_gadget"
        
        # 2. Akses screen rekomendasi dan panggil fungsi tampilkan detail
        # Pastikan nama screen di main.py adalah 'rekomendasi_gadget'
        rekomen_screen = app.root.get_screen("rekomendasi_gadget")
        
        # 3. Panggil method baru yang kita buat di Langkah 1
        rekomen_screen.show_detail_from_wishlist(item_data)