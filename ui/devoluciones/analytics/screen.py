import tkinter as tk
from tkinter import ttk

from ui.devoluciones.analytics.widgets import (
    TablaKPI,
    GraficaPastel
)


class DevolucionesAnalyticsScreen(tk.Frame):
    """
    Dashboard de Analytics de Devoluciones.
    Enfoque: legibilidad y presentación profesional.
    """

    def __init__(self, parent, *, analytics_service):
        super().__init__(parent)
        self.analytics_service = analytics_service

        self._configurar_estilos()
        self._construir_layout()

        self.pack(fill="both", expand=True)

    # ─────────────────────────────
    # CONFIGURACIÓN VISUAL (FUENTES GRANDES)
    # ─────────────────────────────
    def _configurar_estilos(self):
        style = ttk.Style()

        # Título principal
        style.configure(
            "Analytics.Title.TLabel",
            font=("Segoe UI", 18, "bold")
        )

        # Botón principal
        style.configure(
            "Analytics.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(14, 8)
        )

        # Títulos de secciones (LabelFrame)
        style.configure(
            "TLabelframe.Label",
            font=("Segoe UI", 13, "bold")
        )

    # ─────────────────────────────
    # CONSTRUCCIÓN DE LAYOUT
    # ─────────────────────────────
    def _construir_layout(self):
        # ───── Header ─────
        header = tk.Frame(self)
        header.pack(fill="x", padx=20, pady=(15, 10))

        ttk.Label(
            header,
            text="Análisis de Devoluciones",
            style="Analytics.Title.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Actualizar análisis",
            style="Analytics.TButton",
            command=self._cargar_datos
        ).pack(side="right")

        # ───── Separador ─────
        ttk.Separator(self, orient="horizontal").pack(
            fill="x", padx=20, pady=(0, 15)
        )

        # ───── Contenedor principal ─────
        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        # ───── Tabla KPIs ─────
        tabla_frame = tk.LabelFrame(
            main,
            text="Resumen General",
            padx=15,
            pady=15
        )
        tabla_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        self.tabla = TablaKPI(tabla_frame)
        self.tabla.pack(fill="both", expand=True)

        # ───── Gráficas ─────
        graficas_frame = tk.LabelFrame(
            main,
            text="Distribución",
            padx=15,
            pady=15
        )
        graficas_frame.grid(row=1, column=0, sticky="nsew")

        graficas_frame.columnconfigure((0, 1, 2), weight=1)

        self.grafica_total = GraficaPastel(
            graficas_frame,
            "Total de\nDevoluciones"
        )
        self.grafica_piezas = GraficaPastel(
            graficas_frame,
            "Total de\nPiezas"
        )
        self.grafica_importe = GraficaPastel(
            graficas_frame,
            "Importe\nTotal"
        )

        self.grafica_total.grid(row=0, column=0, sticky="nsew", padx=10)
        self.grafica_piezas.grid(row=0, column=1, sticky="nsew", padx=10)
        self.grafica_importe.grid(row=0, column=2, sticky="nsew", padx=10)

    # ─────────────────────────────
    # DATOS
    # ─────────────────────────────
    def _cargar_datos(self):
        """
        Lee KPIs y refresca tabla y gráficas.
        """
        data = self.analytics_service.obtener_kpis()

        self.tabla.actualizar(data)

        self.grafica_total.dibujar(
            data["devoluciones"]["total"],
            data["ventas"]["total"]
        )

        self.grafica_piezas.dibujar(
            data["devoluciones"]["piezas"],
            data["ventas"]["piezas"]
        )

        self.grafica_importe.dibujar(
            data["devoluciones"]["importe"],
            data["ventas"]["importe"]
        )
