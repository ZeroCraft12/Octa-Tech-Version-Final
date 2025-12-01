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

# Data Dummy dengan teks PANJANG untuk mengetes Scroll
INITIAL_PRODUCTS = [
    {
        'id': 1,
        'name': 'iPhone 15 Pro',
        'image': 'https://placehold.co/600x600/4F46E5/FFFFFF/png?text=iPhone+15+Pro',
        'category': 'Smartphone',
        'reviews': [
            {'id': 1, 'user': 'Budi Santoso', 'rating': 5, 'text': 'Kamera luar biasa! Hasil foto sangat jernih bahkan di malam hari. Saya sudah mencoba memotret bulan dan hasilnya menakjubkan. Baterai juga tahan seharian untuk pemakaian normal.'},
            {'id': 2, 'user': 'Siti Aminah', 'rating': 4, 'text': 'Performa sangat cepat untuk edit video ringan. Namun harganya memang cukup mahal dibandingkan kompetitor. Tapi build quality titaniumnya terasa sangat premium dan ringan di tangan.'},
            {'id': 3, 'user': 'Reviewer Panjang', 'rating': 5, 'text': 'Ini adalah tes teks panjang untuk memastikan layar bisa di-scroll. '.join(['Lorem ipsum dolor sit amet. '] * 10)},
            {'id': 4, 'user': 'Pengguna Lama', 'rating': 3, 'text': 'Upgrade dari iPhone 11, terasa bedanya jauh sekali terutama di layar 120Hz.'}
        ]
    },
    {
        'id': 2,
        'name': 'Samsung Galaxy S24',
        'image': 'https://placehold.co/600x600/7C3AED/FFFFFF/png?text=Galaxy+S24',
        'category': 'Smartphone',
        'reviews': [
            {'id': 1, 'user': 'Andi Wijaya', 'rating': 5, 'text': 'Layar AMOLED-nya sangat tajam.'},
            {'id': 2, 'user': 'Dewi Lestari', 'rating': 4, 'text': 'Fitur AI sangat membantu.'}
        ]
    },
    {
        'id': 3,
        'name': 'MacBook Air M3',
        'image': 'https://placehold.co/600x600/059669/FFFFFF/png?text=MacBook+Air+M3',
        'category': 'Laptop',
        'reviews': [
            {'id': 1, 'user': 'Rudi Hartono', 'rating': 5, 'text': 'Ringan, cepat, dan baterai tahan lama.'}
        ]
    },
    {
        'id': 4,
        'name': 'Sony WH-1000XM5',
        'image': 'https://placehold.co/600x600/DC2626/FFFFFF/png?text=Sony+XM5',
        'category': 'Headphone',
        'reviews': [
            {'id': 1, 'user': 'Joko Susilo', 'rating': 5, 'text': 'Noise cancellation terbaik!'}
        ]
    },
]

