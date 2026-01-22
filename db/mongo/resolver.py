from db.mongo.collections import (
    DEVOLUCIONES,
    DEVOLUCIONES_VENTAS,
)

def resolver_coleccion_devoluciones(motivo: str) -> str:
    motivo = (motivo or "").lower()

    if motivo in ("captura", "precio", "cliente", "otro motivo"):
        return DEVOLUCIONES_VENTAS

    return DEVOLUCIONES
