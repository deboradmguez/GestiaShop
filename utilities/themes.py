from tkinter import ttk

def apply_custom_theme(app):
    """
    Aplica un estilo personalizado y consistente a los widgets de ttk,
    integrándolos con el tema de CustomTkinter.
    """
    style = ttk.Style(app)
    
    # Colores del tema oscuro por defecto de CustomTkinter
    bg_color = "#242424"
    fg_color = "#DCE4EE"
    header_bg = "#2B2B2B"
    selected_bg = "#1F6AA5" # Un azul estándar de CTk
    field_bg = "#343638"

    # --- CORRECCIÓN CLAVE ---
    # Usar 'clam' como base es más confiable para la personalización
    # en diferentes sistemas operativos, especialmente para eliminar bordes.
    style.theme_use("clam")

    # --- Estilo del Treeview (Tablas) ---
    style.configure(
        "Treeview",
        background=bg_color,
        foreground=fg_color,
        fieldbackground=field_bg,
        borderwidth=0,
        rowheight=28  # Un poco menos de espacio para un look más compacto
    )
    style.map(
        "Treeview",
        background=[('selected', selected_bg)]
    )
    
    # Estilo de la cabecera del Treeview
    style.configure(
        "Treeview.Heading",
        background=header_bg,
        foreground=fg_color,
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        padding=5
    )
    # Quitar los bordes feos de la cabecera en Windows
    style.layout("Treeview.Heading", [
        ('Treeview.heading', {'sticky': 'nswe'})
    ])
    style.map("Treeview.Heading",
        background=[('active', bg_color)]
    )

    # --- Estilo para el DateEntry de ttkbootstrap ---
    # Esto hará que el calendario emergente también se vea oscuro
    style.configure('TEntry', fieldbackground=field_bg, foreground=fg_color, borderwidth=1, insertcolor=fg_color)
    style.configure('TButton', background=header_bg, foreground=fg_color, borderwidth=0)
    style.map('TButton', background=[('active', selected_bg)])
    style.configure('Toolbutton', background=bg_color, foreground=fg_color, padding=5)
    style.map('Toolbutton', background=[('active', selected_bg)])