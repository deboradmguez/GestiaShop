from tkinter import ttk
import customtkinter as ctk

def apply_custom_theme(app):
    """
    Aplica un estilo personalizado y consistente a los widgets de ttk,
    integrándolos perfectamente con el tema de CustomTkinter.
    """
    # Obtener los colores actuales del tema de CustomTkinter
    appearance_mode = ctk.get_appearance_mode().lower()
    
    # IMPORTANTE: Detectar correctamente el tema
    if appearance_mode in ["dark", "sistema"] and ctk.get_appearance_mode() == "Dark":
        # Colores para tema oscuro
        bg_color = "#212121"  # Fondo principal más oscuro
        fg_color = "#FFFFFF"  # Texto blanco
        header_bg = "#2B2B2B"  # Fondo del header
        selected_bg = "#1F538D"  # Azul de selección
        field_bg = "#2B2B2B"  # Fondo de campos
        border_color = "#3E3E3E"  # Color de bordes
        hover_color = "#404040"  # Color hover
        entry_bg = "#343638"  # Fondo de entrada
    else:
        # Colores para tema claro
        bg_color = "#FFFFFF"
        fg_color = "#000000"
        header_bg = "#F0F0F0"
        selected_bg = "#0078D4"
        field_bg = "#FFFFFF"
        border_color = "#CCCCCC"
        hover_color = "#E5E5E5"
        entry_bg = "#FFFFFF"
    
    print(f"DEBUG: Aplicando tema {appearance_mode}, bg_color: {bg_color}, fg_color: {fg_color}")

    style = ttk.Style(app)
    
    # Usar 'clam' como tema base para mejor compatibilidad
    try:
        style.theme_use("clam")
    except:
        # Fallback si clam no está disponible
        style.theme_use("default")

    # === CONFIGURACIÓN DEL TREEVIEW ===
    style.configure(
        "Treeview",
        background=bg_color,
        foreground=fg_color,
        fieldbackground=bg_color,  # Fondo del área de datos
        selectbackground=selected_bg,
        selectforeground="#FFFFFF",
        borderwidth=0,
        lightcolor=bg_color,
        darkcolor=bg_color,
        rowheight=30,
        relief="flat"
    )
    
    # Mapeo de estados para Treeview
    style.map(
        "Treeview",
        background=[('selected', selected_bg), ('!selected', bg_color)],
        foreground=[('selected', '#FFFFFF'), ('!selected', fg_color)]
    )
    
    # Configuración del header del Treeview
    style.configure(
        "Treeview.Heading",
        background=header_bg,
        foreground=fg_color,
        font=("Segoe UI", 10, "bold"),
        borderwidth=1,
        relief="flat",
        padding=(10, 8)
    )
    
    # Layout del header para eliminar bordes
    style.layout("Treeview.Heading", [
        ('Treeview.heading', {
            'sticky': 'nswe',
            'children': [
                ('Treeview.padding', {
                    'sticky': 'nswe',
                    'children': [
                        ('Treeview.label', {'sticky': 'nswe'})
                    ]
                })
            ]
        })
    ])
    
    style.map(
        "Treeview.Heading",
        background=[('active', hover_color), ('!active', header_bg)],
        foreground=[('active', fg_color), ('!active', fg_color)]
    )

    # === CONFIGURACIÓN DE ENTRY ===
    style.configure(
        "TEntry",
        fieldbackground=entry_bg,
        foreground=fg_color,
        borderwidth=1,
        relief="flat",
        insertcolor=fg_color,
        selectbackground=selected_bg,
        selectforeground="#FFFFFF"
    )

    style.map(
        "TEntry",
        fieldbackground=[('focus', entry_bg), ('!focus', entry_bg)],
        bordercolor=[('focus', selected_bg), ('!focus', border_color)],
        lightcolor=[('focus', selected_bg), ('!focus', border_color)],
        darkcolor=[('focus', selected_bg), ('!focus', border_color)]
    )

    # === CONFIGURACIÓN DE BUTTON ===
    style.configure(
        "TButton",
        background=header_bg,
        foreground=fg_color,
        borderwidth=1,
        relief="flat",
        padding=(10, 6)
    )
    
    style.map(
        "TButton",
        background=[('active', hover_color), ('pressed', selected_bg), ('!active', header_bg)],
        foreground=[('pressed', '#FFFFFF'), ('!pressed', fg_color)]
    )

    # === CONFIGURACIÓN DE COMBOBOX ===
    style.configure(
        "TCombobox",
        fieldbackground=entry_bg,
        background=entry_bg,
        foreground=fg_color,
        borderwidth=1,
        relief="flat",
        selectbackground=selected_bg,
        selectforeground="#FFFFFF",
        arrowcolor=fg_color
    )
    
    style.map(
        "TCombobox",
        fieldbackground=[('focus', entry_bg), ('readonly', entry_bg)],
        selectbackground=[('focus', selected_bg)],
        bordercolor=[('focus', selected_bg), ('!focus', border_color)]
    )

    # === CONFIGURACIÓN DE SPINBOX ===
    style.configure(
        "TSpinbox",
        fieldbackground=entry_bg,
        background=entry_bg,
        foreground=fg_color,
        borderwidth=1,
        relief="flat",
        insertcolor=fg_color,
        selectbackground=selected_bg,
        selectforeground="#FFFFFF",
        arrowcolor=fg_color
    )
    
    style.map(
        "TSpinbox",
        fieldbackground=[('focus', entry_bg), ('!focus', entry_bg)],
        bordercolor=[('focus', selected_bg), ('!focus', border_color)]
    )

    # === CONFIGURACIÓN DE FRAME ===
    style.configure(
        "TFrame",
        background=bg_color,
        borderwidth=0,
        relief="flat"
    )

    # === CONFIGURACIÓN DE LABEL ===
    style.configure(
        "TLabel",
        background=bg_color,
        foreground=fg_color
    )

    # === CONFIGURACIÓN DE SCROLLBAR ===
    style.configure(
        "Vertical.TScrollbar",
        background=header_bg,
        troughcolor=bg_color,
        borderwidth=0,
        arrowcolor=fg_color,
        relief="flat"
    )
    
    style.map(
        "Vertical.TScrollbar",
        background=[('active', hover_color), ('pressed', selected_bg)]
    )