KV = '''
#:import hex kivy.utils.get_color_from_hex

# ----- KOMPONEN REUSABLE -----

<StarIcon@MDIcon>:
    theme_text_color: "Custom"
    text_color: hex("#FACC15")
    font_size: "18sp"

<StarRating@MDBoxLayout>:
    orientation: 'horizontal'
    adaptive_size: True
    spacing: "2dp"
    rating: 0
    StarIcon:
        icon: "star" if root.rating >= 1 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 1 else hex("#E5E7EB")
    StarIcon:
        icon: "star" if root.rating >= 2 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 2 else hex("#E5E7EB")
    StarIcon:
        icon: "star" if root.rating >= 3 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 3 else hex("#E5E7EB")
    StarIcon:
        icon: "star" if root.rating >= 4 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 4 else hex("#E5E7EB")
    StarIcon:
        icon: "star" if root.rating >= 5 else "star-outline"
        text_color: hex("#FACC15") if root.rating >= 5 else hex("#E5E7EB")

# ----- SCREEN HOME -----

<ProductCard>:
    style: "elevated"
    orientation: "vertical"
    size_hint_y: None
    height: "320dp"
    radius: [12,]
    md_bg_color: 1, 1, 1, 1
    on_release: app.show_product_detail(root.product_id)
    elevation: 1
    
    MDBoxLayout:
        size_hint_y: None
        height: "180dp"
        radius: [12, 12, 0, 0]
        FitImage:
            source: root.image_source
            radius: [12, 12, 0, 0]
            
    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "6dp"
        
        MDLabel:
            text: root.category
            font_style: "Label"
            role: "medium"
            theme_text_color: "Custom"
            text_color: hex("#4F46E5")
            bold: True
            adaptive_height: True

        MDLabel:
            text: root.name
            font_style: "Title"
            role: "medium"
            theme_text_color: "Custom"
            text_color: hex("#1F2937")
            bold: True
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
        
        MDBoxLayout:
            adaptive_height: True
            spacing: "8dp"
            StarRating:
                rating: root.rating
            MDLabel:
                text: f"({root.review_count} reviews)"
                font_style: "Body"
                role: "small"
                theme_text_color: "Secondary"
                adaptive_height: True

<ReviewScreen>:
    md_bg_color: hex("#EEF2FF")
    
    MDBoxLayout:
        orientation: 'vertical'
        
        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            padding: ["20dp", "40dp", "20dp", "30dp"]
            spacing: "8dp"
            md_bg_color: hex("#EEF2FF")

            MDLabel:
                text: "Review Gadget"
                halign: "center"
                font_style: "Headline"
                role: "medium"
                theme_text_color: "Custom"
                text_color: hex("#1F2937")
                bold: True
                adaptive_height: True
            
            MDLabel:
                text: "Temukan review produk gadget terbaik dari pengguna"
                halign: "center"
                font_style: "Body"
                role: "large"
                theme_text_color: "Secondary"
                adaptive_height: True

        MDBoxLayout:
            adaptive_height: True
            padding: [0, 0, 0, "30dp"]
            MDAnchorLayout:
                anchor_x: "center"
                size_hint_y: None
                height: "56dp"
                MDCard:
                    size_hint: None, None
                    size: min(root.width - 40, 600), "56dp"
                    style: "elevated"
                    md_bg_color: 1, 1, 1, 1
                    radius: [8,]
                    padding: ["16dp", "4dp", "16dp", "4dp"]
                    MDBoxLayout:
                        spacing: "12dp"
                        MDIcon:
                            icon: "magnify"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Secondary"
                        TextInput:
                            id: search_input
                            hint_text: "Cari produk gadget..."
                            background_color: 0,0,0,0
                            foreground_color: 0,0,0,1
                            cursor_color: 0,0,0,1
                            font_size: "16sp"
                            multiline: False
                            padding_y: [16, 0]
                            size_hint_y: 1
                            on_text: app.filter_products(self.text)

        MDScrollView:
            do_scroll_x: False
            scroll_type: ['bars', 'content'] 
            bar_width: "10dp"
            
            MDGridLayout:
                id: product_grid
                cols: 1 if root.width < 600 else (2 if root.width < 900 else 3)
                adaptive_height: True
                padding: "20dp"
                spacing: "24dp"
                size_hint_y: None

# ----- SCREEN DETAIL -----

<DetailScreen>:
    md_bg_color: hex("#EEF2FF")
    
    # PERBAIKAN SCROLLVIEW
    MDScrollView:
        do_scroll_x: False
        do_scroll_y: True
        # PENTING: scroll_type ini memungkinkan drag mouse/touch
        scroll_type: ['bars', 'content'] 
        bar_width: "12dp"
        bar_color: hex("#4F46E5")
        bar_inactive_color: hex("#C7D2FE")
        
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            padding: "20dp"
            spacing: "20dp"
            
            MDButton:
                style: "text"
                on_release: app.go_back()
                pos_hint: {"x": 0}
                MDButtonIcon:
                    icon: "arrow-left"
                    theme_text_color: "Custom"
                    text_color: hex("#4F46E5")
                MDButtonText:
                    text: "Kembali ke Pencarian"
                    theme_text_color: "Custom"
                    text_color: hex("#4F46E5")
                    font_style: "Label"
                    role: "large"
                    bold: True

            MDCard:
                orientation: "vertical"
                size_hint_x: None
                width: min(root.width - 40, 900)
                pos_hint: {"center_x": .5}
                adaptive_height: True
                radius: [16,]
                padding: "32dp"
                md_bg_color: 1, 1, 1, 1
                elevation: 1
                
                MDBoxLayout:
                    orientation: "vertical" if root.width < 700 else "horizontal"
                    adaptive_height: True
                    spacing: "32dp"
                    
                    MDCard:
                        size_hint: None, None
                        width: (root.width - 104) if root.width < 700 else "300dp"
                        height: self.width
                        radius: [12,]
                        elevation: 0
                        md_bg_color: hex("#F3F4F6")
                        FitImage:
                            source: root.product_image
                            radius: [12,]
                            
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        pos_hint: {"top": 1} if root.width < 700 else {"center_y": .5}
                        spacing: "8dp"
                        
                        MDLabel:
                            text: root.product_category
                            theme_text_color: "Custom"
                            text_color: hex("#4F46E5")
                            font_style: "Label"
                            role: "large"
                            bold: True
                            adaptive_height: True
                            
                        MDLabel:
                            text: root.product_name
                            theme_text_color: "Custom"
                            text_color: hex("#111827")
                            font_style: "Display"
                            role: "small"
                            bold: True
                            adaptive_height: True
                            
                        MDBoxLayout:
                            adaptive_height: True
                            spacing: "8dp"
                            StarRating:
                                rating: root.product_rating
                            MDLabel:
                                text: f"({root.review_count} reviews)"
                                theme_text_color: "Secondary"
                                adaptive_height: True

                MDDivider:
                    color: hex("#E5E7EB")
                    pos_hint: {"center_x": .5}
                    modifier: "middle"
                    
                MDBoxLayout:
                    adaptive_height: True
                    padding: [0, "24dp", 0, "16dp"]
                    MDLabel:
                        text: "Review Pengguna"
                        font_style: "Headline"
                        role: "small"
                        bold: True
                        adaptive_height: True
                        pos_hint: {"center_y": .5}
                    Widget:
                    MDButton:
                        style: "filled"
                        theme_bg_color: "Custom"
                        md_bg_color: hex("#4F46E5")
                        on_release: root.show_add_review_dialog()
                        MDButtonIcon:
                            icon: "plus"
                            theme_icon_color: "Custom"
                            icon_color: 1,1,1,1
                        MDButtonText:
                            text: "Tambah Review"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1

                MDBoxLayout:
                    id: review_list
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "0dp"

<ReviewItem>:
    orientation: "vertical"
    adaptive_height: True
    padding: [0, "16dp", 0, "16dp"]
    spacing: "8dp"
    
    MDBoxLayout:
        spacing: "12dp"
        adaptive_height: True
        MDCard:
            size_hint: None, None
            size: "40dp", "40dp"
            radius: [20,]
            md_bg_color: hex("#E0E7FF")
            elevation: 0
            MDIcon:
                icon: "account"
                halign: "center"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: hex("#4F46E5")
        
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
                text_color: hex("#1F2937")
            StarRating:
                rating: root.rating

    MDLabel:
        text: root.text
        font_style: "Body"
        role: "medium"
        theme_text_color: "Custom"
        text_color: hex("#4B5563")
        adaptive_height: True
        padding: ["52dp", 0, 0, 0]

    MDDivider:
        color: hex("#F3F4F6")
        
<AddReviewContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "220dp"
    
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
        height: "100dp"
        
        TextInput:
            id: review_text
            hint_text: "Ceritakan pengalaman Anda..."
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
