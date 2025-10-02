import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class ConfiguracionTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
    def _aplicar_configuracion(self):
        """Recolecta los nuevos valores de la UI y se los pasa al controlador."""
        mapa_temas_inverso = {
            "Oscuro": "dark", "Claro": "light", "Sistema": "system"
        }
        tema_seleccionado_es = self.combo_tema.get()
        tema_interno_en = mapa_temas_inverso.get(tema_seleccionado_es, "dark")

        nuevos_valores = {
            "nombre_comercio": self.entry_nombre_comercio.get().strip(),
            "tema": tema_interno_en,
            "mostrar_alertas_stock": self.var_alertas.get(),
            "umbral_alerta_stock": int(self.spin_umbral.get()),
            "pin_admin": self.controller.configuracion.get("pin_admin")
        }
        
        self.controller.aplicar_y_guardar_config(nuevos_valores)

    def _restaurar_valores_por_defecto(self):
        """Llama al método del controlador para iniciar la restauración."""
        self.controller.restaurar_config_default()

    def recargar_vista(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        config = self.controller.get_configuracion()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0) 
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=1, pady=20, padx=20, sticky="n")

        # --- ENCABEZADO (Solo Título) ---
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="CONFIGURACIÓN DEL SISTEMA", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        # --- SECCIONES DE CONTENIDO ---
        frame_negocio = ctk.CTkFrame(main_container, border_width=1)
        frame_negocio.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(frame_negocio, text="Información del Negocio", font=ctk.CTkFont(weight="bold")).pack(pady=10, padx=15)
        self.entry_nombre_comercio = ctk.CTkEntry(frame_negocio)
        self.entry_nombre_comercio.insert(0, config.get("nombre_comercio", ""))
        self.entry_nombre_comercio.pack(fill="x", padx=15, pady=(0, 15))

        frame_tema = ctk.CTkFrame(main_container, border_width=1)
        frame_tema.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(frame_tema, text="Apariencia", font=ctk.CTkFont(weight="bold")).pack(pady=10, padx=15)
        temas_en_espanol = ["Oscuro", "Claro", "Sistema"]
        mapa_temas = {"dark": "Oscuro", "light": "Claro", "system": "Sistema"}
        self.combo_tema = ctk.CTkComboBox(frame_tema, values=temas_en_espanol)
        tema_actual_en = config.get("tema", "dark")
        self.combo_tema.set(mapa_temas.get(tema_actual_en, "Oscuro"))
        self.combo_tema.pack(fill="x", padx=15, pady=(0, 15))

        frame_alertas = ctk.CTkFrame(main_container, border_width=1)
        frame_alertas.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(frame_alertas, text="Alertas de Stock", font=ctk.CTkFont(weight="bold")).pack(pady=10, padx=15)
        
        self.var_alertas = tk.BooleanVar(value=config.get("mostrar_alertas_stock", True))
        check_alertas = ctk.CTkCheckBox(frame_alertas, text="Mostrar alertas de stock bajo", variable=self.var_alertas)
        check_alertas.pack(anchor="w", pady=10, padx=15)

        frame_umbral = ctk.CTkFrame(frame_alertas, fg_color="transparent")
        frame_umbral.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(frame_umbral, text="Umbral para alertas:", font=("Segoe UI", 12)).pack(side="left")
        self.spin_umbral = ttk.Spinbox(frame_umbral, from_=1, to=50, width=8, font=("Segoe UI", 10))
        self.spin_umbral.set(config.get("umbral_alerta_stock", 5))
        self.spin_umbral.pack(side="left", padx=10)

        # --- INICIO DE LA MODIFICACIÓN ---

        # 1. Creamos un frame para los botones que se alineará a la derecha
        frame_botones = ctk.CTkFrame(main_container, fg_color="transparent")
        frame_botones.pack(fill="x", pady=20, padx=0)

        # 2. Creamos los botones con colores diferenciados
        btn_restaurar = ctk.CTkButton(
            frame_botones, 
            text="↩️ Restaurar", 
            command=self._restaurar_valores_por_defecto,
            fg_color="transparent", # Color de "peligro" o secundario
            border_width=2,
            text_color=("gray10", "#DCE4EE")
        )
        btn_restaurar.pack(side="right")
        
        btn_aplicar = ctk.CTkButton(
            frame_botones, 
            text="💾 Guardar Cambios", 
            command=self._aplicar_configuracion,
            fg_color="#28a745" # Color de "éxito" o principal
        )
        btn_aplicar.pack(side="right", padx=(0, 10))
        
        # --- FIN DE LA MODIFICACIÓN ---