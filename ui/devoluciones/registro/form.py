import tkinter as tk
from tkinter import ttk, StringVar
from tkcalendar import DateEntry

from utils.constants import MOTIVOS


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────

ZONAS = [
    "Z11","Z12","Z13","Z14","Z15","Z17","Z18",
    "Z19","Z20","Z21","Z22","Z23","Z27","Z28"
]

PASILLOS = ["P1", "P2", "P3", "P4"]


# ─────────────────────────────────────────────
# FORMULARIO: DATOS GENERALES DE LA DEVOLUCIÓN
# ─────────────────────────────────────────────
class RegistroForm(ttk.LabelFrame):
    """
    Datos generales de la devolución.
    """

    def __init__(self, parent):
        super().__init__(parent, text="Datos de la devolución", padding=10)

        self.fecha = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.folio = ttk.Entry(self)
        self.cliente = ttk.Entry(self)
        self.direccion = ttk.Entry(self)

        self.zona = ttk.Combobox(self, values=ZONAS, state="readonly")
        self.zona.current(0)

        self.motivo = ttk.Combobox(self, values=MOTIVOS, state="readonly")
        self.motivo.current(0)

        self.motivo_otro = ttk.Entry(self)

        self._layout()

    def _layout(self):
        campos = [
            ("Fecha", self.fecha, 0, 0),
            ("Folio", self.folio, 0, 1),
            ("Cliente", self.cliente, 0, 2),
            ("Dirección", self.direccion, 0, 3),
            ("Zona", self.zona, 2, 0),
            ("Motivo", self.motivo, 2, 1),
            ("Otro motivo", self.motivo_otro, 2, 2),
        ]

        for texto, widget, fila, col in campos:
            ttk.Label(self, text=texto).grid(row=fila, column=col, sticky="w")
            widget.grid(row=fila + 1, column=col, padx=8, pady=6, sticky="ew")

    def get_data(self) -> dict:
        otro = self.motivo_otro.get().strip()
        return {
            "fecha": self.fecha.get_date(),
            "folio": self.folio.get().strip(),
            "cliente": self.cliente.get().strip(),
            "direccion": self.direccion.get().strip(),
            "zona": self.zona.get(),
            "motivo": otro.lower() if otro else self.motivo.get().lower(),
        }

    def clear(self):
        for campo in (self.folio, self.cliente, self.direccion, self.motivo_otro):
            campo.delete(0, "end")

        self.motivo.current(0)
        self.zona.current(0)


# ─────────────────────────────────────────────
# FORMULARIO: ARTÍCULO (AUTOCOMPLETADO)
# ─────────────────────────────────────────────
class ArticuloForm(ttk.LabelFrame):
    """
    Formulario para agregar artículos con panel lateral de sugerencias.
    """

    def __init__(self, parent):
        super().__init__(parent, text="Agregar artículo", padding=10)

        # ───── Variables ─────
        self.buscar_var = StringVar()
        self.codigo_var = StringVar()
        self.nombre_var = StringVar()
        self.precio_var = StringVar()
        self.pasillo_var = StringVar()
        self.cantidad_var = StringVar(value="1")

        # Layout principal (2 columnas)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=4)

        # ─────────────────────────
        # COLUMNA IZQUIERDA (FORMULARIO)
        # ─────────────────────────
        left = ttk.Frame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(left, text="Buscar (código o nombre)").grid(row=0, column=0, sticky="w")
        self.buscar = ttk.Entry(left, textvariable=self.buscar_var, width=45)
        self.buscar.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

        headers = ["Código", "Nombre", "Precio", "Pasillo", "Cant"]
        for i, h in enumerate(headers):
            ttk.Label(left, text=h).grid(row=2, column=i, sticky="w")

        self.codigo = ttk.Entry(left, textvariable=self.codigo_var, state="readonly", width=18)
        self.nombre = ttk.Entry(left, textvariable=self.nombre_var, state="readonly", width=40)
        self.precio = ttk.Entry(left, textvariable=self.precio_var, state="readonly", width=10)

        self.pasillo = ttk.Combobox(
            left,
            textvariable=self.pasillo_var,
            values=PASILLOS,
            width=6,
            state="disabled"
        )

        self.cantidad = ttk.Entry(left, textvariable=self.cantidad_var, width=6)

        self.codigo.grid(row=3, column=0, padx=4, pady=4)
        self.nombre.grid(row=3, column=1, padx=4, pady=4, sticky="ew")
        self.precio.grid(row=3, column=2, padx=4, pady=4)
        self.pasillo.grid(row=3, column=3, padx=4, pady=4)
        self.cantidad.grid(row=3, column=4, padx=4, pady=4)

        # ─────────────────────────
        # COLUMNA DERECHA (SUGERENCIAS)
        # ─────────────────────────
        right = ttk.LabelFrame(self, text="Sugerencias", padding=8)
        right.grid(row=0, column=1, sticky="nsew")

        self._listbox = tk.Listbox(
            right,
            height=14,               # más alto ahora que no hay detalle abajo
            activestyle="dotbox",
            exportselection=False
        )

        scroll = ttk.Scrollbar(
            right,
            orient="vertical",
            command=self._listbox.yview
        )
        self._listbox.config(yscrollcommand=scroll.set)

        self._listbox.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

    # ─────────────────────────
    # AUTOCOMPLETADO (USADO POR EVENTS)
    # ─────────────────────────
    def mostrar_sugerencias(self, productos: list):
        self._productos_cache = productos
        self._listbox.delete(0, tk.END)

        for p in productos:
            self._listbox.insert(
                tk.END,
                f"{p['clave']} — {p['nombre']}"
            )

    def ocultar_sugerencias(self):
        self._listbox.delete(0, tk.END)

    # ─────────────────────────
    # API PARA EVENTS
    # ─────────────────────────
    def set_producto(self, producto: dict, pasillo: str | None):
        self.codigo_var.set(producto.get("clave", ""))
        self.nombre_var.set(producto.get("nombre", ""))
        self.precio_var.set(f"{producto.get('lcd4', 0):.2f}")

        if pasillo:
            self.pasillo_var.set(pasillo)
            self.pasillo.config(state="disabled")
        else:
            self.pasillo_var.set("")
            self.pasillo.config(state="readonly")

    def get_data(self) -> dict:
        try:
            cantidad = int(self.cantidad_var.get())
        except ValueError:
            raise ValueError("Cantidad inválida")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        return {
            "clave": self.codigo_var.get(),
            "nombre": self.nombre_var.get(),
            "precio": float(self.precio_var.get() or 0),
            "pasillo": self.pasillo_var.get(),
            "cantidad": cantidad,
        }

    def clear(self):
        self.buscar_var.set("")
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.precio_var.set("")
        self.pasillo_var.set("")
        self.cantidad_var.set("1")
        self.pasillo.config(state="disabled")
        self.ocultar_sugerencias()
