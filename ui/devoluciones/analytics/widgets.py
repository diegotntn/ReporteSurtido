import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraficaPastel(tk.Frame):
    def __init__(self, parent, titulo):
        super().__init__(parent)

        self.fig = Figure(figsize=(4, 4))
        self.ax = self.fig.add_subplot(111)
        self.titulo = titulo

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def dibujar(self, valor_dev, valor_vta):
        self.ax.clear()

        if valor_dev + valor_vta == 0:
            self.ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")
        else:
            self.ax.pie(
                [valor_dev, valor_vta],
                labels=["Almacen", "Ventas"],
                autopct="%1.1f%%",
                startangle=90
            )

        self.ax.set_title(self.titulo)
        self.canvas.draw()

class TablaKPI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        columnas = ("tipo", "total", "piezas", "importe")

        # ───── Estilos SOLO para esta tabla ─────
        style = ttk.Style()

        style.configure(
            "Treeview",
            font=("Segoe UI", 12),   # ⬅ tamaño del contenido
            rowheight=30            # ⬅ altura de filas
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 13, "bold")  # ⬅ encabezados
        )

        # ───── Treeview ─────
        self.tree = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=6
        )

        # Encabezados
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("total", text="Total")
        self.tree.heading("piezas", text="Piezas")
        self.tree.heading("importe", text="Importe")

        # Columnas (alineación y ancho)
        self.tree.column("tipo", anchor="w", width=220)
        self.tree.column("total", anchor="center", width=120)
        self.tree.column("piezas", anchor="center", width=120)
        self.tree.column("importe", anchor="e", width=150)

        self.tree.pack(fill="both", expand=True)

    # ─────────────────────────────
    def actualizar(self, data):
        self.tree.delete(*self.tree.get_children())

        self.tree.insert(
            "",
            "end",
            values=(
                "Devoluciones",
                data["devoluciones"]["total"],
                data["devoluciones"]["piezas"],
                f"{data['devoluciones']['importe']:.2f}"
            )
        )

        self.tree.insert(
            "",
            "end",
            values=(
                "Devoluciones Venta",
                data["ventas"]["total"],
                data["ventas"]["piezas"],
                f"{data['ventas']['importe']:.2f}"
            )
        )