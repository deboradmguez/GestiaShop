import customtkinter
import sys

class CTkNotification(customtkinter.CTkToplevel):
    def __init__(self,
                 master,
                 message,
                 icon,
                 duration=3000,
                 sound=False,
                 position="top-right",
                 fg_color=None,
                 text_color=None):

        super().__init__()

        self.master = master
        self.message_text = message
        self.duration = duration
        self.sound = sound
        self.icon = icon
        
        self.position = position

        self.lift()
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=1, fg_color=fg_color)
        self.main_frame.pack(expand=True, fill="both")

        inner_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        inner_frame.pack(padx=12, pady=8, expand=True, fill="both")
        inner_frame.grid_columnconfigure(1, weight=1)

        self.icon_label = customtkinter.CTkLabel(inner_frame, text=icon, font=("Segoe UI", 14))
        self.icon_label.grid(row=0, column=0, padx=(0, 10), sticky="ns")
        
        self.message_label = customtkinter.CTkLabel(inner_frame, 
                                                    text=message, 
                                                    wraplength=250, 
                                                    justify="left",
                                                    text_color=text_color)
        self.message_label.grid(row=0, column=1, sticky="nsew")
        
        self._set_geometry()

        if sound:
            self.bell()
            
        self.after(duration, self.destroy)

    def _set_geometry(self):
        self.update_idletasks() 
        
        width = 300
        height = self.main_frame.winfo_reqheight()
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = 0
        y = 0

        if "right" in self.position:
            x = screen_width - width - 20
        elif "left" in self.position:
            x = 20
        else: # center
            x = int((screen_width / 2) - (width / 2))

        if "bottom" in self.position:
            y = screen_height - height - 40
        else: # top
            y = 40
        
        self.geometry(f"{width}x{height}+{x}+{y}")