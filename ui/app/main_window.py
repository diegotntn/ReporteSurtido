import tkinter as tk

# ───────── Base de datos (infraestructura) ─────────
from db import get_db

# ───────── Repositorios ─────────
from db.mongo.repos.productos_repo import ProductosRepo
from db.mongo.repos.personal_repo import PersonalRepo
from db.mongo.repos.vendedores_repo import VendedoresRepo
from db.mongo.repos.devoluciones_repo import DevolucionesRepo
from db.mongo.repos.asignaciones_repo import AsignacionesRepo

# ───────── Services (casos de uso) ─────────
from services.productos_service import ProductosService
from services.personal_service import PersonalService
from services.vendedores_service import VendedoresService
from services.asignaciones_service import AsignacionesService
from services.devoluciones.facade import DevolucionesService
from services.devoluciones.analytics.service import DevolucionesAnalyticsService

# ───────── UI Core ─────────
from ui.app.menu import AppMenu
from ui.app.state import AppState


class MainWindow(tk.Tk):
    """
    Ventana principal de la aplicación.

    RESPONSABILIDADES:
    - Crear infraestructura (DB Provider)
    - Crear repositorios
    - Crear services correctamente inyectados
    - Registrar servicios en un solo diccionario
    - Inicializar UI y estado global

    REGLAS:
    - MainWindow NO conoce reportes
    - MainWindow NO maneja threads
    - MainWindow NO hace lógica de negocio
    """

    def __init__(self):
        super().__init__()

        # ───────────────── Ventana ─────────────────
        self.title("Sistema de Devoluciones")
        self.geometry("1250x1250")
        self.minsize(1100, 680)

        # ───────────────── Infraestructura DB ─────────────────
        self.db_provider = get_db()
        db = self.db_provider._db  # MongoDatabase

        # ───────────────── Repositorios ─────────────────
        self.productos_repo = ProductosRepo(db)
        self.personal_repo = PersonalRepo(db)
        self.vendedores_repo = VendedoresRepo(db)
        self.devoluciones_repo = DevolucionesRepo(db)
        self.asignaciones_repo = AsignacionesRepo(db)

        # ───────────────── Services ─────────────────
        self.productos_service = ProductosService(self.productos_repo)
        self.personal_service = PersonalService(self.personal_repo)
        self.vendedores_service = VendedoresService(self.vendedores_repo)

        self.asignaciones_service = AsignacionesService(
            asignaciones_repo=self.asignaciones_repo,
            personal_repo=self.personal_repo
        )

        self.devoluciones_service = DevolucionesService(
            devoluciones_repo=self.devoluciones_repo,
            productos_repo=self.productos_repo,
            personal_repo=self.personal_repo,
            vendedores_repo=self.vendedores_repo,
        )

        # 🔹 Analytics de devoluciones (NUEVO)
        self.devoluciones_analytics_service = DevolucionesAnalyticsService(
            self.db_provider
        )

        # ───────────────── Registro de services ─────────────────
        self.servicios = {
            "productos": self.productos_service,
            "personal": self.personal_service,
            "vendedores": self.vendedores_service,
            "asignaciones": self.asignaciones_service,
            "devoluciones": self.devoluciones_service,
            "devoluciones_analytics": self.devoluciones_analytics_service,  # 👈 CLAVE
        }

        # ───────────────── Estado global ─────────────────
        self.state = AppState()

        # ───────────────── Menú principal ─────────────────
        self.menu = AppMenu(
            parent=self,
            servicios=self.servicios,
            state=self.state
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

        REGLA:
        - Refrescar solo pantallas Tk activas
        - Nada de renders pesados
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
