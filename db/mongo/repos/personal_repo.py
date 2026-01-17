import pandas as pd
import uuid


class PersonalRepo:
    """
    Repositorio de PERSONAL (MongoDB)

    RESPONSABILIDADES:
    - Acceso directo a Mongo
    - CRUD puro
    - NO lógica de negocio
    - Devuelve DataFrames cuando aplica
    """

    def __init__(self, db):
        self.col = db.personal

    # ─────────────────────────
    # Helpers
    # ─────────────────────────
    @staticmethod
    def _df(docs):
        return pd.DataFrame(docs) if docs else pd.DataFrame(
            columns=["id", "nombre", "activo"]
        )

    # ─────────────────────────
    # Crear
    # ─────────────────────────
    def crear(self, nombre: str) -> str:
        pid = str(uuid.uuid4())
        self.col.insert_one({
            "_id": pid,
            "nombre": nombre.strip(),
            "activo": True
        })
        return pid

    # ─────────────────────────
    # Listar (CONTRATO OFICIAL)
    # ─────────────────────────
    def listar_personal(self, solo_activos: bool = True) -> pd.DataFrame:
        query = {"activo": True} if solo_activos else {}
        docs = list(self.col.find(query).sort("nombre", 1))

        for d in docs:
            d["id"] = d.pop("_id")

        return self._df(docs)

    # ─────────────────────────
    # Alias de compatibilidad
    # ─────────────────────────
    def listar(self, solo_activos: bool = True) -> pd.DataFrame:
        return self.listar_personal(solo_activos)

    # ─────────────────────────
    # Actualizar
    # ─────────────────────────
    def actualizar(self, persona_id: str, nuevo_nombre: str):
        self.col.update_one(
            {"_id": persona_id},
            {"$set": {"nombre": nuevo_nombre.strip()}}
        )

    # ─────────────────────────
    # Eliminar / Desactivar
    # ─────────────────────────
    def eliminar(self, persona_id: str):
        self.col.delete_one({"_id": persona_id})

    def desactivar(self, persona_id: str):
        # En tu sistema = eliminación real
        self.eliminar(persona_id)
