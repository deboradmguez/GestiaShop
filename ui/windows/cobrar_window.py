import customtkinter as ctk
from utilities import helpers
import tkinter as tk

class CobrarWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, total_a_cobrar):
        super().__init__(parent)
        self.controller = controller
        self.total_a_cobrar = total_a_cobrar

        self.title("💰 Cobrar Venta")
        self.transient(parent)
        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.grab_set()

        self.metodo_pago = tk.StringVar(value="Efectivo")
        self.monto_efectivo_entry = None
        self.monto_transferencia_entry = None
        self.entry_referencia = None
        
        self.focus_after_id = None

        self._crear_widgets()
        self._configurar_bindings()
        self._actualizar_inputs_metodo()
        helpers.centrar_ventana(self, parent)


    def destroy(self):
        if self.focus_after_id:
            self.after_cancel(self.focus_after_id)
            self.focus_after_id = None
        super().destroy()

    def _crear_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        frame_total = ctk.CTkFrame(main_frame, border_width=1)
        frame_total.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_total, text="Total a Cobrar", font=ctk.CTkFont(weight="bold")).pack()
        ctk.CTkLabel(frame_total, text=f"${self.total_a_cobrar:,.2f}", font=("Segoe UI", 16, "bold")).pack(pady=(0,5))

        frame_metodos = ctk.CTkFrame(main_frame)
        frame_metodos.pack(pady=(0, 5))
        self.opciones_metodo = ["Efectivo", "Transferencia", "Mixto"]
        for op in self.opciones_metodo:
            radio = ctk.CTkRadioButton(
                frame_metodos, text=op, variable=self.metodo_pago, value=op,
                command=self._actualizar_inputs_metodo
            )
            radio.pack(side="left", padx=10, pady=5)

        self.frame_inputs = ctk.CTkFrame(main_frame, border_width=1)
        self.frame_inputs.pack(padx=10, pady=5, fill="both", expand=True, ipady=10)
        ctk.CTkLabel(self.frame_inputs, text="Detalles de Pago", font=ctk.CTkFont(weight="bold")).pack(pady=(0,10))


        frame_finalizar = ctk.CTkFrame(main_frame)
        frame_finalizar.pack(pady=20)
        self.btn_finalizar = ctk.CTkButton(
            frame_finalizar, text="✅ Finalizar Venta",
            command=self._on_finalizar_venta,
            fg_color="#28a745", hover_color="#218838"
        )
        self.btn_finalizar.pack(ipadx=10, ipady=5)

    def _configurar_bindings(self):
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self._on_finalizar_venta())
        self.bind("<Left>", self._navegar_metodos_pago)
        self.bind("<Right>", self._navegar_metodos_pago)

    def _navegar_metodos_pago(self, event):
        indice_actual = self.opciones_metodo.index(self.metodo_pago.get())
        if event.keysym == "Right":
            nuevo_indice = (indice_actual + 1) % len(self.opciones_metodo)
        else: # Left
            nuevo_indice = (indice_actual - 1 + len(self.opciones_metodo)) % len(self.opciones_metodo)
        self.metodo_pago.set(self.opciones_metodo[nuevo_indice])
        self._actualizar_inputs_metodo()

    def _safe_focus(self, widget):
        try:
            if widget and widget.winfo_exists():
                widget.focus()
        except tk.TclError:
            pass
            
    def _actualizar_inputs_metodo(self, *args):
        if self.focus_after_id:
            self.after_cancel(self.focus_after_id)
            self.focus_after_id = None

        for widget in self.frame_inputs.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Detalles" in widget.cget("text"):
                continue
            widget.destroy()

        metodo = self.metodo_pago.get()

        if metodo == "Efectivo":
            ctk.CTkLabel(self.frame_inputs, text="Monto Recibido:").pack(anchor="w", padx=10)
            self.monto_efectivo_entry = ctk.CTkEntry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_efectivo_entry.pack(fill="x", pady=(0, 5), padx=10)
            self.monto_efectivo_entry.insert(0, f"{self.total_a_cobrar:.2f}")
            self.focus_after_id = self.after(50, lambda: self._safe_focus(self.monto_efectivo_entry))
            self.label_vuelto = ctk.CTkLabel(self.frame_inputs, text="Vuelto: $0.00", font=("Segoe UI", 12, "bold"))
            self.label_vuelto.pack(fill="x", pady=5, padx=10)
            self.monto_efectivo_entry.bind("<KeyRelease>", self._calcular_vuelto)
            self._calcular_vuelto()

        elif metodo == "Transferencia":
            ctk.CTkLabel(self.frame_inputs, text="Referencia (opcional):").pack(anchor="w", padx=10)
            self.entry_referencia = ctk.CTkEntry(self.frame_inputs, font=("Segoe UI", 16))
            self.entry_referencia.pack(fill="x", padx=10)
            self.focus_after_id = self.after(50, lambda: self._safe_focus(self.entry_referencia))
            
        elif metodo == "Mixto":
            ctk.CTkLabel(self.frame_inputs, text="Monto Efectivo:").pack(anchor="w", padx=10)
            self.monto_efectivo_entry = ctk.CTkEntry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_efectivo_entry.pack(fill="x", padx=10)

            ctk.CTkLabel(self.frame_inputs, text="Monto Transferencia:").pack(anchor="w", pady=(5,0), padx=10)
            self.monto_transferencia_entry = ctk.CTkEntry(self.frame_inputs, font=("Segoe UI", 16))
            self.monto_transferencia_entry.pack(fill="x", padx=10)
            self.focus_after_id = self.after(50, lambda: self._safe_focus(self.monto_efectivo_entry))
            self.monto_efectivo_entry.bind("<KeyRelease>", lambda e: self._calcular_monto_restante(self.monto_efectivo_entry, self.monto_transferencia_entry))
            self.monto_transferencia_entry.bind("<KeyRelease>", lambda e: self._calcular_monto_restante(self.monto_transferencia_entry, self.monto_efectivo_entry))

    def _calcular_vuelto(self, event=None):
        try:
            monto_recibido = float(self.monto_efectivo_entry.get())
            vuelto = monto_recibido - self.total_a_cobrar
            if vuelto >= 0:
                self.label_vuelto.configure(text=f"Vuelto: ${vuelto:,.2f}", text_color="white")
            else:
                self.label_vuelto.configure(text=f"Falta: ${abs(vuelto):,.2f}", text_color="red")
        except (ValueError, TypeError):
            self.label_vuelto.configure(text="Monto inválido", text_color="red")

    def _calcular_monto_restante(self, entry_activa, entry_pasiva):
        try:
            monto_ingresado = float(entry_activa.get() or 0)
            monto_restante = self.total_a_cobrar - monto_ingresado
            
            entry_pasiva.unbind("<KeyRelease>")
            entry_pasiva.delete(0, tk.END)

            if monto_restante > 0:
                entry_pasiva.insert(0, f"{monto_restante:.2f}")
            else:
                entry_pasiva.insert(0, "0.00")
            entry_pasiva.bind("<KeyRelease>", lambda e: self._calcular_monto_restante(entry_pasiva, entry_activa))

        except (ValueError, TypeError):
            entry_pasiva.delete(0, tk.END)

    def _on_finalizar_venta(self):
        payment_data = {"metodo": self.metodo_pago.get()}
        try:
            if payment_data["metodo"] == "Efectivo":
                pago_recibido = float(self.monto_efectivo_entry.get())
                if pago_recibido < self.total_a_cobrar:
                    self.controller.notificar_error("El pago es insuficiente.")
                    return
                payment_data["pago_efectivo"] = self.total_a_cobrar

            elif payment_data["metodo"] == "Transferencia":
                payment_data["pago_transferencia"] = self.total_a_cobrar
                payment_data["referencia"] = self.entry_referencia.get() if self.entry_referencia else ""

            elif payment_data["metodo"] == "Mixto":
                pago_efectivo = float(self.monto_efectivo_entry.get() or 0)
                pago_transferencia = float(self.monto_transferencia_entry.get() or 0)
                if (pago_efectivo + pago_transferencia) < self.total_a_cobrar:
                    self.controller.notificar_error("El pago mixto es insuficiente.")
                    return
                payment_data["pago_efectivo"] = pago_efectivo
                payment_data["pago_transferencia"] = pago_transferencia
                
            venta_exitosa = self.controller.finalizar_venta(payment_data)
            
            if venta_exitosa:
                self.withdraw()
                self.after(100, self.destroy)

        except (ValueError, TypeError):
            self.controller.notificar_error("Monto inválido.")