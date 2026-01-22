from db.mongo.collections import (
    DEVOLUCIONES,
    DEVOLUCIONES_VENTAS,
)

MOTIVOS_DEVOLUCION = (
    "faltante",
    "cambio de articulo",
    "caducidad",
    "mal estado",
)

def resolver_coleccion_devoluciones(motivo: str) -> str:
    motivo = (motivo or "").lower()
    return DEVOLUCIONES if motivo in MOTIVOS_DEVOLUCION else DEVOLUCIONES_VENTAS
