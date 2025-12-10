import os
import pandas as pd
import re
import webbrowser
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import MDWidget
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

# ==========================================
# 1. DATA HANDLER
# ==========================================
class GadgetDataManager:
    def __init__(self, csv_path=None):
        self.df = pd.DataFrame()
        target_filename = 'database(Laptop).csv'
        
        possible_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), target_filename),
            os.path.join(os.getcwd(), target_filename),
            os.path.join(os.getcwd(), 'Main', 'libs', 'screens', target_filename)
        ]
        if csv_path: possible_paths.insert(0, csv_path)

        self.final_path = None
        for path in possible_paths:
            if os.path.exists(path):
                self.final_path = path
                break

        if self.final_path:
            try:
                self.df = pd.read_csv(self.final_path, sep=';')
                self.df.columns = self.df.columns.str.strip()
                if 'Image 3' in self.df.columns:
                    self.df.rename(columns={'Image 3': 'Image3'}, inplace=True)

                if 'Harga' in self.df.columns:
                    self.df['CleanPrice'] = self.df['Harga'].apply(self._clean_price)
                if 'RAM' in self.df.columns:
                    self.df['CleanRAM'] = self.df['RAM'].apply(self._clean_ram)
                if 'Storage' in self.df.columns:
                    self.df['CleanStorage'] = self.df['Storage'].apply(self._clean_storage)
                
                print(f"DEBUG: Sukses load {len(self.df)} produk.")
            except Exception as e:
                print(f"DEBUG: Error baca CSV: {e}")
        else:
            print("DEBUG: CSV FILE TIDAK DITEMUKAN.")

    def _clean_price(self, price_str):
        try:
            return int(str(price_str).replace('Rp', '').replace('.', '').replace('++', '').split('-')[0].strip())
        except: return 0

    def _clean_ram(self, ram_str):
        try:
            match = re.search(r'(\d+)\s*GB', str(ram_str), re.IGNORECASE)
            return int(match.group(1)) if match else 0
        except: return 0

    def _clean_storage(self, storage_str):
        try:
            s = str(storage_str).upper()
            if 'TB' in s:
                return int(re.search(r'(\d+)\s*TB', s).group(1)) * 1024
            elif 'GB' in s:
                return int(re.search(r'(\d+)\s*GB', s).group(1))
            return 0
        except: return 0

    def filter_laptops(self, budget_range=None, cpu_type=None, ram_size=None, storage_size=None):
        if self.df.empty: return self.df
        filtered = self.df.copy()
        
        if budget_range:
            min_b, max_b = budget_range
            filtered = filtered[(filtered['CleanPrice'] >= min_b) & (filtered['CleanPrice'] <= max_b)]
        if cpu_type and cpu_type != "Semua":
            filtered = filtered[filtered['CPU'].str.contains(cpu_type, case=False, na=False)]
        if ram_size and ram_size != "Semua":
            try:
                user_ram = int(str(ram_size).replace("GB", "").strip())
                filtered = filtered[filtered['CleanRAM'] >= user_ram]
            except: pass
        if storage_size and storage_size != "Semua":
            try:
                user_s = int(str(storage_size).replace("GB", "").replace("TB", "").strip())
                if "TB" in storage_size: user_s *= 1024
                filtered = filtered[filtered['CleanStorage'] >= user_s]
            except: pass
        return filtered

# ==========================================
# 2. KV LAYOUT
# ==========================================

