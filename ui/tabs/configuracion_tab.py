import customtkinter as ctk


class ConfiguracionTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
    # --- Funciones de ayuda para crear widgets ---
    def _crear_campo_entry(self, parent, label_text, value):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w")
        entry = ctk.CTkEntry(parent, width=35)
        entry.insert(0, value)
        entry.pack(fill="x", pady=2)
        return entry

    def _crear_campo_combobox(self, parent, label_text, value, values_list):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w")
        combo = ttk.Combobox(parent, values=values_list, state="readonly")
        combo.set(value)
        combo.pack(fill="x", pady=2)
        return combo

    def _crear_campo_spinbox(self, parent, label_text, value):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=2)
        ctk.CTkLabel(frame, text=label_text).pack(side="left")
        spin = ttk.Spinbox(frame, from_=1, to=50, width=8)
        spin.set(value)
        spin.pack(side="left", padx=5)
        return spin

    # --- Métodos que llaman al controlador ---
    def _aplicar_configuracion(self):
        """Recolecta los nuevos valores y se los pasa al controlador."""
        nuevos_valores = {
            "nombre_comercio": self.entry_nombre_comercio.get().strip(),
            "tema": self.combo_tema.get(),
            "mostrar_alertas_stock": self.var_alertas.get(),
            "umbral_alerta_stock": int(self.spin_umbral.get())
        }
        self.controller.aplicar_y_guardar_config(nuevos_valores)

    def _restaurar_valores_por_defecto(self):
        """Pide al controlador que restaure los valores y, si tiene éxito, recarga la vista."""
        if self.controller.restaurar_config_default():
            self.recargar_vista()

    def recargar_vista(self):
        """
        Destruye los widgets existentes y vuelve a crear la interfaz
        con los datos de configuración más recientes.
        """
        # Limpiar la pestaña antes de volver a dibujarla
        for widget in self.winfo_children():
            widget.destroy()
            
        # El controller nos da la configuración actual
        config = self.controller.get_configuracion()
        
        # --- Frame principal con scrollbar ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
        frame_principal = ctk.CTkFrame(scrollable_frame, padding=15)
        frame_principal.pack(fill="x", expand=True)
        
        # --- Widgets de Configuración ---
        
        ctk.CTkLabel(frame_principal, text="CONFIGURACIÓN DEL SISTEMA", font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))
        
        # Negocio
        frame_negocio = ctk.CTkLabelFrame(frame_principal, text="Información del Negocio", padding=10)
        frame_negocio.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_negocio, text="Nombre:", font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        self.entry_nombre_comercio = ctk.CTkEntry(frame_negocio, width=35, font=("Segoe UI", 10))
        self.entry_nombre_comercio.insert(0, config.get("nombre_comercio", ""))
        self.entry_nombre_comercio.pack(fill="x", pady=2)
        
        # Apariencia
        frame_tema = ctk.CTkLabelFrame(frame_principal, text="Apariencia", padding=10)
        frame_tema.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_tema, text="Tema:", font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        temas_disponibles = ["superhero", "darkly", "cyborg", "vapor", "sandstone"]
        self.combo_tema = ttk.Combobox(frame_tema, values=temas_disponibles, font=("Segoe UI", 10), state="readonly")
        self.combo_tema.set(config.get("tema", "superhero"))
        self.combo_tema.pack(fill="x", pady=2)
        
        # --- NUEVO: Label informativo ---
        ctk.CTkLabel(frame_tema, text="Nota: Cambiar el tema reiniciará la aplicación.", font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(5,0))
        
        # Inventario
        frame_inventario = ctk.CTkLabelFrame(frame_principal, text="Inventario", padding=10)
        frame_inventario.pack(fill="x", pady=5)
        self.var_alertas = tk.BooleanVar(value=config.get("mostrar_alertas_stock", True))
        check_alertas = ttk.Checkbutton(frame_inventario, text="Mostrar alertas de stock bajo", variable=self.var_alertas)
        check_alertas.pack(anchor="w", pady=2)
        frame_umbral = ctk.CTkFrame(frame_inventario)
        frame_umbral.pack(fill="x", pady=2)
        ctk.CTkLabel(frame_umbral, text="Umbral alertas:", font=("Segoe UI", 10)).pack(side="left")
        self.spin_umbral = ttk.Spinbox(frame_umbral, from_=1, to=50, width=8, font=("Segoe UI", 10))
        self.spin_umbral.set(config.get("umbral_alerta_stock", 5))
        self.spin_umbral.pack(side="left", padx=(5, 0))
        
        # Botones de Acción
        frame_botones = ctk.CTkFrame(frame_principal)
        frame_botones.pack(fill="x", pady=15)
        btn_aplicar = ctk.CTkButton(frame_botones, text="💾 Aplicar", command=self._aplicar_configuracion, style="success.TButton", width=15)
        btn_aplicar.pack(side="left", padx=5)
        btn_restaurar = ctk.CTkButton(frame_botones, text="↩️ Restaurar", command=self._restaurar_valores_por_defecto, style="warning.TButton", width=15)
        btn_restaurar.pack(side="left", padx=5)