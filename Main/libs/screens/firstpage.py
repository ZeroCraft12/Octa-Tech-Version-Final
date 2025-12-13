import os
import sys
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp

# --- SETUP PATH ---
current_file_path = os.path.abspath(__file__)
screens_dir = os.path.dirname(current_file_path)
libs_dir = os.path.dirname(screens_dir)
MAIN_DIR = os.path.dirname(libs_dir)
ASSETS_DIR = os.path.join(MAIN_DIR, "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "Images")

from kivy.properties import StringProperty
from kivymd.uix.card import MDCard

# ... (rest of imports)

# Normalize paths for KV to avoid issues
IMG_DIR_KV = IMG_DIR.replace("\\", "/") + "/"

class TeamCard(MDCard):
    name = StringProperty("")
    image_source = StringProperty("")

KV = f'''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TeamCard>:
    orientation: "vertical"
    size_hint: None, None
    size: "160dp", "240dp"
    radius: [16, 16, 16, 16]
    elevation: 2
    md_bg_color: [1, 1, 1, 1]
    padding: "8dp"
    spacing: "8dp"
    
    FitImage:
        source: root.image_source
        radius: [12, 12, 12, 12]
        size_hint_y: 0.75

    MDLabel:
        text: root.name
        halign: "center"
        font_style: "Label"
        role: "large"
        bold: True
        adaptive_height: True
        theme_text_color: "Primary"


<TeamScreen>:
    md_bg_color: get_color_from_hex("#008AC5")
    
    FitImage:
        source: "{IMG_DIR_KV}welcome page.jpg"
        size_hint: 1, 1
        pos_hint: {{"center_x": .5, "center_y": .5}}
        opacity: 0.3

    MDBoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "24dp"
        pos_hint: {{"center_x": .5, "center_y": .5}}
        adaptive_height: True

        MDLabel:
            text: "Meet The Team"
            halign: "center"
            font_style: "Display"
            role: "small"
            bold: True
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            adaptive_height: True

        MDBoxLayout:
            orientation: "horizontal"
            adaptive_size: True
            spacing: "16dp"
            pos_hint: {{"center_x": .5}}
            
            TeamCard:
                image_source: "{IMG_DIR_KV}p_Fathan.jpg"
                name: "Fathan Faqrurozi"
            
            TeamCard:
                image_source: "{IMG_DIR_KV}p_Irfan.jpeg"
                name: "M. Irfan Pratama"
            
            TeamCard:
                image_source: "{IMG_DIR_KV}p_Zai.png"
                name: "M. Zaidan Alfaizi"

        MDLabel:
            text: "Dosen Pengampu:\\nDr. Atik Wintarti, M.Kom."
            font_name: "Poppins-Bold"
            halign: "center"
            font_style: "Body"
            role: "medium"
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 0.8]
            adaptive_height: True

<HeroScreen>:
    md_bg_color: [1, 1, 1, 1]

    FitImage:
        source: "{IMG_DIR_KV}welcome page.jpg"
        size_hint: 1, 1
        pos_hint: {{"center_x": .5, "center_y": .5}}
        
    MDBoxLayout:
        orientation: "vertical"
        padding: "40dp"
        spacing: "20dp"
        
        MDLabel:
            text: "Find Your Dream Gadget"
            font_name: "Montserrat"
            font_style: "Display"
            role: "medium"
            bold: True
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            adaptive_height: True
            line_height: 1.1

        MDLabel:
            text: "Rekomendasi gadget terbaik untuk mahasiswa.\\nCepat, Tepat, dan Terpercaya."
            font_name: "LeagueSpartan"
            font_style: "Headline"
            role: "small"
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 0.9]
            adaptive_height: True

        # 3 Image Grid
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "180dp"
            spacing: "10dp"
            
            MDCard:
                radius: [12, 12, 12, 12]
                elevation: 3
                
                FitImage:
                    source: "{IMG_DIR_KV}slider1.jpg"
                    radius: [12, 12, 12, 12]
            
            MDCard:
                radius: [12, 12, 12, 12]
                elevation: 3
                
                FitImage:
                    source: "{IMG_DIR_KV}slider2.jpg"
                    radius: [12, 12, 12, 12]
            
            MDCard:
                radius: [12, 12, 12, 12]
                elevation: 3
                
                FitImage:
                    source: "{IMG_DIR_KV}slider3.jpg"
                    radius: [12, 12, 12, 12]
            MDCard:
                radius: [12, 12, 12, 12]
                elevation: 3
                
                FitImage:
                    source: "{IMG_DIR_KV}slider4.jpg"
                    radius: [12, 12, 12, 12]    
        
        MDWidget: # Spacer

        MDButton:
            style: "filled"
            theme_bg_color: "Custom"
            md_bg_color: [1, 1, 1, 1]
            theme_width: "Custom"
            width: "220dp"
            height: "56dp"
            on_release: root.go_to_login()
            
            MDButtonIcon:
                icon: "arrow-right"
                theme_icon_color: "Custom"
                icon_color: get_color_from_hex("#008AC5")
                pos_hint: {{"center_y": .5}}
                
            MDButtonText:
                text: "Get Started"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#008AC5")
                font_style: "Title"
                role: "medium"
                pos_hint: {{"center_y": .5}}
'''

Builder.load_string(KV)

class TeamScreen(MDScreen):
    def on_touch_down(self, touch):
        # Allow clicking anywhere to proceed, but prioritize logic
        if self.collide_point(*touch.pos):
            # If touch not handled by children (unlikely here since cards don't have actions), proceed
            # But wait/check if user wants to just view. 
            # Original code had tap anywhere to go next. Let's keep it but maybe only on background?
            # For modern UX, maybe a button is better, but user asked for previous behavior or similar.
            # Let's add a delay or check if it's a valid touch.
            # Actually, standard flow: Wait or Tap. 
            # Let's bind a tap to the screen to move to hero.
            if super().on_touch_down(touch):
                return True
            
            if self.manager:
                self.manager.transition.direction = "left"
                self.manager.current = "hero_screen"
            return True
        return super().on_touch_down(touch)

class HeroScreen(MDScreen):
    def go_to_login(self):
        if self.manager:
            self.manager.transition.direction = "left"
            # As per main.py, login screen name is 'login_screen'
            # But user might have 'hero_screen' -> 'login_screen' flow in main.py
            self.manager.current = "login_screen"

