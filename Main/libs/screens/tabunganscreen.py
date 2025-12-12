from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
# Perbaikan: Hapus MDDialogContent dari import karena tidak dikenali di versi Anda
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty, NumericProperty, ListProperty
from datetime import datetime
import os

# Load the KV file at module import time
kv_file = os.path.join(os.path.dirname(__file__), 'savingsscreen.kv')
Builder.load_file(kv_file)

class HistoryItem(MDListItem):
    amount_text = StringProperty()
    date_text = StringProperty()
    is_positive = NumericProperty(1)

class EditGoalContent(MDBoxLayout):
    pass

class SavingsScreen(MDScreen):
    goal_name = StringProperty('Belum Ada Target')
    target_amount = NumericProperty(0)
    current_amount = NumericProperty(0)
    progress_percent = NumericProperty(0)
    
    history_data = ListProperty([])

    def on_enter(self):
        quick_amounts = [10000, 25000, 50000, 100000, 250000, 500000]
        grid = self.ids.quick_grid
        grid.clear_widgets()
        
        for amt in quick_amounts:
            # Menggunakan style 'outlined' agar terlihat seperti chip/kotak
            # size_hint_x=1 agar memenuhi kolom grid
            btn = MDButton(style="outlined", size_hint_x=1)
            btn.bind(on_release=lambda x, amount=amt: self.deposit(amount))
            
            # Format text tombol: +10k, +25k
            display_text = f"+{int(amt/1000)}k"
            btn_text = MDButtonText(text=display_text, pos_hint={"center_x": .5, "center_y": .5})
            
            btn.add_widget(btn_text)
            grid.add_widget(btn)
        
        self.update_ui()

    def update_ui(self, *args):
        if self.target_amount > 0:
            self.progress_percent = (self.current_amount / self.target_amount) * 100
        else:
            self.progress_percent = 0
            
        history_container = self.ids.history_list
        history_container.clear_widgets()
        
        for item in self.history_data:
            is_pos = 1 if item['amount'] > 0 else 0
            sign = "+" if is_pos else ""
            item_widget = HistoryItem(
                amount_text=f"{sign}{self.format_rupiah(item['amount'])}",
                date_text=item['date'],
                is_positive=is_pos
            )
            history_container.add_widget(item_widget)

    def deposit(self, amount):
        self.current_amount += amount
        # Menambah di index 0 agar muncul paling atas
        self.history_data.insert(0, {
            'amount': amount, 
            'date': datetime.now().strftime("%d %b %Y")
        })
        self.update_ui()

    def add_manual_deposit(self):
        field = self.ids.input_amount
        try:
            amount = int(field.text)
            if amount > 0:
                self.deposit(amount)
                field.text = ""
        except ValueError:
            pass 

    def withdraw_money(self):
        amount = 500000 
        if self.current_amount >= amount:
            self.current_amount -= amount
            self.history_data.insert(0, {
                'amount': -amount, 
                'date': datetime.now().strftime("%d %b %Y")
            })
            self.update_ui()

    def reset_data(self):
        self.current_amount = 0
        self.history_data = []
        self.update_ui()

    def open_edit_dialog(self):
        self.dialog_content = EditGoalContent()
        self.dialog_content.ids.edit_name.text = self.goal_name
        self.dialog_content.ids.edit_target.text = str(int(self.target_amount))

        # PERBAIKAN DI SINI:
        # Langsung masukkan self.dialog_content sebagai argumen kedua tanpa MDDialogContent wrapper
        self.edit_dialog = MDDialog(
            MDDialogHeadlineText(text="Edit Goal"),
            self.dialog_content, 
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Batal"),
                    style="text",
                    on_release=lambda x: self.edit_dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Simpan"),
                    style="text",
                    on_release=self.save_edit_goal
                ),
                spacing="8dp",
            ),
            size_hint=(0.9, None),
        )
        self.edit_dialog.open()

    def save_edit_goal(self, instance):
        new_name = self.dialog_content.ids.edit_name.text
        new_target = self.dialog_content.ids.edit_target.text
        
        if new_name and new_target:
            self.goal_name = new_name
            try:
                self.target_amount = int(new_target)
                self.update_ui()
                self.edit_dialog.dismiss()
            except ValueError:
                pass

    def format_rupiah(self, value):
        return "Rp {:,.0f}".format(value).replace(",", ".")
    
    def back_to_home(self):
        self.manager.current = "home_screen"
