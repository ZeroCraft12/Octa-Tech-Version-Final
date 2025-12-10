import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.widget import Widget
from kivymd.uix.label import MDLabel 
from kivymd.uix.fitimage import FitImage
from kivymd.uix.divider import MDDivider

# Import komponen Dialog
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

import csv
import os

import random

def load_products():
    products = []
    # Determine the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to CSV file
    csv_path = os.path.join(current_dir, "database(Laptop).csv")
    
    print(f"DEBUG: Attempting to load CSV from {csv_path}")
    if not os.path.exists(csv_path):
        print(f"CRITICAL ERROR: CSV file not found at {csv_path}")
        return []

    # --- DUMMY DATA POOL ---
    dummy_users = [
        "Budi Santoso", "Siti Aminah", "Rizky Pratama", "Dewi Lestari", 
        "Andi Susanto", "Rina Wijaya", "Eko Saputra", "Nurul Hidayah",
        "Bayu Nugroho", "Sari Indah", "Adi Kurniawan", "Mega Putri",
        "Fajar Ramadhan", "Lina Marlina", "Dimas Anggara"
    ]

    positive_templates = [
        "Laptop ini sangat bagus! Performa cepat dan layarnya jernih.",
        "Worth it banget dengan harga segini. Baterai awet seharian.",
        "Desainnya elegan dan ringan, enak dibawa kemana-mana.",
        "Buat multitasking lancar jaya, ga ada kendala.",
        "Suka banget sama keyboardnya, empuk buat ngetik lama.",
        "Pengiriman cepat, barang aman sampai tujuan. Mantap!",
        "Gaming tipis-tipis masih oke banget pake laptop ini.",
        "Speaker kenceng, bass-nya lumayan berasa.",
        "Chargernya cepet penuh, sangat membantu mobilitas.",
        "Rekomended banget buat mahasiswa atau pekerja kantoran."
    ]

    neutral_templates = [
        "Lumayan lah buat harga segini, sesuai ekspektasi.",
        "Bagus sih, tapi sayang port USB-nya dikit.",
        "Body agak licin, tapi overall oke.",
        "Webcam standar aja, butuh pencahayaan bagus.",
        "Kadang agak anget kalau dipake berat, tapi wajar sih.",
        "Cukup baik untuk penggunaan sehari-hari."
    ]

    try:
        # Use utf-8-sig to handle potential BOM from Excel
        with open(csv_path, mode='r', encoding='utf-8-sig') as file:
            # Using delimiter ';' as seen in the file content
            reader = csv.DictReader(file, delimiter=';')
            
            # Debug: Print fieldnames to verify CSV structure
            print(f"DEBUG: CSV Fieldnames: {reader.fieldnames}")

            for i, row in enumerate(reader):
                try:
                    # Construct absolute path for the image
                    image_filename = row.get('Image1', '').strip()
                    image_path = os.path.join(current_dir, "Laptop", image_filename)
                    if not os.path.exists(image_path):
                         # print(f"DEBUG: Image not found: {image_path}") # Optional: reduce noise
                         pass
                    
                    # Generate Dummy Reviews
                    product_reviews = []
                    num_reviews = random.randint(1, 5) # Generate 1 to 5 reviews per product
                    
                    for _ in range(num_reviews):
                        user = random.choice(dummy_users)
                        # Biased towards positive ratings for realism/demo
                        rating = random.choices([3, 4, 5], weights=[1, 4, 5], k=1)[0] 
                        
                        if rating >= 4:
                            text = random.choice(positive_templates)
                        else:
                            text = random.choice(neutral_templates)
                            
                        product_reviews.append({
                            'user': user,
                            'rating': rating,
                            'text': text
                        })


                    product = {
                        'id': int(row['No']),
                        'name': f"{row['Brand']} {row['Nama']}",
                        'image': image_path,
                        'category': 'Laptop',
                        'price': row.get('Harga', ''),
                        'description': f"CPU: {row.get('CPU','')}, RAM: {row.get('RAM','')}, Storage: {row.get('Storage','')}",
                        'reviews': product_reviews 
                    }
                    products.append(product)
                except (ValueError, KeyError) as e:
                     print(f"CRITICAL ERROR: Skipping row {i} due to error: {e}. Row data: {row}")
                     continue
            
            print(f"DEBUG: Successfully loaded {len(products)} products from CSV.")
                     
    except Exception as e:
        print(f"CRITICAL ERROR: Error reading CSV: {e}")
        return []

    return products

# Load products from CSV
INITIAL_PRODUCTS = load_products()

