import os
import pandas as pd
import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemLeadingIcon
from kivy.metrics import dp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

# ==========================================
# 1. DATA HANDLER (Backend Logic)
# ==========================================
class GadgetDataManager:
    def __init__(self, csv_path=None):
        self.df = pd.DataFrame()
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path1 = os.path.join(current_dir, 'dumb database.csv')
        cwd = os.getcwd()
        path2 = os.path.join(cwd, 'dumb database.csv')
        path3 = os.path.join(cwd, 'Main', 'libs', 'screens', 'dumb database.csv')

        self.final_path = None
        if csv_path and os.path.exists(csv_path):
            self.final_path = csv_path
        elif os.path.exists(path1):
            self.final_path = path1
        elif os.path.exists(path2):
            self.final_path = path2
        elif os.path.exists(path3):
            self.final_path = path3

        if self.final_path:
            try:
                self.df = pd.read_csv(self.final_path)
                self.df.columns = self.df.columns.str.strip()
                if 'Harga' in self.df.columns:
                    self.df['CleanPrice'] = self.df['Harga'].apply(self._clean_price)
                if 'RAM' in self.df.columns:
                    self.df['CleanRAM'] = self.df['RAM'].apply(self._clean_ram)
                if 'Storage' in self.df.columns:
                    self.df['CleanStorage'] = self.df['Storage'].apply(self._clean_storage)
                print(f"DEBUG: Sukses load database. Jumlah baris: {len(self.df)}")
            except Exception as e:
                print(f"DEBUG: Error baca CSV: {e}")
        else:
            print("DEBUG: CSV Database tidak ditemukan.")

    def _clean_price(self, price_str):
        try:
            clean_str = str(price_str).replace('Rp', '').replace('.', '').split('-')[0].strip()
            return int(clean_str)
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
                match = re.search(r'(\d+)\s*TB', s)
                return int(match.group(1)) * 1024 if match else 0
            elif 'GB' in s:
                match = re.search(r'(\d+)\s*GB', s)
                return int(match.group(1)) if match else 0
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
                if "TB" in storage_size:
                    user_storage = int(str(storage_size).replace("TB", "").strip()) * 1024
                else:
                    user_storage = int(str(storage_size).replace("GB", "").strip())
                filtered = filtered[filtered['CleanStorage'] >= user_storage]
            except: pass
        return filtered

