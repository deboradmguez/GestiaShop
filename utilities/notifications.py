def mostrar_mensaje_exito(label_widget, texto):
    """Muestra una notificación de éxito en la etiqueta proporcionada."""
    # CAMBIO: Usamos una tupla para el color del texto (claro, oscuro)
    label_widget.configure(text=f"✅ {texto}", text_color=("black", "white"), fg_color="#28a745")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())

def mostrar_mensaje_alerta(label_widget, texto):
    """Muestra una notificación de alerta en la etiqueta proporcionada."""
    # Esta ya estaba bien, pero la dejamos para consistencia.
    label_widget.configure(text=f"⚠️ {texto}", text_color="black", fg_color="#ffc107")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())

def mostrar_mensaje_error(label_widget, texto):
    """Muestra una notificación de error en la etiqueta proporcionada."""
    # CAMBIO: Usamos una tupla para el color del texto (claro, oscuro)
    label_widget.configure(text=f"❌ {texto}", text_color=("white", "white"), fg_color="#dc3545")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())