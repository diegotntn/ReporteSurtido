from pymongo import MongoClient
from datetime import datetime, date


class MongoClientProvider:
    """
    Proveedor de acceso a MongoDB.

    RESPONSABILIDADES:
    - Crear y cerrar la conexión
    - Exponer métodos de acceso a datos (CRUD / queries)
    - Encapsular el uso de colecciones Mongo
    - NO contener lógica de negocio
    """

    def __init__(self, uri: str, db_name: str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]

    # ─────────────────────────────
    # 🔹 DEVOLUCIONES
    # ─────────────────────────────
    def get_devoluciones(
        self,
        *,
        desde=None,
        hasta=None,
        vendedor_id=None,
        estatus=None,
        filtro=None,
    ):
        """
        Devuelve devoluciones filtradas.

        CONTRATO:
        - Este método es el ÚNICO punto que habla con Mongo.find()
        - Acepta:
            - filtro: dict Mongo completo (prioritario)
            - desde / hasta: datetime
            - vendedor_id
            - estatus

        NOTA:
        - Si viene `filtro`, se mezcla con los demás filtros
        - No convierte tipos (eso ya viene hecho desde queries)
        """

        query = {}

        # ───── Filtro Mongo directo (queries nuevas) ─────
        if isinstance(filtro, dict):
            query.update(filtro)

        # ───── Filtro por fecha ─────
        if desde and hasta:
            query["fecha"] = {"$gte": desde, "$lte": hasta}
        elif desde:
            query["fecha"] = {"$gte": desde}
        elif hasta:
            query["fecha"] = {"$lte": hasta}

        # ───── Filtro por vendedor ─────
        if vendedor_id:
            query["vendedor_id"] = vendedor_id

        # ───── Filtro por estatus ─────
        if estatus:
            query["estatus"] = estatus

        # ───── Ejecución Mongo ─────
        return list(self._db.devoluciones.find(query))


    def aggregate_devoluciones(self, pipeline: list) -> list:
        """
        Ejecuta un aggregate sobre la colección devoluciones.
        Usado por ReportesQueries.
        """
        return list(self._db.devoluciones.aggregate(pipeline))

    def get_articulos(self, devolucion_id):
        """
        Devuelve los artículos de una devolución.

        NO accede directamente a la colección,
        reutiliza get_devoluciones() para mantener consistencia.
        """
        data = self.get_devoluciones(
            filtro={"_id": devolucion_id}
        )

        if not data:
            return []

        return data[0].get("articulos", [])

    def get_devolucion_completa(self, devolucion_id):
        """
        Devuelve la devolución completa (encabezado + artículos).
        """
        data = self.get_devoluciones(
            filtro={"_id": devolucion_id}
        )

        if not data:
            return None

        return data[0]

    def insertar_devolucion(
        self,
        *,
        devolucion_id,
        fecha,
        folio,
        cliente,
        direccion,
        motivo,
        zona,
        total,
        articulos,
        vendedor_id=None,
        estatus="pendiente",
    ):
        """
        Inserta una devolución nueva.
        """
        self._db.devoluciones.insert_one({
            "_id": devolucion_id,
            "fecha": fecha,
            "folio": folio,
            "cliente": cliente,
            "direccion": direccion,
            "motivo": motivo,
            "zona": zona,
            "total": total,
            "articulos": articulos,
            "vendedor_id": vendedor_id,
            "estatus": estatus,
        })

    def actualizar_devolucion(
        self,
        devolucion_id,
        *,
        fecha=None,
        folio=None,
        cliente=None,
        direccion=None,
        motivo=None,
        zona=None,
        items=None,
        vendedor_id=None,
        estatus=None,
    ):
        """
        Actualiza campos de una devolución.
        """
        update = {}

        if fecha is not None:
            update["fecha"] = fecha
        if folio is not None:
            update["folio"] = folio
        if cliente is not None:
            update["cliente"] = cliente
        if direccion is not None:
            update["direccion"] = direccion
        if motivo is not None:
            update["motivo"] = motivo
        if zona is not None:
            update["zona"] = zona
        if items is not None:
            update["articulos"] = items
        if vendedor_id is not None:
            update["vendedor_id"] = vendedor_id
        if estatus is not None:
            update["estatus"] = estatus

        if update:
            self._db.devoluciones.update_one(
                {"_id": devolucion_id},
                {"$set": update}
            )

    def eliminar_devolucion(self, devolucion_id):
        """
        Elimina una devolución.
        """
        self._db.devoluciones.delete_one(
            {"_id": devolucion_id}
        )

    # ─────────────────────────────
    # 🔹 PERSONAL
    # ─────────────────────────────
    def listar_personal(self, solo_activos=True):
        query = {}
        if solo_activos:
            query["activo"] = True
        return list(self._db.personal.find(query))

    def crear_persona(self, nombre: str) -> str:
        res = self._db.personal.insert_one({
            "nombre": nombre,
            "activo": True
        })
        return str(res.inserted_id)

    def actualizar_persona(self, persona_id: str, nuevo_nombre: str):
        self._db.personal.update_one(
            {"_id": persona_id},
            {"$set": {"nombre": nuevo_nombre}}
        )

    def eliminar_persona(self, persona_id: str):
        self._db.personal.delete_one(
            {"_id": persona_id}
        )

    # ─────────────────────────────
    # 🔹 ASIGNACIONES
    # ─────────────────────────────
    def listar_asignaciones(self):
        return list(self._db.asignaciones.find())

    def crear_asignacion(
        self,
        pasillo,
        persona_id,
        fecha_desde,
        fecha_hasta
    ):
        self._db.asignaciones.insert_one({
            "pasillo": pasillo,
            "persona_id": persona_id,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        })

    def actualizar_asignacion(
        self,
        asignacion_id,
        pasillo,
        persona_id,
        fecha_desde,
        fecha_hasta
    ):
        self._db.asignaciones.update_one(
            {"_id": asignacion_id},
            {"$set": {
                "pasillo": pasillo,
                "persona_id": persona_id,
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            }}
        )

    def eliminar_asignaciones_por_persona(self, persona_id):
        self._db.asignaciones.delete_many(
            {"persona_id": persona_id}
        )

    # ─────────────────────────────
    # 🔹 VENDEDORES
    # ─────────────────────────────
    def listar_vendedores(self, solo_activos=True):
        query = {}
        if solo_activos:
            query["activo"] = True
        return list(self._db.vendedores.find(query))

    # ─────────────────────────────
    # 🔹 LIFECYCLE
    # ─────────────────────────────
    def close(self):
        """
        Cierra la conexión MongoDB.
        """
        self._client.close()

# ─────────────────────────────
# 🔹 ANALYTICS DEVOLUCIONES
# ────────────────────────────

    def aggregate_kpis_devoluciones(self, *, collection: str):
        """
        KPIs:
        - total devoluciones
        - total piezas (sum items.cantidad)
        - importe total
        """
        pipeline = [
            {
                "$unwind": {
                    "path": "$items",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$group": {
                    "_id": None,
                    "ids": {"$addToSet": "$_id"},
                    "piezas": {
                        "$sum": {"$ifNull": ["$items.cantidad", 0]}
                    },
                    "importe": {
                        "$sum": {"$ifNull": ["$total", 0]}
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total": {"$size": "$ids"},
                    "piezas": 1,
                    "importe": 1
                }
            }
        ]

        res = list(self._db[collection].aggregate(pipeline))
        if not res:
            return {"total": 0, "piezas": 0, "importe": 0}

        return res[0]
