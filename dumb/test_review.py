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
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

Window.size = (1024, 768)

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
    review_count = NumericProperty(0)
    
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

class HomeScreen(MDScreen):
    pass

class GadgetReviewApp(MDApp):
    products = ListProperty(INITIAL_PRODUCTS)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        
        # PENTING: Load file KV eksternal di sini
        Builder.load_file("review.kv")
        
        self.sm = ScreenManager()
        self.home_screen = HomeScreen(name='home')
        self.detail_screen = DetailScreen(name='detail')
        
        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.detail_screen)
        
        return self.sm

    def on_start(self):
        self.filter_products("")

    def filter_products(self, query):
        grid = self.home_screen.ids.product_grid
        grid.clear_widgets()
        query = query.lower()
        
        for product in self.products:
            if query in product['name'].lower() or query in product['category'].lower():
                total = sum(r['rating'] for r in product['reviews'])
                count = len(product['reviews'])
                avg = round(total / count) if count > 0 else 0
                
                card = ProductCard(
                    product_id=product['id'],
                    name=product['name'],
                    category=product['category'],
                    image_source=product['image'],
                    rating=avg,
                    review_count=count
                )
                grid.add_widget(card)

    def show_product_detail(self, product_id):
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            self.detail_screen.load_product(product)
            self.sm.transition.direction = 'left'
            self.sm.current = 'detail'

    def go_back(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'
        self.filter_products(self.home_screen.ids.search_input.text)

    def add_review(self, product_id, rating, text):
        for product in self.products:
            if product['id'] == product_id:
                new_review = {
                    'id': len(product['reviews']) + 1,
                    'user': 'Saya (Baru)',
                    'rating': rating,
                    'text': text
                }
                product['reviews'].append(new_review)
                break

if __name__ == '__main__':
    GadgetReviewApp().run()