KV = '''
#:import hex kivy.utils.get_color_from_hex

<NavHeader@MDBoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    height: "100dp"
    md_bg_color: hex("#4F46E5")
    padding: ["24dp", "24dp", "24dp", "24dp"]
    spacing: "12dp"
    radius: [0, 0, 24, 24]
    
    MDIconButton:
        icon: "home"
        theme_icon_color: "Custom"
        icon_color: 1, 1, 1, 1
        pos_hint: {"center_y": .6}
        on_release: app.root.get_screen("rekomendasi_gadget").go_to_home() 
        style: "standard"

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        pos_hint: {"center_y": .6}
        MDLabel:
            text: "Panduan Rekomendasi"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Title"
            role: "medium"
            adaptive_height: True
        MDLabel:
            text: "Temukan gadget impianmu sesuai kebutuhan"
            halign: "center"
            theme_text_color: "Custom"
            text_color: hex("#E0E7FF")
            font_style: "Body"
            role: "small"
            adaptive_height: True

    MDIconButton:
        icon: "refresh"
        theme_icon_color: "Custom"
        icon_color: 1, 1, 1, 1
        pos_hint: {"center_y": .6}
        on_release: app.root.get_screen("rekomendasi_gadget").restart_flow()
        style: "standard"

# New Component for Options
<OptionCard@MDCard>:
    orientation: "horizontal"
    size_hint_y: None
    height: "72dp"
    radius: [12]
    padding: "16dp"
    spacing: "16dp"
    style: "elevated"
    md_bg_color: 1, 1, 1, 1
    elevation: 1
    ripple_behavior: True
    
    MDIcon:
        icon: root.icon_name if hasattr(root, 'icon_name') else "checkbox-blank-circle-outline"
        theme_text_color: "Custom"
        text_color: hex("#4F46E5")
        pos_hint: {"center_y": .5}
        
    MDLabel:
        text: root.text_option if hasattr(root, 'text_option') else ""
        font_style: "Title"
        role: "small"
        pos_hint: {"center_y": .5}

<GridCardItem>:
    orientation: "horizontal"
    size_hint_y: None
    height: "140dp"
    padding: "12dp"
    spacing: "16dp"
    radius: [16]
    elevation: 2
    style: "elevated"
    md_bg_color: 1, 1, 1, 1
    ripple_behavior: True
    shadow_softness: 2
    shadow_offset: (0, 2)
    
    FitImage:
        source: root.source
        size_hint: (None, 1)
        width: self.height
        radius: [12]
        
    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"center_y": .5}
        adaptive_height: True
        spacing: "4dp"
        
        MDLabel:
            text: root.product_name
            font_style: "Title"
            role: "medium"
            bold: True
            adaptive_height: True
            max_lines: 2
            shorten: True
            shorten_from: "right"
            theme_text_color: "Custom"
            text_color: hex("#111827")
            
        MDLabel:
            text: root.cpu_info
            font_style: "Body"
            role: "small"
            theme_text_color: "Secondary"
            max_lines: 2
            shorten: True
            adaptive_height: True

        MDLabel:
            text: root.price
            font_style: "Title"
            role: "medium"
            theme_text_color: "Custom"
            text_color: hex("#16A34A") # Green
            bold: True
            adaptive_height: True
            padding: [0, "8dp", 0, 0]

<GadgetStepScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: hex("#F9FAFB")
        
        NavHeader:
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: ["24dp", "32dp", "24dp", "24dp"]
            spacing: "24dp"
            
            MDLabel:
                id: question_label
                text: "Pertanyaan?"
                halign: "center"
                font_style: "Headline"
                role: "medium"
                bold: True
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: hex("#1F2937")

            MDScrollView:
                bar_width: 0
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    MDGridLayout:
                        id: options_grid
                        cols: 1
                        spacing: "16dp"
                        adaptive_height: True

            MDAnchorLayout:
                anchor_x: "right"
                size_hint_y: None
                height: "60dp"
                MDButton:
                    style: "text"
                    on_release: root.controller.next_step(skip=True)
                    MDButtonText:
                        text: "LEWATI >>"
                        theme_text_color: "Custom"
                        text_color: hex("#6B7280")

<GadgetResultScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: hex("#F3F4F6")
        NavHeader:
        
        MDBoxLayout:
            orientation: 'vertical'
            
            MDBoxLayout:
                adaptive_height: True
                padding: ["24dp", "16dp"]
                spacing: "12dp"
                md_bg_color: hex("#FFFFFF")
                elevation: 0
                
                MDLabel:
                    text: "Hasil Rekomendasi"
                    font_style: "Title"
                    role: "large"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: hex("#1F2937")
                    pos_hint: {"center_y": .5}
                    
                MDWidget:
                
                # Sort Buttons styled as Chips
                MDButton:
                    style: "tonal"
                    height: "32dp"
                    on_release: root.controller.apply_sort("price_asc")
                    radius: [8]
                    theme_bg_color: "Custom"
                    md_bg_color: hex("#EEF2FF")
                    MDButtonText:
                        text: "Termurah"
                        theme_text_color: "Custom"
                        text_color: hex("#4F46E5")
                        font_style: "Label"
                        role: "large"
                        
                MDButton:
                    style: "tonal"
                    height: "32dp"
                    on_release: root.controller.apply_sort("price_desc")
                    radius: [8]
                    theme_bg_color: "Custom"
                    md_bg_color: hex("#EEF2FF")
                    MDButtonText:
                        text: "Termahal"
                        theme_text_color: "Custom"
                        text_color: hex("#4F46E5")
                        font_style: "Label"
                        role: "large"

            MDScrollView:
                do_scroll_x: False
                bar_width: "6dp"
                MDGridLayout:
                    id: result_grid
                    cols: 1
                    spacing: "16dp"
                    padding: ["24dp", "16dp"]
                    adaptive_height: True
                    size_hint_y: None

            MDAnchorLayout:
                anchor_x: "center"
                size_hint_y: None
                height: "80dp"
                padding: "16dp"
                MDButton:
                    style: "filled"
                    theme_bg_color: "Custom"
                    md_bg_color: hex("#111827")
                    on_release: root.controller.restart_flow()
                    size_hint_x: 1
                    MDButtonText:
                        text: "Cari Ulang"
                        pos_hint: {"center_x": .5, "center_y": .5}

<GadgetDetailScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: hex("#F9FAFB")
        
        NavHeader:
        
        MDScrollView:
            bar_width: "8dp"
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                
                # 1. HERO IMAGE COMPONENT
                MDBoxLayout:
                    size_hint_y: None
                    height: "300dp"
                    md_bg_color: [1, 1, 1, 1]
                    padding: "24dp"
                    
                    MDScrollView:
                        do_scroll_x: True
                        do_scroll_y: False
                        bar_width: 0
                        
                        MDBoxLayout:
                            id: image_gallery_box 
                            orientation: 'horizontal'
                            adaptive_width: True
                            spacing: "16dp"

                # 2. PRODUCT TITLE & ACTION
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: ["24dp", "24dp", "24dp", "8dp"]
                    spacing: "8dp"
                    md_bg_color: hex("#FFFFFF")
                    radius: [0, 0, 24, 24]
                    elevation: 1
                    
                    MDBoxLayout:
                        adaptive_height: True
                        spacing: "12dp"
                        MDLabel:
                            id: detail_name
                            text: "Nama Laptop"
                            font_style: "Headline"
                            role: "medium"
                            bold: True
                            adaptive_height: True
                            theme_text_color: "Custom"
                            text_color: hex("#111827")
                        
                        MDIconButton:
                            icon: "heart"
                            style: "tonal"
                            theme_bg_color: "Custom"
                            md_bg_color: hex("#FEF2F2")
                            theme_icon_color: "Custom"
                            icon_color: hex("#EF4444")
                            on_release: root.controller.add_to_wishlist()
                            pos_hint: {"top": 1}

                    MDLabel:
                        id: detail_price
                        text: "Rp 0"
                        font_style: "Headline"
                        role: "small"
                        theme_text_color: "Custom"
                        text_color: hex("#16A34A")
                        bold: True
                        adaptive_height: True

                # 3. SPECS & LINKS
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: "24dp"
                    spacing: "24dp"
                    
                    # Specs Card
                    MDCard:
                        style: "outlined"
                        padding: "20dp"
                        radius: [16]
                        md_bg_color: 1, 1, 1, 1
                        adaptive_height: True
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            spacing: "12dp"
                            
                            MDLabel:
                                text: "Spesifikasi Utama"
                                font_style: "Title" 
                                role: "medium"
                                bold: True
                                adaptive_height: True
                                
                            MDDivider:
                                
                            MDLabel:
                                id: detail_specs
                                text: "..."
                                font_style: "Body"
                                role: "large"
                                theme_text_color: "Secondary"
                                adaptive_height: True
                                line_height: 1.5

                    # Action Buttons
                    MDBoxLayout:
                        adaptive_height: True
                        spacing: "12dp"
                        
                        MDButton:
                            style: "filled"
                            theme_bg_color: "Custom"
                            md_bg_color: hex("#42B549") # Tokopedia Green
                            size_hint_x: 0.5
                            height: "56dp"
                            on_release: root.controller.open_tokped()
                            MDButtonText:
                                text: "Tokopedia"
                                pos_hint: {"center_x": .5, "center_y": .5}

                        MDButton:
                            style: "filled"
                            theme_bg_color: "Custom"
                            md_bg_color: hex("#EE4D2D") # Shopee Orange
                            size_hint_x: 0.5
                            height: "56dp"
                            on_release: root.controller.open_shopee()
                            MDButtonText:
                                text: "Shopee"
                                pos_hint: {"center_x": .5, "center_y": .5}
                    
                    MDButton:
                        style: "text"
                        pos_hint: {"center_x": .5}
                        on_release: root.controller.go_back_to_results()
                        MDButtonIcon:
                            icon: "arrow-left"
                            theme_icon_color: "Custom"
                            icon_color: hex("#4F46E5")
                        MDButtonText:
                            text: "Kembali ke Hasil"
                            theme_text_color: "Custom"
                            text_color: hex("#4F46E5")
'''

