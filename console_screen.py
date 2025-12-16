from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import io
import contextlib
import traceback
import numpy as np
import math
from kivy.core.image import Image as CoreImage
import os
from kivy.storage.jsonstore import JsonStore

SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "type": type,
    "dir": dir,
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
}


class ConsoleScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
    def on_pre_enter(self):

        app = MDApp.get_running_app()

        home_bg = app.root.ids.home_bg

        store_path = os.path.join(app.user_data_dir, "user_settings.json")
        self.store = JsonStore(store_path)

        if self.store.exists("background"):
            bg_file = self.store.get("background")["file"]
            self.set_background(bg_file, save=False)


        sm = app.root.ids.screen_manager


        self.context = {
            "app": app,
            "root": app.root,
            "np": np,
            "math": math,
            "sm": sm,
            "set_bg": self.set_background,
            "list_bg": self.list_backgrounds,
            "home_bg": home_bg,
            "save_home_bg_settings": self.save_home_bg_settings
        }

        if self.store.exists("home_bg_settings"):
            settings = self.store.get("home_bg_settings")
            home_bg = self.context["home_bg"]
            home_bg.keep_ratio = settings.get("keep_ratio", True)
            home_bg.allow_stretch = settings.get("allow_stretch", True)
            home_bg.size_hint = tuple(settings.get("size_hint", [1, 1]))
            home_bg.pos_hint = settings.get("pos_hint", {"center_x": 0.5, "center_y": 0.5})

        # Prompt inicial
        self.ids.output.text = (
            ">>> Console Python\n"
            ">>> "
        )

    def ejecutar(self, codigo):
        if not codigo.strip():
            return

        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                try:
                    # Intentar evaluar como expresión
                    resultado = eval(
                        codigo,
                        {"__builtins__": SAFE_BUILTINS},
                        self.context
                    )
                    if resultado is not None:
                        print(resultado)

                except SyntaxError:
                    # Ejecutar como bloque
                    exec(
                        codigo,
                        {"__builtins__": SAFE_BUILTINS},
                        self.context
                    )

        except Exception:
            buffer.write("Error:\n")
            buffer.write(traceback.format_exc(limit=1))

        # Mostrar salida en la terminal
        salida = buffer.getvalue()

        self.ids.output.text += f"{codigo}\n"
        if salida.strip():
            self.ids.output.text += salida
        self.ids.output.text += ">>> "

    def list_backgrounds(self):
        """Devuelve una lista de nombres de imágenes en la carpeta images/"""
        folder = "images"
        exts = (".png", ".jpg", ".jpeg", ".bmp")
        if not os.path.exists(folder):
            return []
        files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
        print("Imáges available:")
        for f in files:
            print(f"- {f}")
        return files

    def set_background(self, filename, save=True):
        path = os.path.join("images", filename)
        if not os.path.exists(path):
            print(f"Error: Imagen no encontrada: {filename}")
            return
        texture = CoreImage(path).texture
        app = MDApp.get_running_app()
        app.bg_texture = texture
        if hasattr(app.root.ids, "home_bg"):
            app.root.ids.home_bg.texture = texture  # Actualiza la pantalla
        print(f"Fondo cambiado a: {filename}")

        if save:
            self.store.put("background", file=filename)
            app.current_bg = filename

    def save_home_bg_settings(self):
        home_bg = self.context.get("home_bg")
        if not home_bg:
            print("Error: home_bg no está definido")
            return

        settings = {
            "keep_ratio": home_bg.keep_ratio,
            "allow_stretch": home_bg.allow_stretch,
            "size_hint": list(home_bg.size_hint),
            "pos_hint": home_bg.pos_hint,
        }
        self.store.put("home_bg_settings", **settings)

        # Actualizar variable global de la app
        app = MDApp.get_running_app()
        app.home_bg_settings = settings

        print("Configuración de home_bg guardada")



