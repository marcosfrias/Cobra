import os

from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationrail import MDNavigationRailItem
from pdf_viewer import PDFViewerScreen
from kivy.core.image import Image as CoreImage
from web import WebScreen
from graphics_screen import GraphicsScreen, GraphScreen
from console_screen import ConsoleScreen
from console_help import ConsoleHelpScreen

Window.softinput_mode = "below_target"

KV = '''
<CommonNavigationRailItem>
    MDNavigationRailItemIcon:
        icon: root.icon
    MDNavigationRailItemLabel:
        text: root.text


MDNavigationLayout:

    MDScreenManager:
        id: screen_manager

        MDScreen:
            name: "home"
            md_bg_color: app.theme_cls.backgroundColor

            FitImage:
                id: home_bg
                texture: app.bg_texture
                size_hint: app.home_bg_settings["size_hint"]
                keep_ratio: app.home_bg_settings["keep_ratio"]
                allow_stretch: app.home_bg_settings["allow_stretch"]
                pos_hint: app.home_bg_settings["pos_hint"]

            MDBoxLayout:
                orientation: "horizontal"
                size_hint: 1, 1
                
                MDBoxLayout:
                    size_hint_x: None
                    width: "60dp"
                    md_bg_color: app.theme_cls.backgroundColor
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: ["0dp", "12dp", "0dp", "0dp"]
            
                        MDIconButton:
                            icon: "menu"
                            pos_hint: {"center_x": .5}
                            on_release: app.menu_pressed()
                            size_hint_y: None
                            height: "48dp"
                            
                        MDScrollView:
                            id: rail_scroll
                            do_scroll_x: False
            
                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint_y: None
                                adaptive_height: True
                                spacing: "12dp"
                                padding: ["8dp", "30dp", "8dp", "0dp"]
                                

                                MDFabButton:
                                    icon: "home"
                                    pos_hint: {"center_x": .5}
                                    on_release: app.go_back()
                                    md_bg_color: 0.1, 0.7, 0.3, 1
                                    theme_bg_color: "Custom"
                                    style: "standard"
                                    
                                MDIconButton:
                                    icon: "database-edit-outline"
                                    pos_hint: {"center_x": .5}
                                   
                                MDIconButton:
                                    icon: "console"
                                    pos_hint: {"center_x": .5}
                                    on_release: app.open_console()
                                    
                                MDIconButton:
                                    icon: "library-outline"
                                    pos_hint: {"center_x": .5}
                                    on_release: app.open_console_help()
                                        
                                    
                                MDIconButton:
                                    icon: "snake"
                                    pos_hint: {"center_x": .5}
                                    icon_color: "green"
                                

                Widget: 
                    size_hint_x: 1                    

    MDNavigationDrawer:
        id: nav_drawer
        type: "modal"
        radius: 0
        width: root.width

        MDNavigationDrawerMenu:

            MDNavigationDrawerLabel:
                text: "Menu"

            MDNavigationDrawerDivider:

            MDNavigationDrawerItem:
                on_release: app.open_reader()
                MDNavigationDrawerItemLeadingIcon:
                    icon: "file-pdf-box"
                MDNavigationDrawerItemText:
                    text: "Reader"

            MDNavigationDrawerItem:
                on_release: app.open_web()
                MDNavigationDrawerItemLeadingIcon:
                    icon: "spider-web"
                MDNavigationDrawerItemText:
                    text: "Spider Web"

            MDNavigationDrawerItem:
                on_release: app.open_graphics()
                MDNavigationDrawerItemLeadingIcon:
                    icon: "function-variant"
                MDNavigationDrawerItemText:
                    text: "Graphics"
            
            MDNavigationDrawerItem:
                on_release: app.open_dropdown_menu(self)
                MDNavigationDrawerItemLeadingIcon:
                    icon: "tools"
                MDNavigationDrawerItemText:
                    text: "Settings"

            MDNavigationDrawerDivider:

            MDNavigationDrawerItem:
                on_release: app.close_drawer()
                MDNavigationDrawerItemLeadingIcon:
                    icon: "backburger"
                MDNavigationDrawerItemText:
                    text: "Back"
'''

class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()

class Home(MDApp):
    bg_texture = ObjectProperty(None)
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        store_path = os.path.join(self.user_data_dir, "user_settings.json")
        self.store = JsonStore(store_path)

        # Valores por defecto
        bg_file = "fnd.png"
        keep_ratio = True
        allow_stretch = True
        size_hint = (1, 1)
        pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Si hay fondo guardado
        if self.store.exists("background"):
            bg_file = self.store.get("background")["file"]

        # Si hay home_bg_settings guardado
        if self.store.exists("home_bg_settings"):
            settings = self.store.get("home_bg_settings")
            keep_ratio = settings.get("keep_ratio", True)
            allow_stretch = settings.get("allow_stretch", True)
            size_hint = tuple(settings.get("size_hint", [1, 1]))
            pos_hint = settings.get("pos_hint", {"center_x": 0.5, "center_y": 0.5})

        # Guardar en la app para usar en KV
        self.home_bg_settings = {
            "keep_ratio": keep_ratio,
            "allow_stretch": allow_stretch,
            "size_hint": size_hint,
            "pos_hint": pos_hint
        }

        # Textura del fondo
        path = os.path.join("images", bg_file)
        if os.path.exists(path):
            self.bg_texture = CoreImage(path).texture
        else:
            self.bg_texture = CoreImage("images/fnd.png").texture


        Builder.load_file("GraphicsScreen.kv")
        Builder.load_file("web.kv")
        Builder.load_file("pdf_viewer.kv")
        Builder.load_file("console_screen.kv")
        Builder.load_file("console_help.kv")


        root = Builder.load_string(KV)
        root.ids.screen_manager.add_widget(PDFViewerScreen())
        root.ids.screen_manager.add_widget(WebScreen())
        root.ids.screen_manager.add_widget(GraphicsScreen())
        root.ids.screen_manager.add_widget(GraphScreen())
        root.ids.screen_manager.add_widget(ConsoleScreen())
        root.ids.screen_manager.add_widget(ConsoleHelpScreen())
        return root

    def menu_pressed(self):
        self.root.ids.nav_drawer.set_state("toggle")

    def close_drawer(self):
        self.root.ids.nav_drawer.set_state("close")

    def open_reader(self):
        self.root.ids.screen_manager.current = "reader"
        self.close_drawer()

    def open_web(self):
        self.root.ids.screen_manager.current = "web"
        self.close_drawer()

    def open_graphics(self):
        self.root.ids.screen_manager.current = "graphics"
        self.close_drawer()

    def open_console(self):
        self.root.ids.screen_manager.current = "console"
        self.close_drawer()

    def open_console_help(self):
        self.root.ids.screen_manager.current = "console_help"
        self.close_drawer()

    def open_dropdown_menu(self, caller):
        menu_items = [
            {
                "text": "Light",
                "leading_icon": "white-balance-sunny",
                "on_release": lambda: self.change_theme("Light"),
            },
            {
                "text": "Dark",
                "leading_icon": "moon-waning-crescent",
                "on_release": lambda: self.change_theme("Dark"),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=3,
        )
        self.menu.open()

    def change_theme(self, style):
        self.theme_cls.theme_style = style
        self.menu.dismiss()

    def go_back(self):
        self.root.ids.screen_manager.current = "home"

Home().run()