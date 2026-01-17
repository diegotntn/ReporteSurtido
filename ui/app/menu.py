from tkinter import ttk

# ───────── UI Screens ─────────
from ui.devoluciones.registro.screen import RegistroScreen
from ui.devoluciones.historial.screen import HistorialScreen
from ui.devoluciones.analytics.screen import DevolucionesAnalyticsScreen
from ui.personal.screen import PersonalScreen



class AppMenu(ttk.Notebook):
    """
    Menú principal de pestañas (Notebook).

    RESPONSABILIDADES:
    - Crear y registrar pantallas (screens)
    - Inyectar services y estado
    - Mantener navegación simple entre módulos

    REGLAS:
    - NO conoce reportes
    - NO dispara lógica pesada
    """

    def __init__(self, parent, *, servicios, state):
        super().__init__(parent)

        self.servicios = servicios
        self.state = state

        self._crear_tabs()

    # ─────────────────────────────
    def _crear_tabs(self):
        """Crea y registra las pestañas del sistema."""

        # ───── Registro de devoluciones ─────
        self.registro = RegistroScreen(
            parent=self,
            devoluciones_service=self.servicios["devoluciones"],
            productos_service=self.servicios["productos"],
            on_saved=self.state.notify_data_change
        )
        self.add(self.registro, text="Registro")

        # ───── Historial de devoluciones ─────
        self.historial = HistorialScreen(
            parent=self,
            devoluciones_service=self.servicios["devoluciones"],
            on_change=self.state.notify_data_change
        )
        #self.add(self.historial, text="Historial")

        # ───── Analytics de devoluciones ─────
        self.analytics = DevolucionesAnalyticsScreen(
            parent=self,
            analytics_service=self.servicios["devoluciones_analytics"]
        )
        self.add(self.analytics, text="Analytics")

        # ───── Personal ─────
        self.personal = PersonalScreen(
            parent=self,
            personal_service=self.servicios["personal"],
            asignaciones_service=self.servicios["asignaciones"]
        )
        self.add(self.personal, text="Personal")

    # ─────────────────────────────
    def inicializar(self):
        """
        Inicialización inicial de la UI.
        Se llama UNA sola vez desde MainWindow.

        REGLAS:
        - Construir solo pantallas necesarias
        - Nada de lógica pesada
        """

        self.registro.build()
        self.personal.build()

        # Historial y Analytics manejan su propio ciclo
        # (eventos internos / botón actualizar)