# ==========================================
# 2. KV LAYOUT (UI)
# ==========================================
KV = '''
<NavHeader@MDBoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    height: "64dp"
    md_bg_color: [0.1, 0.17, 0.35, 1]
    padding: [16, 0]
    spacing: "12dp"
    
    MDButton:
        style: "text"
        theme_icon_color: "Custom"
        icon_color: 1, 1, 1, 1
        pos_hint: {"center_y": .5}
        on_release: app.root.get_screen("rekomendasi_gadget").go_to_home() 
        MDButtonIcon:
            icon: "home"
    
    MDLabel:
        text: "Octa Tech."
        halign: "center"
        bold: True
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "Title"
        role: "large"
        pos_hint: {"center_y": .5}

    MDButton:
        style: "text"
        theme_icon_color: "Custom"
        icon_color: 1, 1, 1, 1
        pos_hint: {"center_y": .5}
        on_release: app.root.get_screen("rekomendasi_gadget").restart_flow()
        MDButtonIcon:
            icon: "refresh"

<GadgetStepScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [0.96, 0.96, 0.96, 1]
        
        NavHeader:
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "10dp"
            
            MDWidget:
                size_hint_y: 0.1
            
            MDLabel:
                id: question_label
                text: "Pertanyaan?"
                halign: "center"
                font_style: "Headline"
                role: "medium"
                bold: True
                adaptive_height: True
            
            MDWidget:
                size_hint_y: 0.05
            
            MDBoxLayout:
                size_hint_y: None
                height: "400dp"
                MDScrollView:
                    bar_width: 0
                    MDAnchorLayout:
                        anchor_x: "center"
                        anchor_y: "top"
                        size_hint_y: None
                        height: options_grid.height
                        MDGridLayout:
                            id: options_grid
                            cols: 1
                            spacing: "15dp"
                            padding: "10dp"
                            adaptive_size: True
            
            MDWidget:
                size_hint_y: 0.2

            MDAnchorLayout:
                anchor_x: "right"
                size_hint_y: None
                height: "60dp"
                MDButton:
                    style: "outlined"
                    on_release: root.controller.next_step(skip=True)
                    MDButtonText:
                        text: "SKIP >>"

<GadgetResultScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [0.96, 0.96, 0.96, 1]
        
        NavHeader:
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: "16dp"
            
            MDLabel:
                text: "Rekomendasi Laptop"
                halign: "center"
                font_style: "Headline"
                role: "small"
                bold: True
                size_hint_y: None
                height: "50dp"
            
            MDBoxLayout:
                orientation: 'horizontal'
                adaptive_height: True
                spacing: "8dp"
                pos_hint: {"center_x": .5}
                padding: [0, 0, 0, "10dp"]
                
                MDLabel:
                    text: "Urutkan:"
                    adaptive_size: True
                    pos_hint: {"center_y": .5}
                
                MDButton:
                    style: "tonal"
                    on_release: root.controller.apply_sort("price_asc")
                    MDButtonText:
                        text: "Termurah"
                
                MDButton:
                    style: "tonal"
                    on_release: root.controller.apply_sort("price_desc")
                    MDButtonText:
                        text: "Termahal"

            MDScrollView:
                MDList:
                    id: result_list
                    spacing: "12dp"
                    padding: "12dp"

            MDAnchorLayout:
                anchor_x: "center"
                size_hint_y: None
                height: "80dp"
                MDButton:
                    style: "filled"
                    on_release: root.controller.restart_flow()
                    MDButtonText:
                        text: "Cari Ulang"

<GadgetDetailScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: [0.96, 0.96, 0.96, 1]
        
        NavHeader:
        
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
                
                # 1. IMAGE CAROUSEL AREA (Putih)
                MDCard:
                    size_hint_y: None
                    height: "200dp"
                    radius: [20, 20, 20, 20]
                    md_bg_color: [1, 1, 1, 1]
                    theme_bg_color: "Custom"
                    elevation: 1
                    
                    MDBoxLayout:
                        id: image_container
                        padding: "10dp"
                        Image:
                            source: "assets/images/laptop_placeholder.png" # Default placeholder
                            id: detail_image
                            keep_ratio: True
                            allow_stretch: True

                # 2. TITLE & WISHLIST BUTTON ROW
                MDBoxLayout:
                    orientation: 'horizontal'
                    adaptive_height: True
                    spacing: "10dp"

                    MDLabel:
                        id: detail_name
                        text: "ASUS Vivobook A121106"
                        font_style: "Headline"
                        role: "small"
                        bold: True
                        adaptive_height: True
                        pos_hint: {"center_y": .5}
                    
                    # TOMBOL ADD TO WISHLIST (Biru)
                    MDButton:
                        style: "filled"
                        theme_bg_color: "Custom"
                        md_bg_color: [0.2, 0.6, 1, 1] # Biru terang
                        pos_hint: {"center_y": .5}
                        on_release: root.controller.save_to_wishlist()
                        
                        MDButtonIcon:
                            icon: "heart-outline"
                            theme_icon_color: "Custom"
                            icon_color: [1,1,1,1]
                        
                        MDButtonText:
                            text: "Add to wishlist"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]

                # 3. CONTENT SPLIT (SPECS LEFT - PRICE RIGHT)
                MDBoxLayout:
                    orientation: 'horizontal'
                    adaptive_height: True
                    spacing: "15dp"
                    height: "300dp" # Tinggi fix agar rapi

                    # KIRI: SPESIFIKASI (Abu Gelap)
                    MDCard:
                        size_hint_x: 0.5
                        adaptive_height: True
                        md_bg_color: [0.75, 0.75, 0.75, 1]
                        theme_bg_color: "Custom"
                        radius: [15, 15, 15, 15]
                        padding: "15dp"
                        
                        MDLabel:
                            id: detail_specs
                            # PERBAIKAN: Gunakan satu baris string dengan \\n untuk menghindari error parser
                            text: "Processor: -\\nRAM: -\\nStorage: -"
                            adaptive_height: True
                            theme_text_color: "Custom"
                            text_color: [0.1, 0.1, 0.1, 1]

                    # KANAN: HARGA & LINK (Abu Gelap)
                    MDCard:
                        size_hint_x: 0.5
                        adaptive_height: True
                        md_bg_color: [0.75, 0.75, 0.75, 1]
                        theme_bg_color: "Custom"
                        radius: [15, 15, 15, 15]
                        padding: "15dp"
                        orientation: "vertical"
                        spacing: "10dp"

                        MDLabel:
                            id: detail_price
                            text: "Rp -"
                            font_style: "Headline"
                            role: "small"
                            bold: True
                            halign: "center"
                            adaptive_height: True
                        
                        MDLabel:
                            text: "Marketplace:"
                            bold: True
                            adaptive_height: True

                        MDLabel:
                            text: "Shopee: Rp -"
                            font_style: "Label"
                            role: "small"
                        MDLabel:
                            text: "Tokopedia: Rp -"
                            font_style: "Label"
                            role: "small"
                        
                        MDWidget:
                        
                        MDButton:
                            style: "text"
                            on_release: root.controller.go_back_to_results()
                            pos_hint: {"center_x": .5}
                            MDButtonText:
                                text: "<< Kembali"
'''

