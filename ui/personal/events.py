from tkinter import messagebox
from datetime import date


class PersonalEvents:
    """
    Callbacks de PERSONAL y ASIGNACIONES.

    Responsabilidades:
    - Alta / selección / eliminación de personal
    - Alta / edición / eliminación de asignaciones
    - Orquestar UI → Services
    """

    def __init__(self, personal_service, asignaciones_service):
        self.personal_service = personal_service
        self.asignaciones_service = asignaciones_service

        self.persona_id_sel = None
        self.asignacion_id = None

    # ─────────────────────────
    # BIND
    # ─────────────────────────
    def bind(self, form, tables):
        self.form = form
        self.tables = tables

        # ── Botones PERSONAL
        self.form.btn_add.config(command=self._agregar_persona)
        self.form.btn_clear.config(command=self._limpiar_form_persona)
        self.form.btn_delete.config(command=self._eliminar_persona)

        # ── Botones ASIGNACIÓN
        self.form.btn_save_asig.config(command=self._guardar_asignacion)
        self.form.btn_cancel_asig.config(command=self._cancelar_edicion)
        self.form.btn_delete_asig.config(command=self._eliminar_asignacion)

        # ── Selecciones TABLAS
        self.tables.tbl_personal.bind(
            "<<TreeviewSelect>>", self._on_select_persona
        )
        self.tables.tbl_asig.bind(
            "<<TreeviewSelect>>", self._on_select_asignacion
        )

    # ─────────────────────────
    # REFRESH GENERAL
    # ─────────────────────────
    def refresh_all(self):
        self._refresh_personal()
        self._refresh_asignaciones()
        self._limpiar_form_persona()
        self._cancelar_edicion()

    # ─────────────────────────
    # PERSONAL
    # ─────────────────────────
    def _refresh_personal(self):
        self.tables.tbl_personal.delete(
            *self.tables.tbl_personal.get_children()
        )

        df = self.personal_service.listar_personal_operativo()
        nombres = []

        for _, p in df.iterrows():
            self.tables.tbl_personal.insert(
                "",
                "end",
                values=(p["id"], p["nombre"])
            )
            nombres.append(p["nombre"])

        self.form.cb_persona["values"] = nombres

    def _agregar_persona(self):
        nombre = self.form.var_nombre.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Dato requerido",
                "Ingresa el nombre del personal."
            )
            return

        try:
            self.personal_service.crear_persona(nombre)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self._limpiar_form_persona()
        self._refresh_personal()

    def _on_select_persona(self, _):
        sel = self.tables.tbl_personal.selection()
        if not sel:
            return

        pid, nombre = self.tables.tbl_personal.item(sel[0], "values")

        self.persona_id_sel = pid
        self.form.var_nombre.set(nombre)
        self.form.btn_delete.state(["!disabled"])

    def _limpiar_form_persona(self):
        self.persona_id_sel = None
        self.form.var_nombre.set("")
        self.form.btn_delete.state(["disabled"])

    def _eliminar_persona(self):
        if not self.persona_id_sel:
            return

        if self.asignaciones_service.tiene_asignaciones(self.persona_id_sel):
            messagebox.showerror(
                "No permitido",
                "Este personal tiene asignaciones activas.\n"
                "Cancélalas antes de eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Eliminar este registro de personal?\n"
            "Esta acción NO se puede deshacer."
        )

        if not confirmar:
            return

        try:
            self.personal_service.eliminar(self.persona_id_sel)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.refresh_all()

    # ─────────────────────────
    # ASIGNACIONES
    # ─────────────────────────
    def _refresh_asignaciones(self):
        self.tables.tbl_asig.delete(
            *self.tables.tbl_asig.get_children()
        )

        for r in self.asignaciones_service.listar_asignaciones():
            self.tables.tbl_asig.insert(
                "",
                "end",
                iid=r["id"],
                values=(
                    r["pasillo"],
                    r["persona"],
                    r["desde"],
                    r["hasta"],
                )
            )

    def _guardar_asignacion(self):
        pasillo = self.form.var_pasillo.get()
        persona = self.form.var_persona.get()

        if not pasillo or not persona:
            messagebox.showwarning(
                "Datos incompletos",
                "Selecciona pasillo y persona."
            )
            return

        desde = self.form.dt_desde.get_date().isoformat()
        hasta = self.form.dt_hasta.get_date().isoformat()

        try:
            if self.asignacion_id:
                self.asignaciones_service.actualizar_asignacion(
                    self.asignacion_id,
                    pasillo,
                    persona,
                    desde,
                    hasta
                )
            else:
                self.asignaciones_service.crear_asignacion(
                    pasillo,
                    persona,
                    desde,
                    hasta
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.refresh_all()

    def _on_select_asignacion(self, _):
        sel = self.tables.tbl_asig.selection()
        if not sel:
            return

        self.asignacion_id = sel[0]
        r = self.tables.tbl_asig.item(self.asignacion_id, "values")

        self.form.var_pasillo.set(r[0])
        self.form.var_persona.set(r[1])
        self.form.dt_desde.set_date(r[2])
        self.form.dt_hasta.set_date(r[3] or date.today())

        self.form.btn_save_asig.config(
            text="Actualizar asignación"
        )
        self.form.btn_cancel_asig.state(["!disabled"])
        self.form.btn_delete_asig.state(["!disabled"])

    def _eliminar_asignacion(self):
        if not self.asignacion_id:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Eliminar esta asignación?\n"
            "Esta acción NO se puede deshacer."
        )

        if not confirmar:
            return

        try:
            self.asignaciones_service.eliminar(self.asignacion_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.refresh_all()

    def _cancelar_edicion(self):
        self.asignacion_id = None

        self.form.var_pasillo.set("")
        self.form.var_persona.set("")
        self.form.dt_desde.set_date(date.today())
        self.form.dt_hasta.set_date(date.today())

        self.form.btn_save_asig.config(
            text="Guardar asignación"
        )
        self.form.btn_cancel_asig.state(["disabled"])
        self.form.btn_delete_asig.state(["disabled"])
