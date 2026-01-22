from os import getenv

from db.mongo.client import MongoClientProvider
from db.mongo.resolver import resolver_coleccion_devoluciones

# ─────────────────────────────────────────────
# REPOSITORIOS
# ─────────────────────────────────────────────
from db.mongo.repos.productos_repo import ProductosRepo
from db.mongo.repos.devoluciones_repo import DevolucionesRepo
from db.mongo.repos.personal_repo import PersonalRepo
from db.mongo.repos.vendedores_repo import VendedoresRepo
from db.mongo.repos.asignaciones_repo import AsignacionesRepo

# ─────────────────────────────────────────────
# SERVICES / FACADES
# ─────────────────────────────────────────────
from services.productos_service import ProductosService
from services.devoluciones.facade import DevolucionesService


# ─────────────────────────────────────────────
# DB BASE
# ─────────────────────────────────────────────
def get_db():
    """
    Devuelve el proveedor Mongo (infraestructura).

    RESPONSABILIDAD:
    - Leer variables de entorno
    - Inicializar MongoClientProvider
    - NO contiene lógica de negocio
    """
    uri = getenv("MONGO_URI")
    db_name = getenv("MONGO_DB")

    if not uri or not db_name:
        raise RuntimeError(
            "Variables de entorno MONGO_URI y MONGO_DB no definidas"
        )

    return MongoClientProvider(uri, db_name)


# ─────────────────────────────────────────────
# REPOSITORIOS
# ─────────────────────────────────────────────
def get_productos_repo():
    """
    Devuelve el repositorio de productos.
    """
    db_provider = get_db()
    return ProductosRepo(db_provider._db)


def get_devoluciones_repo(*, motivo: str):
    """
    Devuelve el repositorio de devoluciones,
    resolviendo la colección según el motivo.
    """
    db_provider = get_db()
    db = db_provider._db

    collection_name = resolver_coleccion_devoluciones(motivo)

    return DevolucionesRepo(
        db=db,
        collection_name=collection_name,
    )


def get_personal_repo():
    """
    Devuelve el repositorio de personal.
    """
    db_provider = get_db()
    return PersonalRepo(db_provider._db)


def get_vendedores_repo():
    """
    Devuelve el repositorio de vendedores.
    """
    db_provider = get_db()
    return VendedoresRepo(db_provider._db)


# ─────────────────────────────────────────────
# SERVICES / FACADES
# ─────────────────────────────────────────────
def get_productos_service():
    """
    Devuelve el servicio de productos correctamente cableado.
    """
    repo = get_productos_repo()
    return ProductosService(repo)


def get_devoluciones_service(*, motivo: str):
    """
    Devuelve la fachada de devoluciones correctamente cableada.

    NOTA CLAVE:
    - El facade NO decide la colección
    - El repo YA viene resuelto por motivo
    - La UI solo consume esta fachada
    """
    return DevolucionesService(
        devoluciones_repo=get_devoluciones_repo(motivo=motivo),
        productos_repo=get_productos_repo(),
        personal_repo=get_personal_repo(),
        vendedores_repo=get_vendedores_repo(),
    )

def get_asignaciones_repo():
    """
    Devuelve el repositorio de asignaciones de pasillo.
    """
    db_provider = get_db()
    return AsignacionesRepo(db_provider._db)
