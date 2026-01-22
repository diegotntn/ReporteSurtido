import pandas as pd
import uuid
from bson import ObjectId


class AsignacionesRepo:
    """
    Repositorio de ASIGNACIONES DE PASILLOS.

    RESPONSABILIDADES:
    - Acceso directo a MongoDB
    - CRUD puro
    - NO lógica de negocio
    - Devuelve DataFrames
    """

    def __init__(self, db):
        self.col = db.asignaciones

    # ─────────────────────────
    # Helpers
    # ─────────────────────────
    @staticmethod
    def _df(docs):
        return pd.DataFrame(docs) if docs else pd.DataFrame()

    # ─────────────────────────
    # Crear
    # ─────────────────────────
    def crear(self, *, pasillo, persona_id, fecha_desde, fecha_hasta):
        aid = str(uuid.uuid4())

        self.col.insert_one({
            "_id": aid,
            "pasillo": pasillo,
            "persona_id": persona_id,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        })

        return aid

    # ─────────────────────────
    # Actualizar
    # ─────────────────────────
    def actualizar(
        self,
        *,
        asignacion_id,
        pasillo,
        persona_id,
        fecha_desde,
        fecha_hasta
    ):
        self.col.update_one(
            {"_id": asignacion_id},
            {
                "$set": {
                    "pasillo": pasillo,
                    "persona_id": persona_id,
                    "fecha_desde": fecha_desde,
                    "fecha_hasta": fecha_hasta
                }
            }
        )

    # ─────────────────────────
    # Listar
    # ─────────────────────────
    def listar(self) -> pd.DataFrame:
        docs = list(self.col.find().sort("fecha_desde", 1))
        return self._df(docs)

    # ─────────────────────────
    # Eliminar (si algún día lo necesitas)
    # ─────────────────────────
    def eliminar(self, asignacion_id: str):

        result = self.col.delete_one({
            "_id": ObjectId(asignacion_id)
        })

        if result.deleted_count == 0:
            raise RuntimeError(
                f"No se eliminó la asignación {asignacion_id}"
            )
