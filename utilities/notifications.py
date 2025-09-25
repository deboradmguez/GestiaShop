def mostrar_mensaje_exito(label_widget, texto):
    """Muestra una notificación de éxito en la etiqueta proporcionada."""
    label_widget.config(text=f"✅ {texto}", foreground="white", background="#28a745")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())

def mostrar_mensaje_alerta(label_widget, texto):
    """Muestra una notificación de alerta en la etiqueta proporcionada."""
    label_widget.config(text=f"⚠️ {texto}", foreground="black", background="#ffc107")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())

def mostrar_mensaje_error(label_widget, texto):
    """Muestra una notificación de error en la etiqueta proporcionada."""
    label_widget.config(text=f"❌ {texto}", foreground="white", background="#dc3545")
    label_widget.place(relx=0.5, rely=0.1, anchor="center")
    label_widget.lift()
    label_widget.after(3000, lambda: label_widget.place_forget())