KV = '''
#:import hex kivy.utils.get_color_from_hex

# ----- KOMPONEN REUSABLE -----

<StarIcon@MDIcon>:
    theme_text_color: "Custom"
    text_color: hex("#FACC15")
    font_size: "16sp"

<StarRating@MDBoxLayout>:
    orientation: 'horizontal'
    adaptive_size: True
    spacing: "2dp"
    rating: 0
    StarIcon:
        icon: "star" if root.rating >= 1 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 1 else hex("#D1D5DB")
    StarIcon:
        icon: "star" if root.rating >= 2 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 2 else hex("#D1D5DB")
    StarIcon:
        icon: "star" if root.rating >= 3 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 3 else hex("#D1D5DB")
    StarIcon:
        icon: "star" if root.rating >= 4 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 4 else hex("#D1D5DB")
    StarIcon:
        icon: "star" if root.rating >= 5 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 5 else hex("#D1D5DB")

# ----- SCREEN HOME -----

<ProductCard>:
    style: "elevated"
    orientation: "vertical"
    size_hint_y: None
    height: "340dp"
    radius: [16,]
    md_bg_color: 1, 1, 1, 1
    on_release: app.show_product_detail(root.product_id)
    elevation: 2
    shadow_softness: 4
    shadow_offset: (0, 2)
    
    MDBoxLayout:
        size_hint_y: None
        height: "180dp"
        radius: [16, 16, 0, 0]
        FitImage:
            source: root.image_source
            radius: [16, 16, 0, 0]
            
    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "4dp"
        
        MDLabel:
            text: root.category.upper()
            font_style: "Label"
            role: "small"
            theme_text_color: "Custom"
            text_color: hex("#6366F1")
            bold: True
            adaptive_height: True

        MDLabel:
            text: root.name
            font_style: "Title"
            role: "medium"
            theme_text_color: "Custom"
            text_color: hex("#111827")
            bold: True
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            max_lines: 2
        
        MDWidget: # Spacer flexible
        
        MDBoxLayout:
            adaptive_height: True
            spacing: "6dp"
            StarRating:
                rating: root.rating
            MDLabel:
                text: f"({root.review_count})"
                font_style: "Body"
                role: "small"
                theme_text_color: "Hint"
                adaptive_height: True
                pos_hint: {"center_y": .5}

<ReviewScreen>:
    md_bg_color: hex("#F3F4F6")

    MDBoxLayout:
        orientation: 'vertical'
        
        # --- HEADER AREA ---
        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            md_bg_color: hex("#4F46E5")
            padding: ["24dp", "40dp", "24dp", "50dp"]
            spacing: "8dp"
            radius: [0, 0, 24, 24]

            MDLabel:
                text: "Review Gadget"
                halign: "center"
                font_style: "Headline"
                role: "large"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                bold: True
                adaptive_height: True
            
            MDLabel:
                text: "Temukan ulasan jujur dari komunitas kami"
                halign: "center"
                font_style: "Body"
                role: "large"
                theme_text_color: "Custom"
                text_color: hex("#E0E7FF")
                adaptive_height: True

        # --- SEARCH BAR (Floating) ---
        MDBoxLayout:
            adaptive_height: True
            padding: ["24dp", 0, "24dp", 0]
            # Negative margin to pull it up into header (Note: Kivy layouts can be tricky with negative margins, 
            # so we use a relative layout approach or just place it right below)
            # Simplified approach: Just standard placement below header for stability
            
            MDCard:
                size_hint_y: None
                height: "56dp"
                style: "elevated"
                md_bg_color: 1, 1, 1, 1
                radius: [28,]
                elevation: 3
                padding: ["16dp", "4dp", "16dp", "4dp"]
                pos_hint: {"center_x": .5, "top": 1} 
                # Hacky: Move it up visually using translation if needed, but simple stack is safer
                
                MDBoxLayout:
                    spacing: "12dp"
                    MDIcon:
                        icon: "magnify"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Hint"
                    TextInput:
                        id: search_input
                        hint_text: "Cari laptop, hp, dll..."
                        background_color: 0,0,0,0
                        foreground_color: 0,0,0,1
                        cursor_color: hex("#4F46E5")
                        font_size: "16sp"
                        multiline: False
                        padding_y: [16, 0]
                        size_hint_y: 1
                        on_text: app.filter_products(self.text)

        # --- CONTENT ---
        MDScrollView:
            do_scroll_x: False
            scroll_type: ['bars', 'content'] 
            bar_width: "8dp"
            
            MDGridLayout:
                id: product_grid
                cols: 1 if root.width < 600 else (2 if root.width < 900 else 3)
                adaptive_height: True
                padding: ["24dp", "24dp", "24dp", "24dp"]
                spacing: "20dp"
                size_hint_y: None

    # Home Button (Floating Bottom Right or Top Right)
    MDIconButton:
        icon: "home"
        style: "tonal"
        pos_hint: {"top": 0.96, "right": 0.96}
        theme_bg_color: "Custom"
        md_bg_color: 1, 1, 1, 0.2
        theme_icon_color: "Custom"
        icon_color: 1, 1, 1, 1
        on_release:
            app.root.transition.direction = 'right'
            app.root.current = 'home_screen'

# ----- SCREEN DETAIL -----

<DetailScreen>:
    md_bg_color: hex("#F9FAFB")
    
    MDScrollView:
        do_scroll_x: False
        do_scroll_y: True
        scroll_type: ['bars', 'content'] 
        bar_width: "12dp"
        bar_color: hex("#4F46E5")
        
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            
            # --- HEADER GAMBAR PRODUK ---
            MDBoxLayout:
                size_hint_y: None
                height: "300dp"
                md_bg_color: 1,1,1,1
                
                FitImage:
                    source: root.product_image
                    size_hint: 1, 1
                    
            # --- KONTEN DETAIL ---
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "24dp"
                spacing: "24dp"
                
                # Info Produk
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "8dp"
                    
                    MDLabel:
                        text: root.product_category.upper()
                        theme_text_color: "Custom"
                        text_color: hex("#4F46E5")
                        font_style: "Label"
                        role: "medium"
                        bold: True
                        adaptive_height: True
                        
                    MDLabel:
                        text: root.product_name
                        theme_text_color: "Custom"
                        text_color: hex("#111827")
                        font_style: "Headline"
                        role: "small"
                        bold: True
                        adaptive_height: True
                        
                    MDBoxLayout:
                        adaptive_height: True
                        spacing: "8dp"
                        StarRating:
                            rating: root.product_rating
                        MDLabel:
                            text: f"{root.product_rating}/5 ({root.review_count} reviews)"
                            theme_text_color: "Secondary"
                            font_style: "Body"
                            role: "medium"
                            adaptive_height: True

                MDDivider:
                    color: hex("#E5E7EB")

                # --- SECTION REVIEWS ---
                MDBoxLayout:
                    adaptive_height: True
                    spacing: "10dp"
                    MDLabel:
                        text: "Ulasan Pengguna"
                        font_style: "Title"
                        role: "large"
                        bold: True
                        adaptive_height: True
                        pos_hint: {"center_y": .5}
                    
                    MDWidget:
                        
                    MDButton:
                        style: "filled"
                        theme_bg_color: "Custom"
                        md_bg_color: hex("#4F46E5")
                        on_release: root.show_add_review_dialog()
                        radius: [20,]
                        MDButtonIcon:
                            icon: "pencil"
                            theme_icon_color: "Custom"
                            icon_color: 1,1,1,1
                        MDButtonText:
                            text: "Tulis Review"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1

                MDBoxLayout:
                    id: review_list
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "16dp"

    # Floating Back Button
    MDIconButton:
        icon: "arrow-left"
        style: "filled"
        pos_hint: {"top": 0.96, "left": 0.04}
        theme_bg_color: "Custom"
        md_bg_color: 1,1,1,1
        theme_icon_color: "Custom"
        icon_color: hex("#1F2937")
        elevation: 2
        on_release: app.go_back()

<ReviewItem>:
    orientation: "vertical"
    adaptive_height: True
    padding: "16dp"
    spacing: "12dp"
    md_bg_color: 1, 1, 1, 1
    radius: [12,]
    elevation: 1 # Shadow card for review
    
    MDBoxLayout:
        spacing: "12dp"
        adaptive_height: True
        
        MDCard:
            size_hint: None, None
            size: "40dp", "40dp"
            radius: [20,]
            md_bg_color: hex("#EEF2FF")
            elevation: 0
            MDIcon:
                icon: "account-circle"
                halign: "center"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: hex("#4F46E5")
                font_size: "24sp"
        
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            pos_hint: {"center_y": .5}
            MDLabel:
                text: root.user_name
                bold: True
                font_style: "Body"
                role: "large"
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: hex("#111827")
            StarRating:
                rating: root.rating

    MDLabel:
        text: root.text
        font_style: "Body"
        role: "medium"
        theme_text_color: "Custom"
        text_color: hex("#4B5563")
        adaptive_height: True
        
<AddReviewContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "240dp"
    
    MDLabel:
        text: "Berikan Rating:"
        adaptive_height: True
        font_style: "Label"
        role: "large"
        
    MDBoxLayout:
        orientation: "horizontal"
        adaptive_height: True
        spacing: "8dp"
        pos_hint: {"center_x": .5}
        
        MDIconButton:
            icon: "star" if root.rating >= 1 else "star-outline"
            theme_icon_color: "Custom"
            icon_color: hex("#FACC15")
            icon_size: "32sp"
            on_release: root.rating = 1
        MDIconButton:
            icon: "star" if root.rating >= 2 else "star-outline"
            theme_icon_color: "Custom"
            icon_color: hex("#FACC15")
            icon_size: "32sp"
            on_release: root.rating = 2
        MDIconButton:
            icon: "star" if root.rating >= 3 else "star-outline"
            theme_icon_color: "Custom"
            icon_color: hex("#FACC15")
            icon_size: "32sp"
            on_release: root.rating = 3
        MDIconButton:
            icon: "star" if root.rating >= 4 else "star-outline"
            theme_icon_color: "Custom"
            icon_color: hex("#FACC15")
            icon_size: "32sp"
            on_release: root.rating = 4
        MDIconButton:
            icon: "star" if root.rating >= 5 else "star-outline"
            theme_icon_color: "Custom"
            icon_color: hex("#FACC15")
            icon_size: "32sp"
            on_release: root.rating = 5

    MDCard:
        style: "outlined"
        md_bg_color: hex("#F9FAFB")
        line_color: hex("#D1D5DB")
        radius: [8,]
        padding: "8dp"
        size_hint_y: None
        height: "120dp"
        
        TextInput:
            id: review_text
            hint_text: "Ceritakan pengalaman Anda... (Minimal 10 karakter)"
            background_color: 0,0,0,0
            foreground_color: 0,0,0,1
            cursor_color: 0,0,0,1
            font_size: "14sp"
            multiline: True
'''

