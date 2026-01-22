from tkinter import ttk

# ───────── UI Screens ─────────
from ui.devoluciones.registro.screen import RegistroScreen
from ui.devoluciones.analytics.screen import DevolucionesAnalyticsScreen
from ui.personal.screen import PersonalScreen


class AppMenu(ttk.Notebook):
    """
    Menú principal de pestañas (Notebook).

    RESPONSABILIDADES:
    - Crear y registrar pantallas (screens)
    - Inyectar services base y estado
    - Mantener navegación simple entre módulos

    NOTA CLAVE:
    - NO crea ni usa DevolucionesService global
    - El registro de devoluciones resuelve el service por motivo
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
            productos_service=self.servicios["productos"],
            on_saved=self.state.notify_data_change
        )
        self.add(self.registro, text="Registro")
        
        # ───── Personal ─────
        self.personal = PersonalScreen(
            parent=self,
            personal_service=self.servicios["personal"],
            asignaciones_service=self.servicios["asignaciones"]
        )
        self.add(self.personal, text="Personal")

        # ───── Analytics de devoluciones ─────
        self.analytics = DevolucionesAnalyticsScreen(
            parent=self,
            analytics_service=self.servicios["devoluciones_analytics"]
        )
        self.add(self.analytics, text="Analytics")

    # ─────────────────────────────
    def inicializar(self):
        """
        Inicialización inicial de la UI.
        Se llama UNA sola vez desde MainWindow.
        """

        self.registro.build()
        self.personal.build()

        # Analytics maneja su propio ciclo (botón / eventos internos)
