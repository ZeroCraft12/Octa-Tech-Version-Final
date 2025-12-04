import sys
import os

# Jika file dijalankan langsung (python Main/main.py), tambahkan folder project root
# ke sys.path supaya impor absolut `Main.*` ditemukan.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Main.libs.screens.login import LoginScreen
from Main.libs.screens.signup import SignupPage
from Main.libs.screens.firstpage import GadgetHomeScreen
from Main.libs.screens.dumyhome import DataApp
from Main.libs.screens.home import HomeScreen
from kivy.properties import ListProperty
from Main.libs.screens.reviewscreen import ReviewScreen, DetailScreen, ProductCard, INITIAL_PRODUCTS
from Main.libs.screens.tabunganscreen import SavingsScreen
from Main.libs.screens.rekomendasi_gadget import GadgetRecommendationScreen
from Main.libs.screens.wishlistscreen import WishlistScreen
#from Main.libs.screens.profil import ProfileScreen



from kivy.core.window import Window
import sqlite3
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder

#module code


DB_NAME = "users.db"

Window.size = (1000, 600)

class OctaTechApp(MDApp):
    products = ListProperty(INITIAL_PRODUCTS)

    def build(self):
        self.theme_cls.theme_style = "Light"
        #init_db() # Pastikan DB siap

        # SCREEN MANAGER: Pengatur lalu lintas halaman
        self.sm = MDScreenManager()
        
        # Tambahkan layar-layar ke manager
        self.sm.add_widget(GadgetHomeScreen(name ="first_page"))

        self.sm.add_widget(LoginScreen(name="login_screen"))

        self.sm.add_widget(SignupPage(name="signup_screen"))

        self.sm.add_widget(HomeScreen(name="home_screen"))
        
        self.sm.add_widget(SavingsScreen(name="savings_screen"))
        
        self.sm.add_widget(ReviewScreen(name="review_screen"))
        
        self.sm.add_widget(DetailScreen(name="review_detail_screen"))

        self.sm.add_widget(GadgetRecommendationScreen(name="rekomendasi_gadget"))

        self.sm.add_widget(WishlistScreen(name="wishlist_screen"))
        #self.root.add_widget(GadgetRecommendationScreen(name='rekomendasi_gadget'))
        Builder.load_file("Main/libs/screens/profile.kv")
        from Main.libs.screens.profilescreen import ProfileScreen
        self.sm.add_widget(ProfileScreen(name="profile_screen"))

        
        return self.sm

    def on_start(self):
        self.filter_products("")

    def filter_products(self, query):
        grid = self.root.get_screen('review_screen').ids.product_grid
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
            detail_screen = self.root.get_screen('review_detail_screen')
            detail_screen.load_product(product)
            self.root.transition.direction = 'left'
            self.root.current = 'review_detail_screen'

    def go_back(self):
        self.root.transition.direction = 'right'
        self.root.current = 'review_screen'
        search_input = self.root.get_screen('review_screen').ids.search_input.text
        self.filter_products(search_input)

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

    def create_table(self):
        # Hanya membuat tabel, tidak mengurusi insert/select
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            conn.commit()

if __name__ == "__main__":
    # Inisialisasi DB sebelum aplikasi jalan
    from Main.libs.screens.signup import init_db
    init_db()
    OctaTechApp().run()



