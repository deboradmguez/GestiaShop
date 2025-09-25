import tkinter as tk
from tkinter import ttk

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
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

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