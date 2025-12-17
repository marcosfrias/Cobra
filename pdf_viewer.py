import sys
import os

from kivymd.uix.screen import MDScreen

# Detectar si estamos en Android
if sys.platform == "android":
    from jnius import autoclass
    from android import activity

    WebViewBridge = autoclass("org.webview.WebViewBridge")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Intent = autoclass("android.content.Intent")
    ANDROID = True
else:
    ANDROID = False

    class WebViewBridge:
        @staticmethod
        def showPDF(path):
            print(f"[TEST MODE] Mostrar PDF: {path}")

    class activity:
        @staticmethod
        def bind(on_activity_result=None):
            print("[TEST MODE] bind on_activity_result")

    class Intent:
        ACTION_GET_CONTENT = "ACTION_GET_CONTENT"
        CATEGORY_OPENABLE = "CATEGORY_OPENABLE"


REQUEST_PICK_PDF = 1001


class PDFViewerScreen(MDScreen):

    def on_enter(self):
        # Bind solo cuando el screen está activo
        if ANDROID:
            activity.bind(on_activity_result=self.on_result)


    def switch_to_home(self):
        if self.manager:
            self.manager.current = "home"

    def open_picker(self):
        if ANDROID:
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("application/pdf")
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            PythonActivity.mActivity.startActivityForResult(
                intent, REQUEST_PICK_PDF
            )
        else:
            print("[TEST MODE] Abrir selector de PDF")

    def on_result(self, request, result_code, data):
        if not ANDROID:
            print("[TEST MODE] on_result llamado")
            return

        if request != REQUEST_PICK_PDF or result_code != PythonActivity.RESULT_OK:
            return

        uri = data.getData()
        pdf_path = self.copy_pdf_from_uri(uri)
        WebViewBridge.showPDF(pdf_path, False)

    def copy_pdf_from_uri(self, uri):
        if ANDROID:
            resolver = PythonActivity.mActivity.getContentResolver()
            input_stream = resolver.openInputStream(uri)

            output_path = os.path.join(
                PythonActivity.mActivity.getFilesDir().toString(),
                "temp.pdf"
            )

            with open(output_path, "wb") as f:
                buffer = bytearray(4096)
                n = input_stream.read(buffer)
                while n > 0:
                    f.write(buffer[:n])
                    n = input_stream.read(buffer)

            input_stream.close()
            return output_path

        print("[TEST MODE] copy_pdf_from_uri llamado")
        return "/path/to/fake.pdf"

    def open_pdf_direct(self, filename):
        if ANDROID:
            WebViewBridge.showPDF(filename, True)
        else:
            print(f"[TEST MODE] Abrir PDF interno: {filename}")

