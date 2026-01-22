import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from utils.constants import PASILLOS


class PersonalForm(ttk.Frame):
    """
    Formularios:
    - Alta / edición de persona
    - Asignación a pasillo
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Variables
        self.var_nombre = tk.StringVar()
        self.var_pasillo = tk.StringVar()
        self.var_persona = tk.StringVar()

        self._build()

    # ─────────────────────────
    # BUILD GENERAL
    # ─────────────────────────
    def _build(self):
        self._build_persona()
        self._build_asignacion()

    # ─────────────────────────
    # FORMULARIO PERSONAL
    # ─────────────────────────
    def _build_persona(self):
        f = ttk.LabelFrame(
            self,
            text="Alta / edición de personal",
            padding=10
        )
        f.pack(fill="x")

        ttk.Label(f, text="Nombre").grid(
            row=0, column=0, sticky="w"
        )

        ttk.Entry(
            f,
            textvariable=self.var_nombre,
            width=32
        ).grid(row=1, column=0, sticky="w")

        self.btn_add = ttk.Button(
            f,
            text="Agregar"
        )
        self.btn_add.grid(row=1, column=1, padx=8)

        self.btn_clear = ttk.Button(
            f,
            text="Limpiar"
        )
        self.btn_clear.grid(row=1, column=2)

        # 🔴 Eliminar personal
        self.btn_delete = ttk.Button(
            f,
            text="Eliminar personal"
        )
        self.btn_delete.grid(row=1, column=3, padx=(8, 0))
        self.btn_delete.state(["disabled"])

    # ─────────────────────────
    # FORMULARIO ASIGNACIÓN
    # ─────────────────────────
    def _build_asignacion(self):
        f = ttk.LabelFrame(
            self,
            text="Asignación a pasillo",
            padding=10
        )
        f.pack(fill="x", pady=(10, 0))

        # Pasillo
        ttk.Label(f, text="Pasillo").grid(
            row=0, column=0, sticky="w"
        )
        self.cb_pasillo = ttk.Combobox(
            f,
            values=PASILLOS,
            textvariable=self.var_pasillo,
            width=8,
            state="readonly"
        )
        self.cb_pasillo.grid(
            row=1, column=0, padx=(0, 10), sticky="w"
        )

        # Persona
        ttk.Label(f, text="Persona").grid(
            row=0, column=1, sticky="w"
        )
        self.cb_persona = ttk.Combobox(
            f,
            textvariable=self.var_persona,
            width=30,
            state="readonly"
        )
        self.cb_persona.grid(
            row=1, column=1, padx=(0, 10), sticky="w"
        )

        # Desde
        ttk.Label(f, text="Desde").grid(
            row=0, column=2, sticky="w"
        )
        self.dt_desde = DateEntry(
            f,
            date_pattern="yyyy-mm-dd"
        )
        self.dt_desde.set_date(date.today())
        self.dt_desde.grid(
            row=1, column=2, padx=(0, 10), sticky="w"
        )

        # Hasta
        ttk.Label(f, text="Hasta").grid(
            row=0, column=3, sticky="w"
        )
        self.dt_hasta = DateEntry(
            f,
            date_pattern="yyyy-mm-dd"
        )
        self.dt_hasta.set_date(date.today())
        self.dt_hasta.grid(
            row=1, column=3, padx=(0, 10), sticky="w"
        )

        # Guardar / actualizar
        self.btn_save_asig = ttk.Button(
            f,
            text="Guardar asignación"
        )
        self.btn_save_asig.grid(
            row=1, column=4, padx=(10, 0)
        )

        # Cancelar edición
        self.btn_cancel_asig = ttk.Button(
            f,
            text="Cancelar edición"
        )
        self.btn_cancel_asig.grid(
            row=1, column=5, padx=(8, 0)
        )
        self.btn_cancel_asig.state(["disabled"])

        # 🔴 Eliminar asignación
        self.btn_delete_asig = ttk.Button(
            f,
            text="Eliminar asignación"
        )
        self.btn_delete_asig.grid(
            row=1, column=6, padx=(8, 0)
        )
        self.btn_delete_asig.state(["disabled"])
