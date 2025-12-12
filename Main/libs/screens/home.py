from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ColorProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

# --- WARNA DI PYTHON (Bisa diakses juga di KV jika diimport/set dynamic) ---
COLOR_OCTA_BLUE = "#1A2B58"
COLOR_BG_GREY = "#F5F5F5"
COLOR_WHITE = "#FFFFFF"
COLOR_ACCENT = "#FFD700"

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Carousel kivy.uix.carousel.Carousel

<LogoButton>:
    size_hint: None, None
    size: dp(40), dp(40)
    pos_hint: {"center_y": 0.5}

<HeroSlide>:
    size_hint_y: None
    height: dp(160)
    radius: [dp(15),]
    elevation: 2
    padding: dp(20)
    spacing: dp(10)
    theme_bg_color: "Custom"
    md_bg_color: root.bg_color
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDLabel:
            text: root.title
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Headline"
            role: "small"
            bold: True
            
        MDLabel:
            text: root.subtitle
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Body"
            role: "medium"

<ModernMenuButton>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(110)
    radius: [dp(15),]
    elevation: 2
    ripple_behavior: True
    padding: dp(10)
    spacing: dp(5)
    theme_bg_color: "Custom"
    md_bg_color: root.icon_bg_color

    MDBoxLayout:
        size_hint: None, None
        size: dp(50), dp(50)
        radius: [dp(25),]
        # md_bg_color: [1, 1, 1, 0.2]  <-- Removed white background
        pos_hint: {"center_x": 0.5}
        
        MDIcon:
            icon: root.icon_name
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            font_size: "32sp"
            halign: "center"

    MDLabel:
        text: root.text_label
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        bold: True
        font_style: "Label"
        role: "large"
        adaptive_height: True

<FeaturedProductCard>:
    orientation: "vertical"
    size_hint: None, None
    size: dp(160), dp(220)
    radius: [dp(15),]
    elevation: 2
    ripple_behavior: True
    theme_bg_color: "Custom"
    md_bg_color: 1, 1, 1, 1
    padding: dp(0)
    
    MDBoxLayout:
        size_hint_y: 0.6
        radius: [dp(15), dp(15), 0, 0]
        Image:
            source: root.product_image
            keep_ratio: True
            allow_stretch: True
            
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(10)
        size_hint_y: 0.4
        
        MDLabel:
            text: root.product_name
            bold: True
            font_style: "Label"
            role: "large"
            max_lines: 1
            shorten: True
            adaptive_height: True
            
        MDLabel:
            text: root.product_category
            font_style: "Body"
            role: "small"
            theme_text_color: "Secondary"
            adaptive_height: True
            
        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(2)
            adaptive_height: True
            
            MDIconButton:
                icon: "star"
                theme_icon_color: "Custom"
                icon_color: get_color_from_hex("#FFD700")
                font_size: "14sp"
                size_hint: None, None
                size: dp(16), dp(16)
                pos_hint: {"center_y": 0.5}
                
            MDLabel:
                text: root.product_rating
                font_style: "Label"
                role: "small"
                theme_text_color: "Secondary"
                adaptive_height: True
                pos_hint: {"center_y": 0.5}

