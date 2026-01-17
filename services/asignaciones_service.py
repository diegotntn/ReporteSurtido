import pandas as pd


class AsignacionesService:
    """
    Lógica de negocio para ASIGNACIONES DE PASILLOS.
    """

    def __init__(self, asignaciones_repo, personal_repo):
        self.asignaciones_repo = asignaciones_repo
        self.personal_repo = personal_repo

    # ─────────────────────────
    # CRUD
    # ─────────────────────────
    def crear_asignacion(self, pasillo, persona_nombre, desde, hasta):
        persona_id = self._resolver_persona_id(persona_nombre)
        self._validar_fechas(desde, hasta)

        return self.asignaciones_repo.crear(
            pasillo=pasillo,
            persona_id=persona_id,
            fecha_desde=desde,
            fecha_hasta=hasta
        )

    def actualizar_asignacion(
        self,
        asignacion_id,
        pasillo,
        persona_nombre,
        desde,
        hasta
    ):
        if not asignacion_id:
            raise ValueError("Asignación no especificada")

        persona_id = self._resolver_persona_id(persona_nombre)
        self._validar_fechas(desde, hasta)

        self.asignaciones_repo.actualizar(
            asignacion_id=asignacion_id,
            pasillo=pasillo,
            persona_id=persona_id,
            fecha_desde=desde,
            fecha_hasta=hasta
        )

    # ─────────────────────────
    # LISTADOS PARA UI
    # ─────────────────────────
    def listar_asignaciones(self) -> list[dict]:
        asignaciones = self.asignaciones_repo.listar()

        if asignaciones.empty:
            return []

        if "_id" in asignaciones.columns:
            asignaciones["id"] = asignaciones["_id"].astype(str)

        if "persona_id" in asignaciones.columns:
            asignaciones["persona_id"] = asignaciones["persona_id"].astype(str)

        personal = self.personal_repo.listar_personal(solo_activos=False)

        if personal.empty:
            return []

        if "_id" in personal.columns:
            personal["id"] = personal["_id"].astype(str)

        mapa_personas = dict(
            zip(personal["id"], personal["nombre"])
        )

        salida = []
        for _, r in asignaciones.iterrows():
            salida.append({
                "id": r["id"],
                "pasillo": r.get("pasillo", ""),
                "persona": mapa_personas.get(r["persona_id"], ""),
                "desde": r.get("fecha_desde", ""),
                "hasta": r.get("fecha_hasta") or ""
            })

        return salida