Builder.load_string(KV)

# ==========================================
# 3. CONTROLLER & UI LOGIC
# ==========================================

class OptionCard(MDCard):
    text_option = StringProperty("")
    icon_name = StringProperty("checkbox-blank-circle-outline")

class GridCardItem(MDCard):
    source = StringProperty("")
    product_name = StringProperty("")
    price = StringProperty("")
    cpu_info = StringProperty("")

class GadgetStepScreen(MDScreen):
    @property
    def controller(self):
        return self.manager.parent

class GadgetBudgetScreen(GadgetStepScreen):
    def on_enter(self): self.controller.setup_budget_ui(self)

class GadgetCPUScreen(GadgetStepScreen):
    def on_enter(self): self.controller.setup_cpu_ui(self)

class GadgetRAMScreen(GadgetStepScreen):
    def on_enter(self): self.controller.setup_ram_ui(self)

class GadgetStorageScreen(GadgetStepScreen):
    def on_enter(self): self.controller.setup_storage_ui(self)

class GadgetResultScreen(GadgetStepScreen): pass
class GadgetDetailScreen(GadgetStepScreen): pass

class GadgetRecommendationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = GadgetDataManager()
        self.user_choices = {"budget": None, "cpu": None, "ram": None, "storage": None}
        self.current_detail_laptop = None
        self.filtered_df = pd.DataFrame()

        self.step_manager = MDScreenManager()
        self.add_widget(self.step_manager)

        self.step_manager.add_widget(GadgetBudgetScreen(name='step_budget'))
        self.step_manager.add_widget(GadgetCPUScreen(name='step_cpu'))
        self.step_manager.add_widget(GadgetRAMScreen(name='step_ram'))
        self.step_manager.add_widget(GadgetStorageScreen(name='step_storage'))
        self.step_manager.add_widget(GadgetResultScreen(name='result_screen'))
        self.step_manager.add_widget(GadgetDetailScreen(name='detail_screen'))

    def get_image_path(self, img_name):
        if not img_name or str(img_name).lower() == 'nan': return ""
        search_dirs = [os.path.join(os.path.dirname(__file__), 'Laptop'),
                       os.path.join(os.getcwd(), 'Laptop'), os.path.dirname(__file__)]
        base_name = os.path.splitext(img_name)[0]
        for folder in search_dirs:
            for ext in ['', '.jpg', '.jpeg', '.png', '.webp']:
                full_path = os.path.join(folder, base_name + ext)
                if os.path.exists(full_path): return full_path
        return "" 

    def go_to_home(self):
        if self.manager:
            self.manager.current = "home_screen"
            self.manager.transition.direction = "right"

    def restart_flow(self):
        self.user_choices = {"budget": None, "cpu": None, "ram": None, "storage": None}
        self.step_manager.current = "step_budget"

    def go_back_to_results(self):
        self.step_manager.current = "result_screen"
        self.step_manager.transition.direction = "right"

    def next_step(self, skip=False):
        curr = self.step_manager.current
        next_scr = ""
        if curr == "step_budget": next_scr = "step_cpu"
        elif curr == "step_cpu": next_scr = "step_ram"
        elif curr == "step_ram": next_scr = "step_storage"
        elif curr == "step_storage":
            self.calculate_recommendation()
            next_scr = "result_screen"
        if next_scr:
            self.step_manager.current = next_scr
            self.step_manager.transition.direction = "left"

    def save_choice_and_next(self, key, value):
        self.user_choices[key] = value
        self.next_step()

    def _create_option_button(self, text, val, key, screen, is_grid=False):
        grid = screen.ids.options_grid
        grid.cols = 2 if is_grid else 1
        
        # Icon selection based on key
        icon = "checkbox-blank-circle-outline"
        if key == "budget": icon = "cash"
        elif key == "cpu": icon = "chip"
        elif key == "ram": icon = "memory"
        elif key == "storage": icon = "harddisk"

        card = OptionCard(text_option=text, icon_name=icon)
        card.bind(on_release=lambda x: self.save_choice_and_next(key, val))
        grid.add_widget(card)

    def setup_budget_ui(self, scr):
        scr.ids.question_label.text = "Budget Maksimal?"
        scr.ids.options_grid.clear_widgets()
        opts = [("1jt - 5jt", (1000000, 5000000)), ("5jt - 10jt", (5000000, 10000000)), ("10jt - 15jt", (10000000, 15000000)), ("15jt - 20jt", (15000000, 20000000)), ("> 20jt", (20000000, 999999999))]
        for t, v in opts: self._create_option_button(t, v, "budget", scr)

    def setup_cpu_ui(self, scr):
        scr.ids.question_label.text = "Pilih CPU"
        scr.ids.options_grid.clear_widgets()
        for t in ["Intel", "AMD", "Semua"]: self._create_option_button(t, t, "cpu", scr, True)

    def setup_ram_ui(self, scr):
        scr.ids.question_label.text = "Pilih RAM"
        scr.ids.options_grid.clear_widgets()
        for t in ["4GB", "8GB", "16GB", "32GB", "Semua"]: self._create_option_button(t, t, "ram", scr, True)

    def setup_storage_ui(self, scr):
        scr.ids.question_label.text = "Pilih Storage"
        scr.ids.options_grid.clear_widgets()
        for t in ["256GB", "512GB", "1TB", "Semua"]: self._create_option_button(t, t, "storage", scr, True)

    def calculate_recommendation(self):
        self.filtered_df = self.data_manager.filter_laptops(
            self.user_choices['budget'], self.user_choices['cpu'],
            self.user_choices['ram'], self.user_choices['storage']
        )
        self.display_results(self.filtered_df)

    def apply_sort(self, sort_type):
        if self.filtered_df.empty: return
        df = self.filtered_df.copy()
        if sort_type == "price_asc": df = df.sort_values(by='CleanPrice')
        elif sort_type == "price_desc": df = df.sort_values(by='CleanPrice', ascending=False)
        self.display_results(df)

    def display_results(self, df):
        grid = self.step_manager.get_screen('result_screen').ids.result_grid
        grid.clear_widgets()

        if df.empty:
            grid.cols = 1
            grid.add_widget(MDLabel(text="Tidak ada produk yang cocok :(", halign="center"))
            return
        
        grid.cols = 1

        for index, row in df.iterrows():
            img_name = str(row.get('Image1', ''))
            final_path = self.get_image_path(img_name)
            if not final_path: final_path = "https://via.placeholder.com/150"

            card = GridCardItem()
            card.source = final_path
            card.product_name = f"{row.get('Brand','')} {row.get('Nama','')}"
            card.price = str(row.get('Harga', 'Hubungi Penjual'))
            card.cpu_info = f"{row.get('RAM','')} | {row.get('Storage','')}\n{row.get('CPU','')}"
            
            card.bind(on_release=lambda x, r=row: self.show_detail(r))
            grid.add_widget(card)

    def show_detail(self, row):
        self.current_detail_laptop = row
        scr = self.step_manager.get_screen('detail_screen')
        
        scr.ids.detail_name.text = str(row.get('Nama', 'Unknown'))
        scr.ids.detail_price.text = str(row.get('Harga', '-'))
        
        spec_text = ""
        for key in ['CPU', 'GPU', 'RAM', 'Storage', 'Layar', 'Baterai', 'Bobot']:
            val = str(row.get(key, '-'))
            spec_text += f"• {key}: {val}\n\n"
        scr.ids.detail_specs.text = spec_text

        # [FIX] PENGGUNAAN IMAGE_GALLERY_BOX (SCROLLVIEW) BUKAN CAROUSEL
        gallery_box = scr.ids.image_gallery_box
        gallery_box.clear_widgets()
        
        has_img = False
        for col in ['Image1', 'Image2', 'Image3', 'Image4']:
            path = self.get_image_path(str(row.get(col, '')))
            if path:
                # Membuat Kartu Gambar 1x1 Besar (320dp agar sesuai kontainer)
                img_card = MDCard(
                    size_hint=(None, None),
                    size=("320dp", "320dp"),
                    radius=[12],
                    elevation=1
                )
                img = FitImage(source=path, radius=[12])
                img_card.add_widget(img)
                gallery_box.add_widget(img_card)
                has_img = True
        
        if not has_img:
            gallery_box.add_widget(MDLabel(text="Gambar tidak tersedia", halign="center", size_hint_x=None, width=300))

        self.step_manager.transition.direction = "left"
        self.step_manager.current = "detail_screen"

    # [FIX] FUNGSI BARU UNTUK WISHLIST
    def show_detail_from_wishlist(self, item_data):
        self.current_detail_laptop = item_data # Load data dari wishlist dict
        
        # Panggil fungsi standard show_detail (dia bisa baca dict/series)
        self.show_detail(item_data)
        
        # UPDATE GALLERY KHUSUS (OVERRIDE JIKA PATH BEDA)
        scr = self.step_manager.get_screen('detail_screen')
        gallery_box = scr.ids.image_gallery_box
        gallery_box.clear_widgets()
        
        # Load gambar dari path yang tersimpan di wishlist
        for key in ['img_path_1', 'img_path_2', 'img_path_3', 'img_path_4']:
            path = item_data.get(key)
            if path and os.path.exists(path):
                img_card = MDCard(
                    size_hint=(None, None),
                    size=("320dp", "320dp"),
                    radius=[12],
                    elevation=1
                )
                img = FitImage(source=path, radius=[12])
                img_card.add_widget(img)
                gallery_box.add_widget(img_card)
        
        # Buka layar detail
        self.step_manager.current = "detail_screen"

    def add_to_wishlist(self):
        try:
            try:
                from Main.libs.screens.wishlistscreen import wishlist_manager
            except ImportError:
                import wishlist_feature
                wishlist_manager = wishlist_feature.wishlist_manager
            
            if self.current_detail_laptop is not None:
                item_dict = self.current_detail_laptop.to_dict()
                
                brand = str(item_dict.get('Brand', '')).strip()
                nama = str(item_dict.get('Nama', '')).strip()
                unique_id = f"{brand}_{nama}".replace(" ", "_").lower()
                
                # Copy semua data agar lengkap saat dikembalikan
                wishlist_data = item_dict.copy()
                
                # Tambah field wajib
                wishlist_data.update({
                    'id': unique_id,
                    'name': f"{brand} {nama}",
                    'price': int(item_dict.get('CleanPrice', 0)),
                    'price_text': str(item_dict.get('Harga', '')),
                    'image': self.get_image_path(str(item_dict.get('Image1', ''))),
                    # Simpan path lengkap semua gambar
                    'img_path_1': self.get_image_path(str(item_dict.get('Image1', ''))),
                    'img_path_2': self.get_image_path(str(item_dict.get('Image2', ''))),
                    'img_path_3': self.get_image_path(str(item_dict.get('Image3', ''))),
                    'img_path_4': self.get_image_path(str(item_dict.get('Image4', ''))),
                })
                
                success = wishlist_manager.add_item(wishlist_data)
                msg = "Berhasil masuk Wishlist!" if success else "Sudah ada di Wishlist!"
                
                MDSnackbar(
                    MDSnackbarText(text=msg),
                    y=dp(24),
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.8,
                ).open()
        except Exception as e:
            print(f"DEBUG Error Wishlist: {e}")
            MDSnackbar(
                MDSnackbarText(text="Gagal akses Wishlist"),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
            ).open()

    def open_tokped(self):
        if self.current_detail_laptop is not None:
            webbrowser.open(str(self.current_detail_laptop.get('Tokped', '')))

    def open_shopee(self):
        if self.current_detail_laptop is not None:
            webbrowser.open(str(self.current_detail_laptop.get('Shopee', '')))

if __name__ == "__main__":
    class TestApp(MDApp):
        def build(self): return GadgetRecommendationScreen()
    TestApp().run()