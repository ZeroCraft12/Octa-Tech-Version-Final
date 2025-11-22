from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivymd.uix.button import MDIconButton

class GradientLayout(MDFloatLayout):
    def __init__(self, warna_atas, warna_bawah, **kwargs):
        super().__init__(**kwargs)
        self.warna_atas = warna_atas
        self.warna_bawah = warna_bawah
        self.bind(pos=self.update_bg, size=self.update_bg)
        self.update_bg()

    def update_bg(self, *args):
        texture = Texture.create(size=(1, 2), colorfmt='rgba')
        c1 = [int(c * 255) for c in self.warna_bawah]
        c2 = [int(c * 255) for c in self.warna_atas]
        buf = bytes(c1 + c2)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.before.clear()
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size, texture=texture)


class HalamanScrollGradient(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # A. Background Gradasi
        bg = GradientLayout(
            warna_atas=[0.1, 0.2, 0.5, 1],
            warna_bawah=[0.3, 0.0, 0.3, 1]
        )
        self.add_widget(bg)

        # B. ScrollView
        scroll = ScrollView(
            pos_hint={"center_x": .5, "center_y": .5},
            do_scroll_x=False,
            do_scroll_y=True
        )

        # C. Kontainer Konten
        kontainer = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True, 
            padding="20dp",
            spacing="20dp"
        )

        # D. JUDUL (PERBAIKAN DI SINI)
        # H4 diganti menjadi Headline dengan role Medium
        judul = MDLabel(
            text="Kurikulum Belajar", 
            theme_text_color="Custom", 
            text_color=[1,1,1,1], 
            font_style="Headline",   # Ganti H4 jadi Headline
            role="Medium",           # Tambahkan role
            halign="center",
            size_hint_y=None,
            height="100dp"
        )
        kontainer.add_widget(judul)

        topik_datascience = [
            "Pengenalan Python", "Statistik Dasar", "Pandas & NumPy",
            "Visualisasi Data", "Machine Learning", "Deep Learning",
            "Natural Language Processing", "Computer Vision", "Big Data",
            "Deployment Model", "Ethics in AI", "Capstone Project"
        ]

        for topik in topik_datascience:
            card = MDCard(
                size_hint_y=None,
                height="80dp",
                # radius=[15], # Di KivyMD 2.0 radius kadang berbeda penulisan, tapi ini aman
                style="elevated", # Style kartu MD3
                md_bg_color=[1, 1, 1, 0.1], 
                padding="10dp"
            )
            
            # SUB-JUDUL (PERBAIKAN DI SINI)
            # H6 diganti menjadi Title dengan role Medium
            lbl = MDLabel(
                text=topik,
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                font_style="Title",  # Ganti H6 jadi Title
                role="Medium",       # Tambahkan role
                valign="center"
            )
            
            icon = MDIconButton(
                icon="chevron-right",
                theme_text_color="Custom",
                text_color=[1,1,1,1],
                pos_hint={"center_y": .5}
            )

            card.add_widget(lbl)
            card.add_widget(icon)
            kontainer.add_widget(card)

        scroll.add_widget(kontainer)
        self.add_widget(scroll)


class AplikasiSaya(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue" # MD3 Menggunakan palette berbeda, tapi ini fallback aman
        return HalamanScrollGradient()

if __name__ == '__main__':
    AplikasiSaya().run()