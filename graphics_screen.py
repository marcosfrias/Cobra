from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty, StringProperty, NumericProperty
import math
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy_garden.graph import Graph, MeshLinePlot
import numpy as np
from kivy.core.window import Window

class GraphicsScreen(MDScreen):
    functions = ListProperty([])

    SAFE_MATH = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "log": np.log,
        "ln": np.log,
        "log10": np.log10,
        "exp": np.exp,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": math.pi,
        "e": math.e,
    }

    def on_kv_post(self, base_widget):
        self.refresh_rv()

    def normalize_expression(self, expr: str) -> str:
        return expr.replace("^", "**")

    def add_function(self):
        text = self.ids.function_input.text.strip()
        if text:
            self.functions.append(text)
            self.ids.function_input.text = ""
            self.refresh_rv()

    def remove_function(self, index):
        if 0 <= index < len(self.functions):
            self.functions.pop(index)
            self.refresh_rv()

    def refresh_rv(self):
        self.ids.functions_rv.data = [
            {"text": f, "index": i} for i, f in enumerate(self.functions)
        ]

    def go_to_graph(self):

        is_rad = self.ids.deg_rad_text.text == "Rad."

        angle = 45
        if is_rad:
            angle = math.radians(angle)

        try:
            x_min = float(self.ids.x_min.text or -10)
            x_max = float(self.ids.x_max.text or 10)
            y_min = float(self.ids.y_min.text or -10)
            y_max = float(self.ids.y_max.text or 10)
        except ValueError:
            print("Dominio inválido")
            return

        graph_screen = self.manager.get_screen("graph")
        graph_screen.plot_functions(
            self.functions,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        self.manager.current = "graph"


class FunctionRow(MDBoxLayout):
    text = StringProperty()
    index = NumericProperty()


class GraphScreen(MDScreen):
    SAFE_MATH = GraphicsScreen.SAFE_MATH

    def plot_functions(self, functions, x_min, x_max, y_min, y_max):
        container = self.ids.graph_container
        container.clear_widgets()

        screen_width, screen_height = Window.size

        x_range = x_max - x_min
        y_range = y_max - y_min

        # Reducir número de ticks para que no se amontonen
        x_ticks_major = max(1, x_range // 10)
        y_ticks_major = max(1, y_range // 10)


        pad_left = str(dp(60))
        pad_bottom = str(dp(40))
        padding = [pad_left, pad_bottom]

        graph = Graph(
            xmin=x_min, xmax=x_max,
            ymin=y_min, ymax=y_max,
            draw_border=False,
            background_color=[0.12, 0.12, 0.12, 1],
            x_ticks_major=x_ticks_major,
            y_ticks_major=y_ticks_major,
            x_grid=True,
            y_grid=True,
            x_grid_label=True,
            y_grid_label=True,
            padding=padding,
            size_hint=(1, 1),  # tamaño completo horizontal
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # centrado
            label_options={"color": [1, 1, 1, 1]},  # Solo pasa el color aquí
            font_size="10sp",
        )

        # Ejes principales
        x_axis = MeshLinePlot(color=[1, 1, 1, 1])
        x_axis.points = [(x_min, 0), (x_max, 0)]
        y_axis = MeshLinePlot(color=[1, 1, 1, 1])
        y_axis.points = [(0, y_min), (0, y_max)]
        graph.add_plot(x_axis)
        graph.add_plot(y_axis)

        # Graficar funciones
        x = np.linspace(x_min, x_max, 800)
        colors = [[1, 0, 0, 1], [0, 0.6, 1, 1], [0, 0.8, 0, 1], [1, 0.5, 0, 1]]
        for idx, expr in enumerate(functions):
            expr = expr.replace("^", "**")
            try:
                y = eval(expr, {"__builtins__": {}}, {**self.SAFE_MATH, "x": x})
                plot = MeshLinePlot(color=colors[idx % len(colors)])
                plot.points = list(zip(x, y))
                graph.add_plot(plot)
            except Exception as e:
                print("Error al graficar:", e)

        container.add_widget(graph)

        # Labels para nombres de ejes
        label_x = Label(
            text="X",
            size_hint=(None, None),
            size=(dp(40), dp(24)),
            pos_hint={"center_x": 0.5, "y": 0.01},  # un poco arriba del borde inferior
            color=[1, 1, 1, 1]
        )

        label_y = Label(
            text="Y",
            size_hint=(None, None),
            size=(dp(24), dp(40)),
            pos_hint={"x": 0.01, "center_y": 0.5},  # un poco a la derecha del borde izquierdo
            color=[1, 1, 1, 1]
        )

        container.add_widget(label_x)
        container.add_widget(label_y)

