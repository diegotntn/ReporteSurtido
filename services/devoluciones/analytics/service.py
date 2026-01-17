class DevolucionesAnalyticsService:
    def __init__(self, db_provider):
        self.db = db_provider

    def obtener_kpis(self):
        return {
            "devoluciones": self.db.aggregate_kpis_devoluciones(
                collection="devoluciones"
            ),
            "ventas": self.db.aggregate_kpis_devoluciones(
                collection="devoluciones_ventas"
            ),
        }
