import tkinter as tk
from tkinter import ttk
from utilities import helpers
class CobrarWindow(tk.Toplevel):
    """
    Clase que representa la ventana emergente para el proceso de cobro.
    """
    def __init__(self, parent, controller, total_a_cobrar):
        super().__init__(parent)
        self.controller = controller
        self.total_a_cobrar = total_a_cobrar

        # --- Configuración de la ventana ---
        self.title("💰 Cobrar Venta")
        self.transient(parent)
        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.grab_set()

        # --- Variables de estado internas ---
        self.metodo_pago = tk.StringVar(value="Efectivo")
        self.monto_efectivo_entry = None
        self.monto_transferencia_entry = None
        self.entry_referencia = None

        # --- Creación de la interfaz ---
        self._crear_widgets()
        self._configurar_bindings()
        self._actualizar_inputs_metodo()
        helpers.centrar_ventana(self, parent)
        


    def _crear_widgets(self):
        """Crea la estructura de widgets de la ventana."""
        # Frame del total
        frame_total = ttk.LabelFrame(self, text="Total a Cobrar", padding=10)
        frame_total.pack(padx=10, pady=10, fill="x")
        ttk.Label(frame_total, text=f"${self.total_a_cobrar:,.2f}", font=("Segoe UI", 16, "bold")).pack()

        # Frame para los métodos de pago (Radios)
        frame_metodos = ttk.Frame(self)
        frame_metodos.pack(pady=(0, 5))
        opciones_metodo = ["Efectivo", "Transferencia", "Mixto"]
        for op in opciones_metodo:
            radio = ttk.Radiobutton(
                frame_metodos, text=op, variable=self.metodo_pago, value=op,
                command=self._actualizar_inputs_metodo
            )
            radio.pack(side="left", padx=5)

        # Frame dinámico para las entradas de texto
        self.frame_inputs = ttk.LabelFrame(self, text="Detalles de Pago", padding=10)
        self.frame_inputs.pack(padx=10, pady=5, fill="both", expand=True)

        # Frame para el botón de finalizar
        frame_finalizar = ttk.Frame(self)
        frame_finalizar.pack(pady=20)
        self.btn_finalizar = ttk.Button(
            frame_finalizar, text="✅ Finalizar Venta", style="success.TButton",
            command=self._on_finalizar_venta
        )
        self.btn_finalizar.pack(ipadx=10, ipady=5)
    
    def _configurar_bindings(self):
        """Configura los atajos de teclado para la ventana."""
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self._on_finalizar_venta())

    def _actualizar_inputs_metodo(self, *args):
        """Limpia y redibuja las entradas de texto según el método de pago."""
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        metodo = self.metodo_pago.get()

        if metodo == "Efectivo":
            ttk.Label(self.frame_inputs, text="Monto Recibido:").pack(anchor="w")
            self.monto_efectivo_entry = ttk.Entry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_efectivo_entry.pack(fill="x", pady=(0, 10))
            self.monto_efectivo_entry.focus_set()
            self.monto_efectivo_entry.insert(0, f"{self.total_a_cobrar:.2f}")

        elif metodo == "Transferencia":
            ttk.Label(self.frame_inputs, text="Referencia (opcional):").pack(anchor="w")
            self.entry_referencia = ttk.Entry(self.frame_inputs, font=("Segoe UI", 16))
            self.entry_referencia.pack(fill="x")
            self.entry_referencia.focus_set()

        elif metodo == "Mixto":
            ttk.Label(self.frame_inputs, text="Monto Efectivo:").pack(anchor="w")
            self.monto_efectivo_entry = ttk.Entry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_efectivo_entry.pack(fill="x")
            self.monto_efectivo_entry.focus_set()

            ttk.Label(self.frame_inputs, text="Monto Transferencia:").pack(anchor="w", pady=(5,0))
            self.monto_transferencia_entry = ttk.Entry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_transferencia_entry.pack(fill="x")

    def _on_finalizar_venta(self):
        """
        Recolecta los datos de la UI y los envía al controlador para ser procesados.
        """
        payment_data = {"metodo": self.metodo_pago.get()}
        
        try:
            if payment_data["metodo"] == "Efectivo":
                pago_recibido = float(self.monto_efectivo_entry.get())
                if pago_recibido < self.total_a_cobrar:
                    # self.controller.mostrar_mensaje_error(...)
                    print("El pago es insuficiente.")
                    return
                payment_data["pago_efectivo"] = self.total_a_cobrar

            elif payment_data["metodo"] == "Transferencia":
                payment_data["pago_transferencia"] = self.total_a_cobrar
                payment_data["referencia"] = self.entry_referencia.get() if self.entry_referencia else ""

            elif payment_data["metodo"] == "Mixto":
                pago_efectivo = float(self.monto_efectivo_entry.get() or 0)
                pago_transferencia = float(self.monto_transferencia_entry.get() or 0)
                if (pago_efectivo + pago_transferencia) < self.total_a_cobrar:
                    # self.controller.mostrar_mensaje_error(...)
                    print("El pago mixto es insuficiente.")
                    return
                payment_data["pago_efectivo"] = pago_efectivo
                payment_data["pago_transferencia"] = pago_transferencia

            # Llama al método del controlador para procesar la venta
            venta_exitosa = self.controller.finalizar_venta(payment_data)
            
            # Si la venta fue exitosa, la ventana se cierra.
            if venta_exitosa:
                self.destroy()

        except (ValueError, TypeError):
            # self.controller.mostrar_mensaje_error(...)
            print("Monto inválido.")
