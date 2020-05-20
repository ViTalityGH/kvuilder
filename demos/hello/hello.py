import os

from glob import glob
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform as _os
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.material_resources import DEVICE_TYPE

from libs.components import messagebox

class MainApp(MDApp):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        Window.bind(
            on_request_close=self.on_request_close
        )
        Window.softinput_mode = 'below_target'
        self.screen_manager = ScreenManager()
        self.dialog_exit = self.create_dialog_exit()

    def get_stylesheets(self):
        path = os.path.join("libs", "stylesheet", DEVICE_TYPE, "**/*.kv")
        stylesheets = glob(path)
        return stylesheets

    def load_stylesheets(self):
        for f in self.get_stylesheets():
            Builder.load_file(f)

    def get_wizard_screen(self):
        from libs.screens.wizard.view import WizardScreen
        from libs.components.wizard import MDSwiperPagination
        
        screen = WizardScreen()
        wizard_manager = screen.ids.wizard_manager
        paginator = MDSwiperPagination()
        paginator.screens = wizard_manager.screen_names
        paginator.manager = wizard_manager
        wizard_manager.paginator = paginator
        screen.add_widget(paginator)
        return screen

    def get_login_screen(self):
        from libs.screens.login.view import LoginScreen

        screen = LoginScreen()
        return screen

    def get_main_screen(self):
        from libs.screens.main.view import MainScreen

        screen = MainScreen()
        return screen

    def get_screen(self):
        screen = self.get_login_screen()
        return screen

    def build(self):
        self.load_stylesheets()
        screen = self.get_screen()
        self.screen_manager.add_widget(screen)
        return self.screen_manager

    def create_menu_settings(self):
        root = self.screen_manager.get_screen("main").ids
        caller = root.nav_content.ids.setting_btn
        items = [
            {
                "icon": "account-badge",
                "text": "Account"
            },
            {
                "icon": "exit-to-app",
                "text": "Logout"
            }
        ]
        menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        menu.set_menu_properties(0.5)
        return menu

    def show_menu_settings(self):
        menu = self.create_menu_settings()
        Window.fbind("on_resize", self.on_resize_menu_settings, menu)
        Clock.schedule_once(lambda x: menu.open(), 0)

    def on_resize_menu_settings(self, *args):
        current = args[0]
        current.dismiss()

    def create_dialog_exit(self):
        btn_kembali = MDFlatButton(text="Kembali")
        btn_kembali.bind(on_release=self.handle_action_exit_button)
        btn_ya = MDRaisedButton(text="Ya")
        btn_ya.bind(on_release=self.handle_action_exit_button)
        dialog = messagebox.InfoMessage(
            title="Info",
            text="Apakah anda yakin ingin keluar?",
            buttons=[
                btn_kembali,
                btn_ya
            ]
        )
        return dialog

    def handle_action_exit_button(self, *args):
        print("Button args:", args)

    def on_request_close(self, *args):
        self.dialog_exit.open()
        return True
