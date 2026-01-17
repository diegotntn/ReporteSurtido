import pandas as pd
from domain.personal import Persona


class PersonalService:
    """
    Lógica de negocio EXCLUSIVA de PERSONAL.

    REGLAS:
    - Service NO accede a Mongo
    - Service SOLO usa PersonalRepo
    - NO maneja asignaciones
    """

    def __init__(self, personal_repo):
        self.repo = personal_repo

    # ─────────────────────────
    # PERSONAL
    # ─────────────────────────
    def crear_persona(self, nombre: str) -> str:
        persona = Persona(
            id="tmp",
            nombre=(nombre or "").strip()
        )
        persona.validar_nombre()

        return self.repo.crear(persona.nombre)

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
