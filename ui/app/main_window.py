import tkinter as tk

# ───────── DB / Factory ─────────
from db.factory import (
    get_db,
    get_productos_service,
    get_personal_repo,
    get_vendedores_repo,
    get_asignaciones_repo,
)

# ───────── Services ─────────
from services.personal_service import PersonalService
from services.vendedores_service import VendedoresService
from services.asignaciones_service import AsignacionesService
from services.devoluciones.analytics.service import DevolucionesAnalyticsService

# ───────── UI Core ─────────
from ui.app.menu import AppMenu
from ui.app.state import AppState


class MainWindow(tk.Tk):
    """
    Ventana principal de la aplicación.

    RESPONSABILIDADES:
    - Inicializar infraestructura (DB)
    - Construir services BASE (no dependientes de motivo)
    - Registrar services en un solo diccionario
    - Inicializar UI y estado global

    REGLAS:
    - NO instancia repos directamente
    - NO instancia DevolucionesService
    - NO decide colecciones
    """

    def __init__(self):
        super().__init__()

        # ───────────────── Ventana ─────────────────
        self.title("Sistema de Devoluciones")
        self.geometry("1250x1250")
        self.minsize(1100, 680)

        # ───────────────── Infraestructura DB ─────────────────
        self.db_provider = get_db()

        # ───────────────── Services BASE ─────────────────
        # Productos (autocomplete, etc.)
        self.productos_service = get_productos_service()

        # Repos base (no dependen de motivo)
        self.personal_repo = get_personal_repo()
        self.vendedores_repo = get_vendedores_repo()
        self.asignaciones_repo = get_asignaciones_repo()

        # Services base
        self.personal_service = PersonalService(self.personal_repo)
        self.vendedores_service = VendedoresService(self.vendedores_repo)

        self.asignaciones_service = AsignacionesService(
            asignaciones_repo=self.asignaciones_repo,
            personal_repo=self.personal_repo,
        )

        # 🔹 Analytics (lectura directa DB, independiente de motivo)
        self.devoluciones_analytics_service = DevolucionesAnalyticsService(
            self.db_provider
        )

        # ───────────────── Registro de services ─────────────────
        self.servicios = {
            "productos": self.productos_service,
            "personal": self.personal_service,
            "vendedores": self.vendedores_service,
            "asignaciones": self.asignaciones_service,
            # ⚠️ NOTA IMPORTANTE:
            # devoluciones_service NO se registra aquí
            # se crea dinámicamente por motivo desde events
            "devoluciones_analytics": self.devoluciones_analytics_service,
        }

        # ───────────────── Estado global ─────────────────
        self.state = AppState()

        # ───────────────── Menú principal ─────────────────
        self.menu = AppMenu(
            parent=self,
            servicios=self.servicios,
            state=self.state,
        )
        self.menu.pack(fill="both", expand=True)

        # ───────────────── Suscripciones ─────────────────
        self.state.subscribe_data_change(self._on_data_change)

        # ───────────────── Inicialización UI ─────────────────
        self.menu.inicializar()

        # ───────────────── Cierre limpio ─────────────────
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ─────────────────────────────────────────────
    def _on_data_change(self):
        """
        Callback global cuando cambian datos.
        """
        if hasattr(self.menu, "historial"):
            self.menu.historial.events.cargar_historial()

    # ─────────────────────────────────────────────
    def on_close(self):
        """
        Cierre limpio de la aplicación.
        """
        try:
            if hasattr(self.db_provider, "close"):
                self.db_provider.close()
        finally:
            self.destroy()
