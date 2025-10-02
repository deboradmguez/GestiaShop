import customtkinter
import sys

class CTkNotification(customtkinter.CTkToplevel):
    def __init__(self,
                 master,
                 message,
                 icon,
                 duration=3000,
                 sound=False,
                 position="top-right", # Cambiamos la posición por defecto
                 fg_color=None,
                 text_color=None):

        super().__init__()

        self.master = master
        self.message_text = message
        self.duration = duration
        self.sound = sound
        self.position = position
        self.icon = icon

        self.lift()
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=1, fg_color=fg_color)
        self.main_frame.pack(expand=True, fill="both")

        inner_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        inner_frame.pack(padx=15, pady=10, expand=True, fill="both")
        inner_frame.grid_columnconfigure(1, weight=1)

        self.icon_label = customtkinter.CTkLabel(inner_frame, text=self.icon, font=("Segoe UI", 20))
        self.icon_label.grid(row=0, column=0, padx=(0, 10), sticky="ns")

        self.message_label = customtkinter.CTkLabel(inner_frame, 
                                                    text=self.message_text, 
                                                    wraplength=280, 
                                                    justify="left",
                                                    text_color=text_color)
        self.message_label.grid(row=0, column=1, sticky="nsew")
        
        self._set_geometry()

        if self.sound:
            self.bell()
            
        self.after(self.duration, self.destroy)

    def _set_geometry(self):
        self.update_idletasks() 
        
        width = 350
        height = self.main_frame.winfo_reqheight()
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # --- INICIO DE LA MODIFICACIÓN ---
        # Lógica de posicionamiento horizontal
        if "right" in self.position:
            x = screen_width - width - 20
        elif "left" in self.position:
            x = 20
        elif "center" in self.position:
            x = int((screen_width / 2) - (width / 2))
        else: # Por defecto, a la derecha
            x = screen_width - width - 20

        # Lógica de posicionamiento vertical
        if "bottom" in self.position:
            y = screen_height - height - 50
        elif "top" in self.position:
            y = 50
        elif "center" in self.position:
            y = int((screen_height / 2) - (height / 2))
        else: # Por defecto, arriba
            y = 50
        
        # Lógica para apilar notificaciones
        active_notifications = [
            w for w in self.master.winfo_children() 
            if isinstance(w, CTkNotification) and w.winfo_exists()
        ]
        
        if "bottom" in self.position:
            # Apilar hacia arriba
            y -= sum(notif.winfo_height() + 10 for notif in active_notifications)
        elif "top" in self.position:
            # Apilar hacia abajo
            y += sum(notif.winfo_height() + 10 for notif in active_notifications)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        # --- FIN DE LA MODIFICACIÓN ---