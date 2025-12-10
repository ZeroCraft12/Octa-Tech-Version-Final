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


import sqlite3
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.widget import Widget

class ChangePasswordContent(BoxLayout):
    pass
    
# Menu class Screen sesuai nama di file KV
class ProfileScreen(MDScreen):
    dialog = None

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
        # from kivymd.uix.button import MDButton, MDButtonText # Already imported at top
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

    def update_username(self):
        new_username = self.ids.new_username_input.text.strip()
        if not new_username:
            self._show_snackbar("Username baru tidak boleh kosong")
            return

        app = MDApp.get_running_app()
        current_username = getattr(app, 'username', None)
        
        if not current_username:
            self._show_snackbar("Silakan login terlebih dahulu")
            return

        db_path = os.path.join(MAIN_DIR, "user_data.db")
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET username = ? WHERE username = ?", (new_username, current_username))
                if cursor.rowcount > 0:
                    conn.commit()
                    app.username = new_username
                    self.ids.username_label.text = new_username
                    self.ids.new_username_input.text = ""
                    self._show_snackbar("Username berhasil diperbarui")
                else:
                    self._show_snackbar("Gagal memperbarui username")
        except sqlite3.IntegrityError:
            self._show_snackbar("Username sudah digunakan")
        except Exception as e:
             self._show_snackbar(f"Database Error: {e}")

    def show_change_password_dialog(self):
        if not self.dialog:
            self.content_cls = ChangePasswordContent()
            self.dialog = MDDialog(
                MDDialogHeadlineText(text="Ganti Password"),
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
                        MDButtonText(text="Simpan"),
                        style="filled",
                        on_release=self.change_password
                    ),
                    spacing="8dp",
                ),
            )
        self.dialog.open()

    def change_password(self, instance):
        input1 = self.content_cls.ids.new_password
        input2 = self.content_cls.ids.confirm_password
        
        pass1 = input1.text
        pass2 = input2.text
        
        if not pass1 or not pass2:
            pass # Creating a snackbar here effectively requires passing ref or simple validation
            # For simplicity just return, but ideally showing error in dialog
            return 
            
        if pass1 != pass2:
             # Ideally show error
             return

        app = MDApp.get_running_app()
        current_username = getattr(app, 'username', None)

        if not current_username:
            self.dialog.dismiss()
            self._show_snackbar("Anda harus login")
            return

        db_path = os.path.join(MAIN_DIR, "user_data.db")
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET password = ? WHERE username = ?", (pass1, current_username))
                conn.commit()
                self._show_snackbar("Password berhasil diubah")
                input1.text = ""
                input2.text = ""
                self.dialog.dismiss()
        except Exception as e:
            self.dialog.dismiss()
            self._show_snackbar(f"Error: {e}")

    def logout(self):
        app = MDApp.get_running_app()
        # Reset user session data
        app.username = ""
        if hasattr(app, 'user_nama'):
            app.user_nama = ""
            
        # Pindah ke screen login
        self.manager.transition.direction = "right"
        self.manager.current = "hero_screen" # Atau "login_screen" tergantung flow, user minta login ulang biasanya ke hero/login. Hero lebih bersih.
        self._show_snackbar("Berhasil Logout")



