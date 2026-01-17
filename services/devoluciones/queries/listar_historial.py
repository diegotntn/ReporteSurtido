"""
Query: listar historial de devoluciones.

RESPONSABILIDAD:
- Construir filtros simples
- Delegar la lectura al repositorio
- Normalizar datos para la UI

NO HACE:
- Acceso directo a Mongo
- Uso de pandas
- Lógica de negocio
"""

from datetime import datetime, date


# ─────────────────────────────────────────────
# Helpers locales
# ─────────────────────────────────────────────

def _dt_inicio(value):
    """Convierte date | datetime | str a datetime (inicio del día)."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    return datetime.fromisoformat(str(value))


def _dt_fin(value):
    """Convierte date | datetime | str a datetime (fin del día)."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.max.time())
    return datetime.fromisoformat(str(value))


# ─────────────────────────────────────────────
# Query principal
# ─────────────────────────────────────────────

def listar_historial(
    *,
    devoluciones_repo,
    desde=None,
    hasta=None,
    **otros_filtros,
):
    """
    Devuelve el historial de devoluciones como lista de dicts.

    Garantías:
    - Siempre devuelve una lista
    - Nunca devuelve None
    """

    # ─────────────────────────────────────────────
    # Construcción de filtros
    # ─────────────────────────────────────────────
    filtros = {}

    # Filtro por fecha
    if desde or hasta:
        filtros["fecha"] = {}

        if desde:
            filtros["fecha"]["$gte"] = _dt_inicio(desde)
        if hasta:
            filtros["fecha"]["$lte"] = _dt_fin(hasta)

    # Otros filtros simples (zona, estatus, vendedor_id, etc.)
    for k, v in otros_filtros.items():
        if v is not None:
            filtros[k] = v

    # ─────────────────────────────────────────────
    # Lectura vía repositorio
    # ─────────────────────────────────────────────
    devoluciones = devoluciones_repo.listar(filtros=filtros)

    if not devoluciones:
        return []

    # ─────────────────────────────────────────────
    # Normalización mínima para UI
    # ─────────────────────────────────────────────
    historial_ui = []

    for d in devoluciones:
        historial_ui.append({
            "id": d.get("id") or d.get("_id"),
            "fecha": d.get("fecha"),
            "folio": d.get("folio"),
            "cliente": d.get("cliente"),
            "zona": d.get("zona"),
            "estatus": d.get("estatus"),
        })

    return historial_ui