def apply_dark_theme_to_all_treeviews(parent_widget, exclude_widgets=None):
    if exclude_widgets is None:
        exclude_widgets = []

    # Ya no necesitamos llamar a ttk.Style() aquí
    current_mode = ctk.get_appearance_mode()

    if current_mode == "Dark":
        anulada_bg = "#3c3c3c"
        anulada_fg = "#ff6b6b"
    else:
        anulada_bg = "#ffebee"
        anulada_fg = "#c62828"

    def apply_to_widget(widget):
        if isinstance(widget, ttk.Treeview) and widget not in exclude_widgets:
            try:
                # La única responsabilidad de esta función ahora es configurar los tags.
                widget.tag_configure("anulada", background=anulada_bg, foreground=anulada_fg)
                widget.tag_configure("parent", font=("Segoe UI", 10, "bold"))
                widget.tag_configure("child", font=("Segoe UI", 9))
                print(f"DEBUG: Tags configurados para el Treeview en modo {current_mode}")

            except Exception as e:
                print(f"DEBUG: Error aplicando tags a Treeview: {e}")

        for child in widget.winfo_children():
            apply_to_widget(child)

    apply_to_widget(parent_widget)

def update_theme_dynamically(app, new_appearance_mode):
    """
    Actualiza el tema dinámicamente cuando cambia el modo de apariencia.
    """
    # Aplicar el nuevo tema
    ctk.set_appearance_mode(new_appearance_mode)
    
    # Aplicar el tema personalizado
    apply_custom_theme(app)
    
    # Actualizar el título de la aplicación para reflejar el cambio
    app.actualizar_titulo_app()
    
    # Aplicar colores a todos los Treeview existentes
    app.after(50, lambda: apply_dark_theme_to_all_treeviews(app))
    
    # Forzar actualización completa de la interfaz
    def force_complete_update():
        # Actualizar todos los frames principales
        for widget in app.winfo_children():
            if widget in (app.lbl_notificacion, app.btn_soporte, app.btn_alerta_stock):
                continue
            
            try:
                widget.update_idletasks()
                if hasattr(widget, 'configure'):
                    widget.configure(fg_color="transparent")
            except:
                pass
        
        # Forzar redibujado completo
        app.update()
        app.update_idletasks()
        
        app.after(50, lambda: apply_dark_theme_to_all_treeviews(app))
    
    # Ejecutar la actualización completa después de un breve delay
    app.after(100, force_complete_update)

def apply_theme_change_and_restart_notification(app, new_theme):
    """
    Guarda el cambio de tema en configuración y muestra opción de reiniciar.
    NO aplica el tema inmediatamente - solo al reiniciar.
    """
    from utilities.dialogs import ConfirmacionDialog
    
    # SOLO guardar en configuración, NO aplicar visualmente
    app.configuracion["tema"] = new_theme
    
    # Mostrar diálogo para reiniciar
    dialogo = ConfirmacionDialog(
        parent=app,
        title="Cambio de Tema",
        message=f"Tema configurado como {new_theme}.\n\nPara aplicar los cambios, necesita reiniciar la aplicación.\n\n¿Desea reiniciar ahora?"
    )
    
    respuesta = dialogo.show()
    if respuesta:
        # Solo reiniciar SI el usuario dice que sí
        import sys
        import os
        app.destroy()
        os.execv(sys.executable, ['python'] + sys.argv)
    # Si dice que no, no hace nada - el tema se aplicará en el próximo reinicio

def save_theme_change_only(app, new_theme):
    """
    Solo guarda el cambio de tema sin aplicar cambios visuales.
    Para usar cuando solo quieres guardar la preferencia.
    """
    app.configuracion["tema"] = new_theme
    print(f"DEBUG: Tema {new_theme} guardado en configuración, se aplicará al reiniciar")