from kivymd.uix.screen import MDScreen
import sys

# Detectar Android
if sys.platform == "android":
    from jnius import autoclass
    BrowserBridge = autoclass("org.webview.BrowserBridge")
    ANDROID = True
else:
    ANDROID = False

    class BrowserBridge:
        @staticmethod
        def showWeb(url):
            print(f"[TEST MODE] Navegar a: {url}")

        @staticmethod
        def hideWeb():
            print("[TEST MODE] Cerrar WebView")


class WebScreen(MDScreen):
    def open_web(self):
        url = "https://www.google.com"
        BrowserBridge.showWeb(url)

    def close_web(self):
        BrowserBridge.hideWeb()

    def go_home(self):
        if self.manager:
            self.manager.current = "home"