Builder.load_string(KV)

class ProductCard(MDCard):
    product_id = NumericProperty(0)
    image_source = StringProperty("")
    category = StringProperty("")
    name = StringProperty("")
    rating = NumericProperty(0)
    review_count = NumericProperty(0)

class ReviewItem(MDBoxLayout):
    user_name = StringProperty("")
    rating = NumericProperty(0)
    text = StringProperty("")

class AddReviewContent(MDBoxLayout):
    rating = NumericProperty(5)

class DetailScreen(MDScreen):
    product_id = NumericProperty(0)
    product_name = StringProperty("")
    product_image = StringProperty("")
    product_category = StringProperty("")
    product_rating = NumericProperty(0)
    review_count = NumericProperty(0) # Perbaikan: Tambahkan properti ini agar tidak error di KV
    
    dialog = None

    def load_product(self, product):
        self.product_id = product['id']
        self.product_name = product['name']
        self.product_image = product['image']
        self.product_category = product['category']
        
        total = sum(r['rating'] for r in product['reviews'])
        count = len(product['reviews'])
        self.product_rating = round(total / count) if count > 0 else 0
        self.review_count = count
        
        # Populate Reviews
        self.ids.review_list.clear_widgets()
        for review in product['reviews']:
            item = ReviewItem(
                user_name=review['user'],
                rating=review['rating'],
                text=review['text']
            )
            self.ids.review_list.add_widget(item)

    def show_add_review_dialog(self):
        if not self.dialog:
            self.content_cls = AddReviewContent()
            self.dialog = MDDialog(
                MDDialogHeadlineText(text="Tulis Review"),
                MDDialogSupportingText(text="Bagikan pendapat Anda jujur tentang produk ini."),
                MDDialogContentContainer(
                    self.content_cls,
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Batal"),
                        style="text",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDButton(
                        MDButtonText(text="Kirim Review"),
                        style="filled",
                        theme_bg_color="Custom",
                        md_bg_color=(79/255, 70/255, 229/255, 1),
                        on_release=self.submit_review
                    ),
                    spacing="8dp",
                ),
            )
        self.dialog.open()

    def submit_review(self, instance):
        text = self.content_cls.ids.review_text.text
        rating = self.content_cls.rating
        
        if text.strip():
            app = MDApp.get_running_app()
            app.add_review(self.product_id, rating, text)
            self.content_cls.ids.review_text.text = "" 
            self.dialog.dismiss()
            product = next((p for p in app.products if p['id'] == self.product_id), None)
            if product:
                self.load_product(product)

class ReviewScreen(MDScreen):
    pass
