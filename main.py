import sys
import os
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import FadeTransition

# Setup Path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Main.libs.screens.login import LoginScreen
from Main.libs.screens.signup import SignupPage
from Main.libs.screens.firstpage import TeamScreen, HeroScreen
from Main.libs.screens.home import HomeScreen
from Main.libs.screens.reviewscreen import ReviewScreen, DetailScreen, ProductCard, INITIAL_PRODUCTS
from Main.libs.screens.tabunganscreen import SavingsScreen
from Main.libs.screens.rekomendasi_gadget import GadgetRecommendationScreen
from Main.libs.screens.wishlistscreen import WishlistScreen

from kivy.properties import ListProperty, StringProperty
import sqlite3
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.text import LabelBase

script_dir = os.path.dirname(os.path.abspath(__file__))
LabelBase.register(name="Montserrat", fn_regular=os.path.join(script_dir, "Main/assets/fonts/Montserrat-Bold.ttf"))
LabelBase.register(name="Poppins", fn_regular=os.path.join(script_dir, "Main/assets/fonts/Poppins-Medium.ttf"))
LabelBase.register(name="Poppins-Bold", fn_regular=os.path.join(script_dir, "Main/assets/fonts/Poppins-Bold.ttf"))
LabelBase.register(name="LeagueSpartan", fn_regular=os.path.join(script_dir, "Main/assets/fonts/LeagueSpartan-Bold.ttf"))

DB_NAME = "users.db"
Window.size = (1920, 1080) 

# 1. SPLASH OCTA (2.png -> 3.png)
class OctaSplash1(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.go_next, 1.5) # Auto pindah setelah 1.5 detik

    def go_next(self, dt):
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = "octa_2"

    def build_ui(self):
        pass 

class OctaSplash2(MDScreen):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.manager.transition = FadeTransition(duration=0.5)
            self.manager.current = "unesa_1"
            return True
        return super().on_touch_down(touch)

# 2. SPLASH UNESA (4.png -> 5.png)
class UnesaSplash1(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.go_next, 1.5)

    def go_next(self, dt):
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = "unesa_2"

class UnesaSplash2(MDScreen):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.manager.transition = FadeTransition(duration=0.5)
            self.manager.current = "team_screen"
            return True
        return super().on_touch_down(touch)


# Main App
class OctaTechApp(MDApp):
    username = StringProperty("")
    products = ListProperty(INITIAL_PRODUCTS)
    search_trigger = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        # FadeTransition
        self.sm = MDScreenManager(transition=FadeTransition())
        
        # Screen: Octa 1 (Icon)
        s1 = OctaSplash1(name="octa_1")
        layout1 = MDBoxLayout(md_bg_color=[1,1,1,1]) # Putih
        layout1.add_widget(Image(source=os.path.join(script_dir, "2.png"), allow_stretch=True, keep_ratio=True))
        s1.add_widget(layout1)
        self.sm.add_widget(s1)

        # Screen: Octa 2 (Text)
        s2 = OctaSplash2(name="octa_2")
        layout2 = MDBoxLayout(md_bg_color=[1,1,1,1])
        layout2.add_widget(Image(source=os.path.join(script_dir, "3.png"), allow_stretch=True, keep_ratio=True))
        s2.add_widget(layout2)
        self.sm.add_widget(s2)

        # Screen: Unesa 1 (Logo)
        s3 = UnesaSplash1(name="unesa_1")
        layout3 = MDBoxLayout(md_bg_color=[1,1,1,1])
        layout3.add_widget(Image(source=os.path.join(script_dir, "4.png"), allow_stretch=True, keep_ratio=True))
        s3.add_widget(layout3)
        self.sm.add_widget(s3)

        # Screen: Unesa 2 (DS)
        s4 = UnesaSplash2(name="unesa_2")
        layout4 = MDBoxLayout(md_bg_color=[1,1,1,1])
        layout4.add_widget(Image(source=os.path.join(script_dir, "5.png"), allow_stretch=True, keep_ratio=True))
        s4.add_widget(layout4)
        self.sm.add_widget(s4)

        # --- 2. SETUP SCREEN DARI FIRSTPAGE.PY ---
        self.sm.add_widget(TeamScreen(name="team_screen")) # Slide Tim
        
        hero = HeroScreen(name="hero_screen")

        self.sm.add_widget(hero)

        # --- 3. SETUP SCREEN LAINNYA ---
        self.sm.add_widget(LoginScreen(name="login_screen"))
        self.sm.add_widget(SignupPage(name="signup_screen"))
        self.sm.add_widget(HomeScreen(name="home_screen"))
        self.sm.add_widget(SavingsScreen(name="savings_screen"))
        self.sm.add_widget(ReviewScreen(name="review_screen"))
        self.sm.add_widget(DetailScreen(name="review_detail_screen"))
        self.sm.add_widget(GadgetRecommendationScreen(name="rekomendasi_gadget"))
        self.sm.add_widget(WishlistScreen(name="wishlist_screen"))
        
        Builder.load_file(os.path.join(script_dir, "Main/libs/screens/profile.kv"))
        from Main.libs.screens.profilescreen import ProfileScreen
        self.sm.add_widget(ProfileScreen(name="profile_screen"))

        return self.sm

    def on_start(self):
        if self.root.has_screen('review_screen'):
            self.filter_products("")

    def filter_products(self, query):
        if self.search_trigger:
            self.search_trigger.cancel()
        self.search_trigger = Clock.schedule_once(lambda dt: self._perform_filter_products(query), 0.3)

    def _perform_filter_products(self, query):
        print(f"DEBUG: _perform_filter_products called with query='{query}'")
        if not self.root.has_screen('review_screen'):
            print("DEBUG: Screen not found")
            return
        
        grid = self.root.get_screen('review_screen').ids.product_grid
        grid.clear_widgets()
        query = query.lower()
        
        print(f"DEBUG: Total products: {len(self.products)}")
        for product in self.products:
            # Safer access
            p_name = str(product.get('name', '')).lower()
            p_cat = str(product.get('category', '')).lower()
            
            if query in p_name or query in p_cat:
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
        try:
            search_input = self.root.get_screen('review_screen').ids.search_input.text
            self.filter_products(search_input)
        except:
            pass

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
    from Main.libs.screens.signup import init_db
    init_db()
    OctaTechApp().run()