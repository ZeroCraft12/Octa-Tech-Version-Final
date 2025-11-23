from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
# UBAH DISINI: Ganti MDButtonText dengan MDButtonIcon
from kivymd.uix.button import MDButton, MDButtonIcon
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation

class GadgetHomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_image = 0
        self.images = [
            "D:\Project Pemdas Octatech test\Assets\loginpage\Latarbelakang.jpg",
            "D:\Project Pemdas Octatech test\Assets\loginpage\Latarbelakang.jpg",
            "D:\Project Pemdas Octatech test\Assets\loginpage\Latarbelakang.jpg"
        ]
        
        # Background gradient
        with self.canvas.before:
            Color(0.09, 0.29, 0.44, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            Color(0.07, 0.45, 0.53, 1)
            self.bg_rect2 = Rectangle(pos=(self.width * 0.5, 0), size=(self.width * 0.5, self.height))
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=[60, 80, 60, 60],
            spacing=40
        )
        
        # Header section
        header_layout = MDBoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint_y=0.3 
        )
        
        title = MDLabel(
            text='Cari gadget terbaik untukmu!',
            font_style='Display',
            role='large',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            bold=True,
            size_hint_y= 0.4,
            height=120
        )
        
        subtitle = MDLabel(
            text='Menemukan rekomendasi gadget terbaik untuk menunjang dunia\nperskuliahanmu, Mudah, Cepat, dan Menyenangkan',
            theme_text_color='Custom',
            text_color=(0.9, 0.9, 0.9, 1),
            font_style='Body',
            role='large',
            size_hint_y=None,
            height=60
        )
        
        header_layout.add_widget(title)
        header_layout.add_widget(subtitle)
        
        # Image slider section
        self.slider_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint_y=0.5,
            padding=[0, 20, 0, 20]
        )
        
        # Create image widgets
        self.image_widgets = []
        for i in range(3):
            img_container = MDBoxLayout(
                size_hint_x=0.33,
                padding=10
            )
            
            with img_container.canvas.before:
                Color(1, 1, 1, 1)
                img_container.rect = RoundedRectangle(
                    pos=img_container.pos,
                    size=img_container.size,
                    radius=[15]
                )
            
            img_container.bind(pos=self.update_img_rect, size=self.update_img_rect)
            
            img = Image(
                source=self.images[i],
                allow_stretch=True,
                keep_ratio=True
            )
            
            img_container.add_widget(img)
            self.slider_layout.add_widget(img_container)
            self.image_widgets.append(img_container)
        
        # Button section
        button_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            padding=[0, 20, 0, 0]
        )
        
        # Spacer agar tombol ada di kanan
        spacer = MDBoxLayout(size_hint_x=0.8) # Saya perbesar sedikit spacernya agar tombol lebih ke kanan
        
        button_container = MDBoxLayout(
            size_hint_x=0.01,
            padding=[0, 0, 0, 0]
        )
        
        # --- BAGIAN YANG DIUBAH ---
        btn = MDButton(
            style='elevated',
            theme_bg_color='Custom',
            md_bg_color=(0.13, 0.82, 0.82, 1),
            size_hint=(None, None), # Ubah size hint agar tombol mengikuti ukuran icon
            width="64dp", # Lebar tombol
            height="40dp", # Tinggi tombol
            radius=[5],   # Membuat sudut tombol agak membulat (opsional)
            pos_hint={"center_x": .5, "center_y": .5}
        )
        
        # Menggunakan MDButtonIcon, bukan MDButtonText
        btn_icon = MDButtonIcon(
            icon='arrow-right',
            theme_icon_color='Custom',
            icon_color=(1, 1, 1, 1),
            font_size="60"
            #height="1000dp" # Ukuran Icon
        )
        
        btn.add_widget(btn_icon)
        # --------------------------
        
        button_container.add_widget(btn)
        
        button_layout.add_widget(spacer)
        button_layout.add_widget(button_container)
        
        # Add all to main layout
        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.slider_layout)
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
        
        # Start auto slide
        Clock.schedule_interval(self.auto_slide, 3)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_rect2.pos = (self.width * 0.5, 0)
        self.bg_rect2.size = (self.width * 0.5, self.height)
    
    def update_img_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def auto_slide(self, dt):
        # Rotate images
        self.current_image = (self.current_image + 1) % len(self.images)
        
        # Update images with animation
        for i, img_container in enumerate(self.image_widgets):
            new_index = (self.current_image + i) % len(self.images)
            img_container.children[0].source = self.images[new_index]
            
            # Add slide animation
            anim = Animation(opacity=0, duration=0.3)
            anim += Animation(opacity=1, duration=0.3)
            anim.start(img_container)

class GadgetApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        
        Window.size = (1000, 600)
        
        return GadgetHomeScreen()

if __name__ == '__main__':
    GadgetApp().run()