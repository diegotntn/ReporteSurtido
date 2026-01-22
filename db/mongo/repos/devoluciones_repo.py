from datetime import datetime


class DevolucionesRepo:
    """
    Repositorio de devoluciones.

    RESPONSABILIDAD:
    - Acceso directo a UNA colección Mongo (inyectada)
    - Persistencia y lectura de documentos
    - NO decide qué colección usar
    - NO transforma para UI
    - NO usa pandas
    """

    def __init__(self, db, collection_name: str):
        """
        Parámetros:
        - db: instancia de base de datos Mongo
        - collection_name: nombre de la colección a usar
        """
        self.col = db[collection_name]

    # ───────────── Helpers ─────────────
    @staticmethod
    def _to_dt(value):
        """
        Convierte str | date | datetime a datetime.
        """
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value))

    # ───────────── CRUD ─────────────
    def insertar(
        self,
        *,
        devolucion_id: str,
        fecha,
        folio: str,
        cliente: str,
        direccion: str,
        motivo: str,
        zona: str,
        total: float,
        items: list[dict],
        vendedor_id=None,
        estatus="pendiente",
    ):
        """
        Inserta una nueva devolución en la colección.
        """
        doc = {
            "_id": devolucion_id,
            "fecha": self._to_dt(fecha),
            "folio": folio,
            "cliente": cliente,
            "direccion": direccion,
            "motivo": motivo,
            "zona": zona,
            "total": float(total),
            "items": items or [],
            "vendedor_id": vendedor_id,
            "estatus": estatus,
            "created_at": datetime.utcnow(),
        }
        self.col.insert_one(doc)

    def actualizar(self, devolucion_id: str, *, data: dict):
        """
        Actualiza campos de una devolución existente.
        """
        if not data:
            return

        self.col.update_one(
            {"_id": devolucion_id},
            {"$set": data}
        )

    def eliminar(self, devolucion_id: str):
        """
        Elimina una devolución por ID.
        """
        self.col.delete_one({"_id": devolucion_id})

    def eliminar_todas(self):
        """
        Elimina TODAS las devoluciones de la colección actual.
        """
        self.col.delete_many({})

    # ───────────── Queries simples ─────────────
    def listar(self, *, filtros=None):
        """
        Devuelve una lista de devoluciones resumidas,
        ordenadas por fecha y folio.
        """
        filtros = filtros or {}

        docs = list(
            self.col
            .find(filtros)
            .sort([("fecha", -1), ("folio", -1)])
        )

        resultado = []
        for d in docs:
            resultado.append({
                "id": d.get("_id"),
                "fecha": d.get("fecha"),
                "folio": d.get("folio"),
                "cliente": d.get("cliente"),
                "zona": d.get("zona"),
                "estatus": d.get("estatus"),
            })

        return resultado

    def obtener_por_id(self, devolucion_id: str):
        """
        Devuelve una devolución completa como dict o None.
        """
        d = self.col.find_one({"_id": devolucion_id})
        if not d:
            return None

        d["id"] = d.pop("_id")
        return d

    def obtener_items(self, devolucion_id: str):
        """
        Devuelve los items de una devolución como lista.
        """
        d = self.col.find_one(
            {"_id": devolucion_id},
            {"items": 1}
        )
        if not d:
            return []

        return d.get("items", [])
