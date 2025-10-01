import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
class ConfiguracionTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
    def _crear_campo_entry(self, parent, label_text, value):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w")
        entry = ctk.CTkEntry(parent, width=35)
        entry.insert(0, value)
        entry.pack(fill="x", pady=2)
        return entry

    def _crear_campo_combobox(self, parent, label_text, value, values_list):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w")
        combo = ctk.CTkComboBox(parent, values=values_list, state="readonly")
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
        # Limpiar la pestaña antes de volver a dibujarla
        for widget in self.winfo_children():
            widget.destroy()
            
        # El controller nos da la configuración actual
        config = self.controller.get_configuracion()
        
        # --- Frame principal con scrollbar ---
        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True)
        
        frame_principal = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        frame_principal.pack(fill="x", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(frame_principal, text="CONFIGURACIÓN DEL SISTEMA", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 20))
        
        frame_negocio = ctk.CTkFrame(frame_principal, border_width=1)
        frame_negocio.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(frame_negocio, text="Información del Negocio", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))
        
        frame_nombre_inner = ctk.CTkFrame(frame_negocio, fg_color="transparent")
        frame_nombre_inner.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(frame_nombre_inner, text="Nombre:", font=("Segoe UI", 12)).pack(anchor="w", pady=2)
        self.entry_nombre_comercio = ctk.CTkEntry(frame_nombre_inner)
        self.entry_nombre_comercio.insert(0, config.get("nombre_comercio", ""))
        self.entry_nombre_comercio.pack(fill="x", pady=2)
        
        frame_tema = ctk.CTkFrame(frame_principal, border_width=1)
        frame_tema.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(frame_tema, text="Apariencia", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))

        frame_combo_tema = ctk.CTkFrame(frame_tema, fg_color="transparent")
        frame_combo_tema.pack(fill="x", padx=10, pady=(0, 5))
        ctk.CTkLabel(frame_combo_tema, text="Tema:", font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        
        # 1. Definimos los temas en español y un mapa para la traducción
        temas_en_espanol = ["Oscuro", "Claro", "Sistema"]
        mapa_temas = {
            "dark": "Oscuro",
            "light": "Claro",
            "system": "Sistema"
        }
        
        # 2. Creamos el ComboBox con los nombres en español
        self.combo_tema = ctk.CTkComboBox(frame_combo_tema, values=temas_en_espanol)
        
        # 3. Obtenemos el tema actual (ej: "dark") y lo convertimos a español (ej: "Oscuro") para mostrarlo
        tema_actual_en = config.get("tema", "dark")
        tema_actual_es = mapa_temas.get(tema_actual_en, "Oscuro")
        self.combo_tema.set(tema_actual_es)
        
        self.combo_tema.pack(fill="x", pady=2)
        
        ctk.CTkLabel(frame_tema, text="Los cambios de tema ahora son instantáneos.", font=ctk.CTkFont(size=10, slant="italic")).pack(anchor="w", pady=(0, 10), padx=10)

        
        frame_inventario = ctk.CTkFrame(frame_principal, border_width=1)
        frame_inventario.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(frame_inventario, text="Inventario", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))
        
        self.var_alertas = tk.BooleanVar(value=config.get("mostrar_alertas_stock", True))
        check_alertas = ctk.CTkCheckBox(frame_inventario, text="Mostrar alertas de stock bajo", variable=self.var_alertas)
        check_alertas.pack(anchor="w", pady=10, padx=10)

        frame_umbral = ctk.CTkFrame(frame_inventario, fg_color="transparent")
        frame_umbral.pack(fill="x", pady=(0, 10), padx=10)
        ctk.CTkLabel(frame_umbral, text="Umbral alertas:", font=("Segoe UI", 10)).pack(side="left")
        self.spin_umbral = ttk.Spinbox(frame_umbral, from_=1, to=50, width=8, font=("Segoe UI", 10))
        self.spin_umbral.set(config.get("umbral_alerta_stock", 5))
        self.spin_umbral.pack(side="left", padx=(5, 0))
        
        # --- Botones de Acción (Corregidos) ---
        frame_botones = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botones.pack(fill="x", pady=20, padx=10)
        btn_aplicar = ctk.CTkButton(frame_botones, text="💾 Aplicar", command=self._aplicar_configuracion)
        btn_aplicar.pack(side="left", padx=5)
        btn_restaurar = ctk.CTkButton(frame_botones, text="↩️ Restaurar", command=self._restaurar_valores_por_defecto)
        btn_restaurar.pack(side="left", padx=5)

    def _aplicar_configuracion(self):
        
        mapa_temas_inverso = {
            "Oscuro": "dark",
            "Claro": "light",
            "Sistema": "system"
        }
        tema_seleccionado_es = self.combo_tema.get()
        tema_interno_en = mapa_temas_inverso.get(tema_seleccionado_es, "dark")

        nuevos_valores = {
            "nombre_comercio": self.entry_nombre_comercio.get().strip(),
            "tema": tema_interno_en, # Usamos el valor traducido
            "mostrar_alertas_stock": self.var_alertas.get(),
            "umbral_alerta_stock": int(self.spin_umbral.get()),
            "pin_admin": self.controller.configuracion.get("pin_admin")
        }
        
        self.controller.aplicar_y_guardar_config(nuevos_valores)