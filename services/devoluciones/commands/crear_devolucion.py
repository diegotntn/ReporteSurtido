import uuid
from datetime import datetime, date

from services.devoluciones.mappers.devolucion_mapper import (
    devolucion_from_ui,
    devolucion_to_persistence,
)


def _normalizar_fecha(fecha):
    """
    MongoDB NO acepta datetime.date
    Convierte date → datetime (00:00:00)
    """
    if isinstance(fecha, date) and not isinstance(fecha, datetime):
        return datetime.combine(fecha, datetime.min.time())
    return fecha

def crear_devolucion(
    *,
    devoluciones_repo,
    productos_repo,
    personal_repo,
    vendedores_repo,
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
    COMMAND: Crear devolución
    """

    # 1️⃣ ID
    devolucion_id = str(uuid.uuid4())

    # 2️⃣ Fecha
    fecha = _normalizar_fecha(fecha)

    # 3️⃣ Dominio
    devol = devolucion_from_ui(
        devolucion_id=devolucion_id,
        folio=folio,
        cliente=cliente,
        direccion=direccion,
        motivo=motivo,
        zona=zona,
        vendedor_id=vendedor_id,
        articulos=items,  # ← viene directo de UI
    )

    # 4️⃣ Validar
    devol.validar()

    # 5️⃣ Mapper (solo para datos simples)
    data = devolucion_to_persistence(devol)

    # 6️⃣ Persistir (USANDO items DIRECTO)
    devoluciones_repo.insertar(
        devolucion_id=devol.id,
        fecha=fecha,
        folio=data["folio"],
        cliente=data["cliente"],
        direccion=data["direccion"],
        motivo=data["motivo"],
        zona=data["zona"],
        total=data["total"],
        items=items,  # ← CLAVE: NO usar data["items"]
        vendedor_id=data.get("vendedor_id"),
        estatus=data.get("estatus", "pendiente"),
    )

    return devol.id
