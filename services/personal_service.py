import pandas as pd
from domain.personal import Persona


class PersonalService:
    """
    Lógica de negocio EXCLUSIVA de PERSONAL.

    REGLAS:
    - Service NO accede a Mongo directamente
    - Service SOLO usa PersonalRepo
    - NO maneja asignaciones
    - NO conoce UI
    """

    def __init__(self, personal_repo):
        self.repo = personal_repo

    # ─────────────────────────
    # CREAR
    # ─────────────────────────
    def crear_persona(self, nombre: str) -> str:
        persona = Persona(
            id="tmp",
            nombre=(nombre or "").strip()
        )
        persona.validar_nombre()

        return self.repo.crear(persona.nombre)

    # ─────────────────────────
    # LISTAR
    # ─────────────────────────
    def listar_personal_operativo(self) -> pd.DataFrame:
        """
        Devuelve personal ACTIVO.
        """
        df = self.repo.listar_personal(solo_activos=True)

        if df.empty:
            return df

        if "_id" in df.columns:
            df["id"] = df["_id"].astype(str)

        return df

    # ─────────────────────────
    # ELIMINAR
    # ─────────────────────────
    def eliminar(self, persona_id: str):
        """
        Elimina una persona por ID.

        NOTA:
        - La validación de asignaciones NO va aquí
        - Events ya valida antes de llamar
        """
        if not persona_id:
            raise ValueError("Persona no especificada")

        self.repo.eliminar(persona_id)
