import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from utilities import helpers

class DateEntry(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.date_string = tk.StringVar()
        self.configure(fg_color="transparent")

        self.entry = ctk.CTkEntry(self, textvariable=self.date_string, state="readonly", width=120)
        self.entry.pack(side="left")

        self.button = ctk.CTkButton(self, text="📅", width=30, command=self._open_calendar)
        self.button.pack(side="left", padx=(5,0))

        self._top_level_calendar = None

    def _open_calendar(self):
        if self._top_level_calendar and self._top_level_calendar.winfo_exists():
            self._top_level_calendar.lift()
            return

        font_tuple = ("Segoe UI", 12)

        dark_style = {
            'background': '#2B2B2B', 'foreground': 'white',
            'selectbackground': '#1F538D', 'selectforeground': 'white',
            'normalbackground': '#2B2B2B', 'normalforeground': 'white',
            'weekendbackground': '#2B2B2B', 'weekendforeground': 'cyan',
            'othermonthforeground': 'gray40', 'othermonthbackground': '#2B2B2B',
            'headerbackground': '#2B2B2B', 'headerforeground': 'white',
            'disableddaybackground': '#2B2B2B', 'disableddayforeground': 'gray40',
            'borderwidth': 0,
            'font': font_tuple
        }
        
        light_style = {
            'background': '#FFFFFF', 'foreground': 'black',
            'selectbackground': '#0078D4', 'selectforeground': 'white',
            'normalbackground': '#FFFFFF', 'normalforeground': 'black',
            'weekendbackground': '#FFFFFF', 'weekendforeground': 'blue',
            'othermonthforeground': 'gray70', 'othermonthbackground': '#FFFFFF',
            'headerbackground': '#F0F0F0', 'headerforeground': 'black',
            'disableddaybackground': '#FFFFFF', 'disableddayforeground': 'gray70',
            'borderwidth': 0,
            'font': font_tuple
        }
        
        style_args = dark_style if ctk.get_appearance_mode() == "Dark" else light_style

        self._top_level_calendar = ctk.CTkToplevel(self)
        self._top_level_calendar.title("Seleccionar Fecha")
        self._top_level_calendar.transient(self)
        self._top_level_calendar.grab_set()

        try:
            current_date = datetime.strptime(self.date_string.get(), "%d/%m/%Y")
        except ValueError:
            current_date = datetime.now()
        
        cal = Calendar(self._top_level_calendar, selectmode='day',
                       year=current_date.year, month=current_date.month, day=current_date.day,
                       date_pattern='dd/mm/y', 
                       showweeknumbers=False,
                       **style_args)
        cal.pack(padx=10, pady=10)

        def on_select():
            self.date_string.set(cal.get_date())
            self._top_level_calendar.destroy()

        ok_button = ctk.CTkButton(self._top_level_calendar, text="Seleccionar", command=on_select)
        ok_button.pack(pady=10)

        
        helpers.centrar_ventana(self._top_level_calendar, self.winfo_toplevel())

    def get(self):
        return self.date_string.get()

    def set(self, date_string):
        self.date_string.set(date_string)
        
    def insert(self, index, date_string):
        self.date_string.set(date_string)