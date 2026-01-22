from tkinter import messagebox

from utils.helpers import pasillo_desde_linea, normalizar_texto_busqueda
from db.factory import get_devoluciones_service


class RegistroEvents:
    """
    Callbacks y lógica de interacción del registro de devoluciones.

    RESPONSABILIDAD:
    - Orquestar UI ↔ Services ↔ Dominio
    - NO conoce Mongo
    - NO conoce colecciones
    - NO decide infraestructura
    """

    def __init__(self, productos_service, on_saved=None):
        """
        Parámetros:
        - productos_service: servicio de productos (autocomplete)
        - on_saved: callback post-guardado
        """
        self.productos_service = productos_service
        self.on_saved = on_saved

        # UI
        self.form = None
        self.form_articulo = None
        self.table = None

        self._btn_guardar = None
        self._btn_agregar = None

        # cache resultados autocomplete
        self._resultados = []

    # ─────────────────────────────────────────
    # BINDING UI
    # ─────────────────────────────────────────
    def bind(
        self,
        form,
        form_articulo,
        table,
        btn_guardar=None,
        btn_agregar=None
    ):
        self.form = form
        self.form_articulo = form_articulo
        self.table = table

        self._btn_guardar = btn_guardar
        self._btn_agregar = btn_agregar

        if self._btn_guardar:
            self._btn_guardar.config(state="disabled")

        # Escuchar escritura (autocomplete)
        self.form_articulo.buscar_var.trace_add(
            "write",
            self._on_buscar_producto
        )

        # Eventos listbox
        lb = self.form_articulo._listbox
        lb.bind("<Double-Button-1>", self._on_listbox_click)
        lb.bind("<Return>", self._on_listbox_enter)

        # Teclas en buscador
        self.form_articulo.buscar.bind("<Down>", self._focus_listbox)
        self.form_articulo.buscar.bind("<Escape>", self._ocultar_sugerencias)

    # ─────────────────────────────────────────
    # AUTOCOMPLETADO
    # ─────────────────────────────────────────
    def _on_buscar_producto(self, *_):
        texto = normalizar_texto_busqueda(
            self.form_articulo.buscar_var.get()
        )

        if len(texto) < 2:
            self._resultados = []
            self.form_articulo.ocultar_sugerencias()
            return

        self._resultados = (
            self.productos_service.buscar_por_clave_o_nombre(texto)
            or []
        )

        self.form_articulo.mostrar_sugerencias(self._resultados)

    def _focus_listbox(self, _event=None):
        if self._resultados:
            lb = self.form_articulo._listbox
            lb.focus_set()
            lb.selection_set(0)

    def _on_listbox_click(self, _event=None):
        self._seleccionar_actual()

    def _on_listbox_enter(self, _event=None):
        self._seleccionar_actual()

    def _seleccionar_actual(self):
        lb = self.form_articulo._listbox
        sel = lb.curselection()

        if not sel:
            return

        producto = self._resultados[sel[0]]
        pasillo = pasillo_desde_linea(producto.get("linea"))

        self.form_articulo.set_producto(
            producto=producto,
            pasillo=pasillo
        )

        self.form_articulo.ocultar_sugerencias()

    def _ocultar_sugerencias(self, _event=None):
        self.form_articulo.ocultar_sugerencias()

    # ─────────────────────────────────────────
    # AGREGAR / ELIMINAR ARTÍCULO
    # ─────────────────────────────────────────
    def on_agregar_articulo(self):
        try:
            data = self.form_articulo.get_data()

            if not data.get("clave"):
                raise ValueError("Selecciona un producto válido")

            if not data.get("pasillo"):
                raise ValueError("Debes seleccionar el pasillo")

            self.table.add_item(
                clave=data["clave"],
                descripcion=data["nombre"],
                cantidad=data["cantidad"],
                precio=data["precio"],
                pasillo=data["pasillo"],
            )

            self.form_articulo.clear()

            if self._btn_guardar:
                self._btn_guardar.config(state="normal")

        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def on_eliminar_articulo(self):
        eliminado = self.table.remove_selected()

        if not eliminado:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un artículo de la tabla"
            )
            return

        if not self.table.get_items() and self._btn_guardar:
            self._btn_guardar.config(state="disabled")

    # ─────────────────────────────────────────
    # GUARDAR DEVOLUCIÓN
    # ─────────────────────────────────────────
    def on_guardar(self):
        try:
            data = self.form.get_data()
            items = self.table.get_items()

            if not items:
                raise ValueError("No hay artículos agregados")

            motivo = data.get("motivo")
            if not motivo:
                raise ValueError("Debes seleccionar un motivo")

            # 🔑 El service se resuelve AQUÍ, cuando ya existe el motivo
            devoluciones_service = get_devoluciones_service(
                motivo=motivo
            )

            devoluciones_service.registrar(
                **data,
                items=items
            )

        except ValueError as e:
            messagebox.showwarning("Error", str(e))
            return

        messagebox.showinfo("OK", "Devolución guardada correctamente")

        # Reset UI
        self.form.clear()
        self.form_articulo.clear()
        self.table.clear()

        if self._btn_guardar:
            self._btn_guardar.config(state="disabled")

        if self.on_saved:
            self.on_saved()
