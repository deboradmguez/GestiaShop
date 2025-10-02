import customtkinter as ctk
from utilities import helpers

class PinDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, text):
        super().__init__(parent)
        
        self.title(title)
        self._text = text
        self._input = None 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._frame = ctk.CTkFrame(self)
        self._frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self._frame, text=self._text).pack(padx=10, pady=(10, 5), fill="x")
        
        self._entry = ctk.CTkEntry(self._frame, show="*")
        self._entry.pack(padx=10, pady=5, fill="x")
        
        button_frame = ctk.CTkFrame(self._frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self._ok_button = ctk.CTkButton(button_frame, text="Aceptar", command=self._ok_event)
        self._ok_button.pack(side="left", padx=(0, 5))
        
        self._cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self._cancel_event)
        self._cancel_button.pack(side="left", padx=5)

        self.bind("<Return>", self._ok_event)
        self.bind("<Escape>", self._cancel_event)
        
        helpers.configurar_dialogo(self, parent, self._entry)

    def _ok_event(self, event=None):
        self._input = self._entry.get()
        self.grab_release()
        self.destroy()

    def _cancel_event(self, event=None):
        self._input = None
        self.grab_release()
        self.destroy()

    def get_input(self):
        """Muestra la ventana y espera hasta que se cierre."""
        self.master.wait_window(self)
        return self._input