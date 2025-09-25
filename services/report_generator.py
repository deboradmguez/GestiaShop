import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from utilities.helpers import obtener_ruta_guardado

def generar_reporte_cierre_caja(datos_cierre, historial_ventas, resumen_ventas, fecha_reporte):
    
    try:
        # Obtenemos la ruta segura para guardar el reporte
        ruta_carpeta = obtener_ruta_guardado("Cierres_de_Caja")
        fecha_db = datetime.strptime(fecha_reporte, "%d/%m/%Y").strftime("%Y-%m-%d")
        nombre_archivo = f"Cierre_Caja_{fecha_db}.pdf"
        ruta_pdf = os.path.join(ruta_carpeta, nombre_archivo)

        doc = SimpleDocTemplate(ruta_pdf, pagesize=A4, topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()
        
        # --- Estilos Personalizados ---
        styles.add(ParagraphStyle(name='Anulada', parent=styles['Normal'], textColor=colors.red))
        styles.add(ParagraphStyle(name='Tachado', parent=styles['Normal'], textColor=colors.grey, strike=1))

        # --- Contenido del PDF ---
        story.append(Paragraph(f"Cierre de Caja - {fecha_reporte}", styles['Title']))
        story.append(Paragraph(f"<i>Caja gestionada por: {datos_cierre.get('usuario', 'N/A')}</i>", styles['Normal']))
        story.append(Spacer(1, 24))

        # Tabla de Resumen de Caja
        total_efectivo = sum(t for m, t in resumen_ventas if m == "Efectivo")
        total_esperado = datos_cierre.get('fondo_inicial', 0.0) + total_efectivo
        
        data_cierre = [
            ["Fondo Inicial:", f"${datos_cierre.get('fondo_inicial', 0.0):,.2f}"],
            ["Total Esperado en Caja:", f"${total_esperado:,.2f}"],
            ["Monto Contado Final:", f"${datos_cierre.get('contado_final', 0.0):,.2f}"],
            ["Diferencia:", f"${datos_cierre.get('diferencia', 0.0):,.2f}"]
        ]
        table_cierre = Table(data_cierre, colWidths=[200, 150])
        story.append(table_cierre)
        story.append(Spacer(1, 24))

        # Tabla de Resumen de Ventas
        total_transferencia = sum(t for m, t in resumen_ventas if m == "Transferencia")
        data_ventas = [
            ["Ventas en Efectivo:", f"${total_efectivo:,.2f}"],
            ["Ventas por Transferencia:", f"${total_transferencia:,.2f}"],
            ["TOTAL GENERAL VENDIDO:", f"${total_efectivo + total_transferencia:,.2f}"]
        ]
        table_ventas = Table(data_ventas, colWidths=[200, 150])
        story.append(table_ventas)
        story.append(Spacer(1, 24))

        # Detalle de Transacciones
        if historial_ventas:
            story.append(Paragraph("Detalle de Transacciones", styles['h2']))
            data_historial = [["Ticket", "Hora", "Descripción", "Cantidad", "Total", "Estado"]]
            
            for venta in historial_ventas:
                # id_t, fecha_h, nom, cant, prec, p_ef, p_tr, total_f, est, tick
                _, fecha_hora, desc, cant, _, _, _, total, estado, ticket = venta
                hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
                
                if estado == 'Anulada':
                    fila = [
                        Paragraph(f"<s>#{ticket}</s>", styles['Tachado']),
                        Paragraph(f"<s>{hora}</s>", styles['Tachado']),
                        Paragraph(f"<s>{desc}</s>", styles['Tachado']),
                        Paragraph(f"<s>{cant}</s>", styles['Tachado']),
                        Paragraph(f"<s>${total:,.2f}</s>", styles['Tachado']),
                        Paragraph("ANULADA", styles['Anulada'])
                    ]
                else:
                    fila = [f"#{ticket}", hora, desc, cant, f"${total:,.2f}", "Completada"]
                
                data_historial.append(fila)

            table_historial = Table(data_historial)
            story.append(table_historial)

        doc.build(story)
        os.startfile(ruta_carpeta) # Abre la carpeta donde se guardó el PDF
        return True, None
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return False, str(e)
def generar_reporte_estadisticas(fecha_inicio, fecha_fin, resumen, top_productos):

    try:
        ruta_carpeta = obtener_ruta_guardado("Reportes_Estadisticos")
        nombre_archivo = f"Reporte_Estadisticas_{fecha_inicio.replace('/', '- C')}_al_{fecha_fin.replace('/', '-')}.pdf"
        ruta_pdf = os.path.join(ruta_carpeta, nombre_archivo)

        doc = SimpleDocTemplate(ruta_pdf, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # --- Contenido del PDF ---
        story.append(Paragraph("Reporte de Estadísticas", styles['Title']))
        story.append(Paragraph(f"Período: {fecha_inicio} al {fecha_fin}", styles['Normal']))
        story.append(Spacer(1, 24))

        # Tabla de Resumen de Ingresos
        story.append(Paragraph("Resumen de Ingresos", styles['h2']))
        data_resumen = [
            ["Facturación Total:", f"${resumen.get('total', 0.0):,.2f}"],
            ["Total en Efectivo:", f"${resumen.get('efectivo', 0.0):,.2f}"],
            ["Total por Transferencia:", f"${resumen.get('transferencia', 0.0):,.2f}"]
        ]
        table_resumen = Table(data_resumen, colWidths=[200, 150])
        story.append(table_resumen)
        story.append(Spacer(1, 24))

        # Tabla de Top Productos
        story.append(Paragraph("Productos Más Vendidos", styles['h2']))
        data_top = [["Producto", "Unidades Vendidas"]]
        for producto, cantidad in top_productos:
            data_top.append([producto, f"{cantidad} unidades"])
        
        table_top = Table(data_top)
        table_top.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.grey)
        ]))
        story.append(table_top)
        
        doc.build(story)
        os.startfile(ruta_carpeta) # Abre la carpeta donde se guardó el PDF
        return True, None
    except Exception as e:
        print(f"Error al generar PDF de estadísticas: {e}")
        return False, str(e)