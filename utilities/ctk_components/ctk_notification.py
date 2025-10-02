import customtkinter

class CTkNotification(customtkinter.CTkToplevel):
    def __init__(self,
                 master,
                 title,
                 message,
                 duration=3000,
                 icon=None,
                 sound=False,
                 position="bottom-right"):

        super().__init__()

        self.master = master
        self.title_text = title
        self.message_text = message
        self.duration = duration
        self.icon = icon
        self.sound = sound
        self.position = position

        self._set_geometry()

        self.lift()
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=1)
        self.main_frame.pack(expand=True, fill="both")

        self.title_label = customtkinter.CTkLabel(self.main_frame, text=self.title_text, font=customtkinter.CTkFont(weight="bold"))
        self.title_label.pack(padx=20, pady=(10, 5), anchor="w")

        self.message_label = customtkinter.CTkLabel(self.main_frame, text=self.message_text, wraplength=280, justify="left")
        self.message_label.pack(padx=20, pady=(0, 10), anchor="w")

        if self.sound:
            self.bell()
            
        self.after(self.duration, self.destroy)

    def _set_geometry(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = 350
        height = 100
        x = 0
        y = 0

        if "right" in self.position:
            x = screen_width - width - 20
        elif "left" in self.position:
            x = 20

        if "bottom" in self.position:
            y = screen_height - height - 50
        elif "top" in self.position:
            y = 50

        # Adjust for multiple notifications
        active_notifications = [w for w in self.master.winfo_children() if isinstance(w, CTkNotification)]
        y -= len(active_notifications) * (height + 10)
        
        self.geometry(f"{width}x{height}+{x}+{y}")