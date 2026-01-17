"""
Query: obtener artículos de una devolución.

RESPONSABILIDAD:
- Obtener artículos para el panel derecho del historial
- Normalizar el contrato de datos para la UI

NO HACE:
- Validaciones de negocio
- Acceso directo a Mongo
- Uso de pandas
"""

# Contrato de claves que la UI espera
_UI_KEYS = ["id", "nombre", "codigo", "pasillo", "cantidad", "unitario"]


def obtener_articulos(*, devoluciones_repo, productos_repo, devolucion_id: str):
    """
    Devuelve los artículos de una devolución como lista de dicts.

    Parámetros:
    - devoluciones_repo: repositorio de devoluciones
    - productos_repo: repositorio de productos
    - devolucion_id: id de la devolución

    Garantías:
    - Nunca devuelve None
    - Siempre devuelve una lista
    - Cada elemento cumple el contrato UI
    """

    # ─────────────────────────────────────────────
    # Validación mínima de entrada
    # ─────────────────────────────────────────────
    if not devolucion_id:
        return []

    # ─────────────────────────────────────────────
    # Lectura base (repositorio)
    # ─────────────────────────────────────────────
    devolucion = devoluciones_repo.obtener_por_id(devolucion_id)
    if not devolucion:
        return []

    items = devolucion.get("items", [])
    if not items:
        return []

    # ─────────────────────────────────────────────
    # Normalización para UI
    # ─────────────────────────────────────────────
    articulos_ui = []

    for item in items:
        producto_id = item.get("producto_id")
        producto = productos_repo.obtener_por_id(producto_id) if producto_id else {}

        row = {
            "id": producto_id or item.get("id"),
            "nombre": producto.get("nombre"),
            "codigo": producto.get("codigo"),
            "pasillo": producto.get("pasillo"),
            "cantidad": item.get("cantidad"),
            "unitario": item.get("unitario"),
        }

        # Garantizar contrato UI
        for key in _UI_KEYS:
            row.setdefault(key, None)

        articulos_ui.append(row)

    return articulos_ui
