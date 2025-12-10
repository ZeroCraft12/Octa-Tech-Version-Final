from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
import os
import shutil

# Mengatur ukuran window agar mirip tampilan mobile/tablet
Window.size = (1000, 600)

# Path untuk menyimpan foto profil
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILE_PHOTOS_DIR = os.path.join(MAIN_DIR, "data", "profile_photos")
os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)


# Mendefinisikan class Screen sesuai nama di file KV
class ProfileScreen(MDScreen):
    def back_to_home(self):
        self.manager.current = "home_screen"

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        # Default text jika belum login atau property kosong
        username_text = "Guest"
        
        # Cek apakah property username ada dan tidak kosong
        if hasattr(app, 'username') and app.username:
            username_text = app.username
            
        # Update label di UI
        if hasattr(self, 'ids') and 'username_label' in self.ids:
            self.ids.username_label.text = username_text

    def open_file_chooser(self):
        """Open a file chooser popup to let user pick an image, then upload it."""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        content.add_widget(filechooser)

        buttons = BoxLayout(size_hint_y=None, height='48dp', spacing='8dp', padding='8dp')
        from kivymd.uix.button import MDButton, MDButtonText
        cancel = MDButton(style='text')
        cancel_text = MDButtonText(text='Batal')
        cancel.add_widget(cancel_text)
        select = MDButton(style='filled')
        select_text = MDButtonText(text='Pilih')
        select.add_widget(select_text)
        buttons.add_widget(cancel)
        buttons.add_widget(select)
        content.add_widget(buttons)

        popup = Popup(title='Pilih Foto Profil', content=content, size_hint=(0.9, 0.9))

        def _select(*args):
            if filechooser.selection:
                src = filechooser.selection[0]
                self._upload_profile_photo(src)
                popup.dismiss()
            else:
                self._show_snackbar('Pilih file terlebih dahulu')

        cancel.bind(on_release=popup.dismiss)
        select.bind(on_release=_select)
        popup.open()

    def _upload_profile_photo(self, src_path):
        try:
            app = MDApp.get_running_app()
            username = getattr(app, 'user_nama', 'guest')
            dest = os.path.join(PROFILE_PHOTOS_DIR, f"{username}_profile.jpg")
            shutil.copy(src_path, dest)
            # set the image source in KV (id: profile_image)
            if hasattr(self, 'ids') and 'profile_image' in self.ids:
                self.ids.profile_image.source = dest
            self._show_snackbar('Foto profil berhasil diupload')
        except Exception as e:
            self._show_snackbar(f'Error upload: {e}')

    def _show_snackbar(self, text):
        snackbar = MDSnackbar(MDSnackbarText(text=text), y=20, size_hint_x=0.8)
        snackbar.open()