<HomeScreen>:
    md_bg_color: get_color_from_hex("#F5F5F5")
    
    MDBoxLayout:
        orientation: "vertical"
        
        # --- HEADER ---
        MDBoxLayout:
            orientation: "horizontal"
            adaptive_height: True
            padding: dp(20), dp(10)
            spacing: dp(10)
            md_bg_color: 1, 1, 1, 1
            
            LogoButton:
                source: "Main/assets/Images/logonontext.png"
                
            MDLabel:
                text: "OctaTech."
                bold: True
                theme_text_color: "Primary"
                font_style: "Title"
                role: "medium"
                adaptive_width: True
                pos_hint: {"center_y": 0.5}
                
            MDLabel: # Spacer
            
            MDIconButton:
                icon: "account-circle-outline"
                on_release: root.to_profile()
                
            
                
        # --- CONTENT ---
        ScrollView:
            bar_width: 0
            
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20), dp(10)
                spacing: dp(20)
                adaptive_height: True
                
                # Greeting
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(5)
                    
                    MDLabel:
                        id: lbl_hello
                        text: "Hai, User!"
                        font_name:"Poppins-Bold"
                        font_style: "Headline"
                        role: "small"
                        bold: True
                        theme_text_color: "Primary"
                        adaptive_height: True
                        
                    MDLabel:
                        text: "Temukan gadget impianmu hari ini."
                        font_style: "Body"
                        font_name:"LeagueSpartan"
                        role: "medium"
                        theme_text_color: "Secondary"
                        adaptive_height: True
                        
                # Hero Carousel Container
                MDCard:
                    size_hint_y: None
                    height: dp(160)
                    radius: [dp(15),]
                    elevation: 2
                    id: carousel_container
                    # Carousel removed from here to be added safely in code or strict KV if 'clip_children' issue persists
                    # We will add Carousel dynamically in python to be safe OR use Carousel directly here
                    
                    Carousel:
                        id: hero_carousel
                        loop: True
                        anim_move_duration: 0.5
                        
                # Menu Grid
                MDGridLayout:
                    cols: 2
                    adaptive_height: True
                    spacing: dp(15)
                    
                    ModernMenuButton:
                        icon_name: "compass-outline"
                        text_label: "Rekomendasi"
                        font_name:"Poppins-Bold"
                        icon_bg_color: get_color_from_hex("#E91E63")
                        on_release: root.to_rekomendasi()
                        
                    ModernMenuButton:
                        icon_name: "piggy-bank-outline"
                        text_label: "Tabungan"
                        font_name:"Poppins-Bold"
                        icon_bg_color: get_color_from_hex("#4CAF50")
                        on_release: root.to_savings()
                        
                    ModernMenuButton:
                        icon_name: "star-outline"
                        text_label: "Review"
                        font_name:"Poppins-Bold"
                        icon_bg_color: get_color_from_hex("#FF9800")
                        on_release: root.to_review()
                        
                    ModernMenuButton:
                        icon_name: "heart-outline"
                        pos_hint: {"center_x": 0.5}
                        text_label: "Wishlist"
                        font_name:"Poppins-Bold"
                        icon_bg_color: get_color_from_hex("#9C27B0")
                        on_release: root.to_wishlist()
                        
                # Featured Text
                MDLabel:
                    text: "Produk Unggulan"
                    font_name:"Poppins-Bold"
                    bold: True
                    font_style: "Title"
                    role: "medium"
                    adaptive_height: True
                    theme_text_color: "Primary"
                    
                # Featured Scroll
                ScrollView:
                    size_hint_y: None
                    height: dp(230)
                    do_scroll_x: True
                    do_scroll_y: False
                    bar_width: 0
                    
                    MDBoxLayout:
                        id: product_row
                        orientation: "horizontal"
                        padding: dp(5), dp(5)
                        spacing: dp(15)
                        adaptive_width: True
                
                MDLabel:
                    size_hint_y: None
                    height: dp(20)