Builder.load_string(KV)


# ==========================================
# 3. CONTROLLER & SCREENS
# ==========================================

class GadgetStepScreen(MDScreen):
    @property
    def controller(self):
        return self.manager.parent

class GadgetBudgetScreen(GadgetStepScreen):
    def on_enter(self):
        self.controller.setup_budget_ui(self)

class GadgetCPUScreen(GadgetStepScreen):
    def on_enter(self):
        self.controller.setup_cpu_ui(self)

class GadgetRAMScreen(GadgetStepScreen):
    def on_enter(self):
        self.controller.setup_ram_ui(self)

class GadgetStorageScreen(GadgetStepScreen):
    def on_enter(self):
        self.controller.setup_storage_ui(self)

class GadgetResultScreen(GadgetStepScreen):
    pass

class GadgetDetailScreen(GadgetStepScreen):
    pass

# ==========================================
# 4. MAIN SCREEN (CONTAINER)
# ==========================================
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

    # --- NAVIGASI ---
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

    # --- LOGIC DATA & UI SETUP ---
    def save_choice_and_next(self, key, value):
        print(f"DEBUG: Pilih {key} = {value}")
        self.user_choices[key] = value
        self.next_step()

    def _create_option_button(self, text, callback_value, key_choice, screen_obj, is_grid=False):
        grid = screen_obj.ids.options_grid
        grid_btn_w = 140 
        spacing = 15     
        total_width = (grid_btn_w * 2) + spacing
        
        if is_grid:
            grid.cols = 2
            btn_size = (dp(grid_btn_w), dp(grid_btn_w))
        else:
            grid.cols = 1
            btn_size = (dp(total_width), dp(80))

        btn = MDButton(
            style="outlined",
            size_hint=(None, None), 
            size=btn_size,
        )
        
        btn_text = MDButtonText(
            text=text, 
            pos_hint={"center_x": .5, "center_y": .5},
            font_style="Headline",
            role="small", 
            halign="center"
        )
        btn.add_widget(btn_text)
        
        btn.bind(on_release=lambda x: self.save_choice_and_next(key_choice, callback_value))
        grid.add_widget(btn)

    def setup_budget_ui(self, screen):
        screen.ids.question_label.text = "Maksimal budget kamu berapa?"
        screen.ids.options_grid.clear_widgets()
        options = [
            ("Rp 1jt - 5jt", (1000000, 5000000)),
            ("Rp 5jt - 10jt", (5000000, 10000000)),
            ("Rp 10jt - 15jt", (10000000, 15000000)),
            ("Rp 15jt - 20jt", (15000000, 20000000)),
            ("> Rp 20jt", (20000000, 999999999)) 
        ]
        for text, val in options:
            self._create_option_button(text, val, "budget", screen, is_grid=False)

    def setup_cpu_ui(self, screen):
        screen.ids.question_label.text = "Mau pakai CPU apa?"
        screen.ids.options_grid.clear_widgets()
        options = ["Intel", "AMD", "Semua"]
        for opt in options:
            self._create_option_button(opt, opt, "cpu", screen, is_grid=True)

    def setup_ram_ui(self, screen):
        screen.ids.question_label.text = "Butuh RAM berapa?"
        screen.ids.options_grid.clear_widgets()
        options = ["4GB", "8GB", "16GB", "32GB", "Semua"]
        for opt in options:
            self._create_option_button(opt, opt, "ram", screen, is_grid=True)

    def setup_storage_ui(self, screen):
        screen.ids.question_label.text = "Butuh Storage berapa?"
        screen.ids.options_grid.clear_widgets()
        options = ["256GB", "512GB", "1TB", "Semua"]
        for opt in options:
            self._create_option_button(opt, opt, "storage", screen, is_grid=True)

    # --- HASIL & DETAIL ---
    def calculate_recommendation(self):
        self.filtered_df = self.data_manager.filter_laptops(
            budget_range=self.user_choices['budget'],
            cpu_type=self.user_choices['cpu'],
            ram_size=self.user_choices['ram'],
            storage_size=self.user_choices['storage']
        )
        self.display_results(self.filtered_df)

    def apply_sort(self, sort_type):
        if self.filtered_df.empty: return
        sorted_df = self.filtered_df.copy()
        if sort_type == "price_asc":
            sorted_df = sorted_df.sort_values(by='CleanPrice', ascending=True)
        elif sort_type == "price_desc":
            sorted_df = sorted_df.sort_values(by='CleanPrice', ascending=False)
        self.display_results(sorted_df)

    def display_results(self, df):
        result_screen = self.step_manager.get_screen('result_screen')
        list_container = result_screen.ids.result_list
        list_container.clear_widgets()
        
        if df.empty:
            list_container.add_widget(MDListItem(MDListItemHeadlineText(text="Tidak ditemukan hasil yang cocok.")))
        else:
            for index, row in df.iterrows():
                leading = MDListItemLeadingIcon(icon="laptop")
                
                item = MDListItem(
                    leading,
                    MDListItemHeadlineText(text=f"{row.get('Brand','')} - {row.get('Nama','')}"[:30]),
                    MDListItemSupportingText(text=f"Harga: {row.get('Harga','')}"),
                    MDListItemTertiaryText(text=f"{row.get('CPU','')} | RAM {row.get('RAM','')}")
                )
                item.bind(on_release=lambda x, r=row: self.show_detail(r))
                list_container.add_widget(item)

    def show_detail(self, row):
        self.current_detail_laptop = row
        detail_screen = self.step_manager.get_screen('detail_screen')
        
        detail_screen.ids.detail_name.text = str(row.get('Nama', 'Unknown'))
        detail_screen.ids.detail_price.text = f"Rp {row.get('Harga', '-')}"
        
        # Format Spesifikasi
        specs = f"Proccesor : {row.get('CPU','-')}\n" \
                f"RAM : {row.get('RAM','-')}\n" \
                f"GPU : {row.get('GPU','-')}\n" \
                f"Storage : {row.get('Storage','-')}\n" \
                f"Layar : {row.get('Layar','-')}"
        
        detail_screen.ids.detail_specs.text = specs
        
        self.step_manager.transition.direction = "left"
        self.step_manager.current = "detail_screen"

    def save_to_wishlist(self):
        try:
            from Main.libs.screens.wishlistscreen import wishlist_manager
            
            if self.current_detail_laptop is not None:
                item_dict = self.current_detail_laptop.to_dict()
                success = wishlist_manager.add_item(item_dict)
                msg = "Berhasil masuk Wishlist!" if success else "Item sudah ada di Wishlist!"
                
                MDSnackbar(
                    MDSnackbarText(text=msg),
                    y=dp(24),
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.8
                ).open()
        except ImportError:
            print("Gagal import wishlist_manager. Pastikan file wishlistscreen.py ada.")
        except Exception as e:
            print(f"Error saving wishlist: {e}")

if __name__ == "__main__":
    GadgetRecommenderApp().run()