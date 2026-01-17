from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


MOTIVOS_VENTA = {"cliente", "captura", "precio"}

uri=os.getenv("MONGO_URI"),
db_name=os.getenv("MONGO_DB")

def mover_devoluciones_a_ventas():
    client = MongoClient(uri)
    db = client[db_name]

    col_origen = db["devoluciones"]
    col_destino = db["devoluciones_ventas"]
    # ─────────────────────────
    # 1️⃣ Buscar devoluciones a mover
    # ─────────────────────────
    filtro = {
        "motivo": {"$in": list(MOTIVOS_VENTA)}
    }

    docs = list(col_origen.find(filtro))

    if not docs:
        print("✔ No hay devoluciones para mover.")
        return

    print(f"🔎 Encontradas {len(docs)} devoluciones para mover.")

    # ─────────────────────────
    # 2️⃣ Insertar en devoluciones_ventas
    # ─────────────────────────
    resultado_insert = col_destino.insert_many(docs)
    ids_insertados = resultado_insert.inserted_ids

    print(f"📦 Insertadas {len(ids_insertados)} en devoluciones_ventas.")

    # ─────────────────────────
    # 3️⃣ Eliminar de devoluciones
    # ─────────────────────────
    resultado_delete = col_origen.delete_many({
        "_id": {"$in": ids_insertados}
    })

    print(f"🗑 Eliminadas {resultado_delete.deleted_count} de devoluciones.")

    print("✅ Proceso completado correctamente.")


if __name__ == "__main__":
    mover_devoluciones_a_ventas()
