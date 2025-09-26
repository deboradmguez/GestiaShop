import tkinter as tk
from tkinter import ttk
from utilities import helpers
class ConfirmacionDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result = False # El resultado por defecto es False (No)

        # --- Creación de la Interfaz ---
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=message, wraplength=300).pack(pady=(0, 20))

        frame_botones = ttk.Frame(frame)
        frame_botones.pack()

        btn_si = ttk.Button(
            frame_botones, text="Sí", style="success.TButton",
            command=self._on_si
        )
        btn_si.pack(side="left", padx=10)

        btn_no = ttk.Button(
            frame_botones, text="No", style="danger.TButton",
            command=self._on_no
        )
        btn_no.pack(side="left", padx=10)
        
        # Centrar la ventana
        #self.update_idletasks()
        helpers.centrar_ventana(self, parent)


    def _on_si(self):
        self.result = True
        self.destroy()

    def _on_no(self):
        self.result = False
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window(self)
        return self.result
    
# ui/utilities/dialogs.py

class PinDialog(tk.Toplevel):
    # Modificamos el constructor para que acepte el PIN
    def __init__(self, parent, pin_correcto):
        super().__init__(parent)
        self.title("Acceso Restringido")
        self.transient(parent)
        self.grab_set()
        self.result = False

        self.PIN_CORRECTO = str(pin_correcto)
        helpers.centrar_ventana(self, parent)

    def _on_ok(self, event=None):
        if self.entry_pin.get() == self.PIN_CORRECTO:
            self.result = True
            self.destroy()
        else:
            # Puedes usar las notificaciones de la app principal si tienes una referencia,
            # o un simple messagebox para el diálogo.
            from tkinter import messagebox
            messagebox.showerror("Error", "PIN incorrecto.", parent=self)
            self.result = False
            self.destroy()
            
    def _on_cancel(self, event=None):
        self.result = False
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window(self)
        return self.result
