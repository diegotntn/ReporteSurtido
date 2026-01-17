"""
Fachada de Devoluciones.

RESPONSABILIDAD:
- Ser el ÚNICO punto de acceso desde la UI
- Delegar a casos de uso (commands / queries)
- Mantener estable la API aunque cambie la implementación interna

NO HACE:
- Validaciones de negocio (eso es dominio)
- Acceso directo a Mongo (eso es DB / repos)
- Transformaciones complejas (eso es mappers / queries)
"""

# ───────────────────────── COMMANDS (ESCRITURA) ─────────────────────────
from services.devoluciones.commands.crear_devolucion import crear_devolucion
from services.devoluciones.commands.actualizar_devolucion import actualizar_devolucion
from services.devoluciones.commands.cambiar_estatus import cambiar_estatus
from services.devoluciones.commands.eliminar_devolucion import eliminar_devolucion

# ───────────────────────── QUERIES (LECTURA) ─────────────────────────
from services.devoluciones.queries.listar_historial import listar_historial
from services.devoluciones.queries.obtener_articulos import obtener_articulos
from services.devoluciones.queries.obtener_completa import obtener_completa


class DevolucionesService:
    """
    Fachada pública usada por la UI.

    La UI:
    - SOLO habla con esta clase
    - NO conoce repositorios
    - NO conoce Mongo
    - NO conoce pandas
    """

    def __init__(
        self,
        *,
        devoluciones_repo,
        productos_repo,
        personal_repo,
        vendedores_repo,
    ):
        """
        Parámetros:
        - devoluciones_repo: acceso a devoluciones
        - productos_repo: acceso a productos
        - personal_repo: acceso a personal
        - vendedores_repo: acceso a vendedores
        """
        self.devoluciones_repo = devoluciones_repo
        self.productos_repo = productos_repo
        self.personal_repo = personal_repo
        self.vendedores_repo = vendedores_repo

    # ───────────────────────── REGISTRO ─────────────────────────
    def registrar(
        self,
        *,
        fecha,
        folio,
        cliente,
        direccion,
        motivo,
        zona,
        items,
        vendedor_id=None,
    ):
        """
        Registra una devolución nueva.

        Flujo:
        UI → Facade → Command → Dominio → Persistencia
        """
        return crear_devolucion(
            devoluciones_repo=self.devoluciones_repo,
            productos_repo=self.productos_repo,
            personal_repo=self.personal_repo,
            vendedores_repo=self.vendedores_repo,
            fecha=fecha,
            folio=folio,
            cliente=cliente,
            direccion=direccion,
            motivo=motivo,
            zona=zona,
            items=items,
            vendedor_id=vendedor_id,
        )

    # ───────────────────────── HISTORIAL ─────────────────────────
    def listar(self, *, desde=None, hasta=None, **filtros):
        """
        Devuelve el historial de devoluciones
        para la tabla principal.
        """
        return listar_historial(
            devoluciones_repo=self.devoluciones_repo,
            desde=desde,
            hasta=hasta,
            **filtros,
        )

    # ───────────────────────── ARTÍCULOS ─────────────────────────
    def obtener_articulos(self, devolucion_id: str):
        """
        Devuelve los artículos de una devolución.

        NOTA:
        - Retorna estructuras simples (list / dict)
        - La UI NO maneja DataFrames
        """
        return obtener_articulos(
            devoluciones_repo=self.devoluciones_repo,
            productos_repo=self.productos_repo,
            devolucion_id=devolucion_id,
        )

    # ───────────────────────── COMPLETA ─────────────────────────
    def obtener_completa(self, devolucion_id: str):
        """
        Devuelve la devolución completa para edición.

        Retorna una estructura del tipo:
        {
            "fecha": ...,
            "folio": ...,
            "cliente": ...,
            ...
            "items": [...]
        }
        """
        return obtener_completa(
            devoluciones_repo=self.devoluciones_repo,
            productos_repo=self.productos_repo,
            devolucion_id=devolucion_id,
        )

    # ───────────────────────── ACTUALIZAR ─────────────────────────
    def actualizar(self, *, devolucion_id: str, **data):
        """
        Actualiza una devolución existente.
        """
        return actualizar_devolucion(
            devoluciones_repo=self.devoluciones_repo,
            productos_repo=self.productos_repo,
            devolucion_id=devolucion_id,
            **data,
        )

    # ───────────────────────── ESTATUS ─────────────────────────
    def cambiar_estatus(self, devolucion_id: str, nuevo_estatus: str):
        """
        Cambia el estatus de una devolución
        (pendiente, cerrada, cancelada, etc.).
        """
        return cambiar_estatus(
            devoluciones_repo=self.devoluciones_repo,
            devolucion_id=devolucion_id,
            nuevo_estatus=nuevo_estatus,
        )

    # ───────────────────────── ELIMINAR ─────────────────────────
    def eliminar(self, devolucion_id: str):
        """
        Elimina una devolución.
        """
        return eliminar_devolucion(
            devoluciones_repo=self.devoluciones_repo,
            devolucion_id=devolucion_id,
        )