'''

Builder.load_string(KV)

# --- CLASSES ---

class LogoButton(ButtonBehavior, Image):
    pass

class HeroSlide(MDCard):
    title = StringProperty("")
    subtitle = StringProperty("")
    bg_color = ColorProperty([0,0,0,0])

class ModernMenuButton(MDCard):
    icon_name = StringProperty("")
    text_label = StringProperty("")
    icon_bg_color = ColorProperty([0,0,0,0])

class FeaturedProductCard(MDCard):
    product_image = StringProperty("")
    product_name = StringProperty("")
    product_category = StringProperty("")
    product_rating = StringProperty("0.0")
    product_id = ObjectProperty(None)
    
    def on_release(self):
        app = MDApp.get_running_app()
        if hasattr(app, 'show_product_detail') and self.product_id:
            app.show_product_detail(self.product_id)

from kivy.clock import Clock

class HomeScreen(MDScreen):
    built_once = False
    _carousel_event = None

    def on_enter(self):
        # Update username
        app = MDApp.get_running_app()
        if hasattr(app, "user_nama"):
            name = app.user_nama if app.user_nama else "User"
            self.ids.lbl_hello.text = f"Hai, {name}!"
            
        if not self.built_once:
            self.setup_carousel()
            self.load_featured_products()
            self.built_once = True
            
            # Apply clip_children manually if needed for container
            self.ids.carousel_container.clip_children = True
        
        # Start Auto Scroll
        self._start_auto_scroll()

    def on_leave(self):
        self._stop_auto_scroll()

    def _start_auto_scroll(self):
        self._stop_auto_scroll() # Ensure no duplicate
        # Scroll every 3 seconds
        self._carousel_event = Clock.schedule_interval(self._scroll_carousel, 3)

    def _stop_auto_scroll(self):
        if self._carousel_event:
            self._carousel_event.cancel()
            self._carousel_event = None

    def _scroll_carousel(self, dt):
        carousel = self.ids.hero_carousel
        carousel.load_next(mode='next')

    def setup_carousel(self):
        # We need to add slides dynamically or definition in KV? 
        # Since usage is simple, let's add them here to keep data separate from view
        carousel = self.ids.hero_carousel
        
        slide1 = HeroSlide(
            title="Kepercayaan Pelanggan", 
            subtitle="Kami selalu berkomitmen untuk memberikan pelayanan terbaik.",
            bg_color=get_color_from_hex("#3F51B5")
        )
        slide2 = HeroSlide(
            title="Rekomendasi Terbaik", 
            subtitle="Cari tahu gadget yang cocok untukmu.",
            bg_color=get_color_from_hex("#009688")
        )
        slide3 = HeroSlide(
            title="OctaTech Savings", 
            subtitle="Mulai menabung untuk gadget impian.",
            bg_color=get_color_from_hex("#1A2B58")
        )
        
        carousel.add_widget(slide1)
        carousel.add_widget(slide2)
        carousel.add_widget(slide3)

    def load_featured_products(self):
        app = MDApp.get_running_app()
        products_to_show = getattr(app, 'products', [])[:5]
        row = self.ids.product_row
        row.clear_widgets()
        
        if not products_to_show:
            lbl = MDLabel(text="Belum ada data produk.", adaptive_width=True)
            row.add_widget(lbl)
        else:
            for p in products_to_show:
                # Calculate rating string
                rating_val = 0
                reviews = p.get('reviews', [])
                if reviews:
                    total = sum(r['rating'] for r in reviews)
                    rating_val = round(total / len(reviews), 1)
                
                card = FeaturedProductCard()
                card.product_image = p.get('image', '')
                card.product_name = p.get('name', 'Produk')
                card.product_category = p.get('category', 'Kategori')
                card.product_rating = str(rating_val)
                card.product_id = p.get('id')
                
                row.add_widget(card)

    def to_profile(self):
        if self.manager:
            self.manager.current = "profile_screen"
            self.manager.transition.direction = "left"

    def to_rekomendasi(self):
        if self.manager:
            self.manager.current = "rekomendasi_gadget"
            self.manager.transition.direction = "left"

    def to_review(self):
        if self.manager:
            self.manager.current = "review_screen"
            self.manager.transition.direction = "left"

    def to_savings(self):
        if self.manager:
            self.manager.current = "savings_screen"
            self.manager.transition.direction = "left"

    def to_wishlist(self):
        if self.manager:
            self.manager.current = "wishlist_screen"
            self.manager.transition.direction = "left"

    def do_logout(self):
        self._stop_auto_scroll()
        MDApp.get_running_app().stop()
