import customtkinter as ctk
from utilities import helpers
from tkinter import messagebox

class ConfirmacionDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result = False

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text=message, wraplength=300).pack(pady=(0, 20))

        frame_botones = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botones.pack()

        btn_si = ctk.CTkButton(
            frame_botones, text="Sí", command=self._on_si,
            fg_color="#28a745", hover_color="#218838" # Color "success"
        )
        btn_si.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            frame_botones, text="No", command=self._on_no,
            fg_color="#D32F2F", hover_color="#B71C1C" # Color "danger"
        )
        btn_no.pack(side="left", padx=10)
        
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
    
class PinDialog(ctk.CTkToplevel):
    def __init__(self, parent, pin_correcto):
        super().__init__(parent)
        self.title("Acceso Restringido")
        self.result = False

        self.PIN_CORRECTO = str(pin_correcto)
        
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Por favor, ingrese el PIN de administrador:").pack(pady=(0, 10))
        
        self.entry_pin = ctk.CTkEntry(frame, show="*", justify="center", font=("Segoe UI", 12))
        self.entry_pin.pack(pady=5)

        frame_botones = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        btn_ok = ctk.CTkButton(frame_botones, text="OK", command=self._on_ok)
        btn_ok.pack(side="left", padx=10)

        btn_cancel = ctk.CTkButton(frame_botones, text="Cancelar", command=self._on_cancel)
        btn_cancel.pack(side="left", padx=10)

        self.bind("<Return>", self._on_ok)
        self.bind("<Escape>", self._on_cancel)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        helpers.configurar_dialogo(self, parent, self.entry_pin)

    def _on_ok(self, event=None):
        if self.entry_pin.get() == self.PIN_CORRECTO:
            self.result = True
            self.destroy()
        else:
            messagebox.showerror("Error", "PIN incorrecto.", parent=self)
            self.result = False
            
    def _on_cancel(self, event=None):
        self.result = None
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window(self)
        return self.result