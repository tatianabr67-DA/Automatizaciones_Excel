"""
Herramienta de Automatización y Limpieza de Reportes de Nómina
------------------------------------------------------------
Descripción: Interfaz gráfica (Tkinter) desarrollada en Python para transformar
reportes crudos de nómina (Nominax) en datasets estructurados listos para análisis.
Autor: Denisse Tatiana Baltazar Romero
"""

import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Diccionario de negocio para asignar sucursales según departamento
MAPA_CIUDADES = {
    "ADMINISTRACION": "TIJUANA",
    "ALMACEN": "SAN QUINTIN",
    "CONTROL DE CALIDAD": "ZAMORA",
    "PRODUCCION": "ZAMORA"
}

def formatear_fecha_segura(valor):
    """
    Convierte cualquier dato de fecha a formato texto 'AAAA-MM-DD'.
    Retorna cadena vacía si el dato es nulo o no válido.
    """
    if pd.isna(valor) or str(valor).strip() == "":
        return ""
    dt = pd.to_datetime(valor, errors='coerce')
    if pd.isna(dt):
        return ""
    return dt.strftime('%Y-%m-%d')

def cargar_excel_defensivo(ruta):
    """
    Intenta leer archivos Excel antiguos (.xls) con motor 'xlrd'
    y recurre al comportamiento por defecto si es necesario.
    """
    try:
        return pd.read_excel(ruta, header=None, engine='xlrd')
    except Exception:
        return pd.read_excel(ruta, header=None)

def limpiar_empleados_departamento(ruta_entrada, ruta_salida):
    """
    Procesa el reporte crudo, mapea ciudades, filtra registros válidos
    y exporta un archivo limpio estructurado.
    """
    df_raw = cargar_excel_defensivo(ruta_entrada)
    
    filas_limpias = []
    dep_actual = None
    ciudad_actual = ""

    for idx, row in df_raw.iterrows():
        primer_valor = str(row[0]).strip() if pd.notna(row[0]) else ""
        tercer_valor = str(row[3]).strip() if pd.notna(row[3]) else ""
        
        # Identificar la sección del departamento
        if primer_valor.lower().startswith("departamento"):
            dep_actual = tercer_valor
            dep_key = re.sub(r'[^A-Z ]', '', dep_actual.upper())
            ciudad_actual = MAPA_CIUDADES.get(dep_key, "")
            continue
        
        num_emp = row[2]
        nombre_emp = str(row[4]).strip() if pd.notna(row[4]) else ""
        
        # Filtrar filas que correspondan a empleados válidos
        if pd.notna(num_emp) and str(num_emp).isdigit() and nombre_emp != "":
            puesto = row[7] if pd.notna(row[7]) else ""
            salario = row[13] if pd.notna(row[13]) else ""
            ingreso_raw = row[14] if pd.notna(row[14]) else ""
            
            ingreso_formateado = formatear_fecha_segura(ingreso_raw)
            
            filas_limpias.append({
                "Número": int(num_emp),
                "Departamento": dep_actual,
                "Nombre": nombre_emp,
                "Puesto": puesto,
                "Salario": salario,
                "Ingreso": ingreso_formateado,
                "Ciudad": ciudad_actual
            })

    df_resultado = pd.DataFrame(filas_limpias)
    df_resultado.to_excel(ruta_salida, index=False)
    return True

# --- INTERFAZ GRÁFICA (GUI) ---
def ejecutar_proceso():
    archivo_origen = entrada_ruta.get()
    if not archivo_origen or not os.path.exists(archivo_origen):
        messagebox.showerror("Error", "Por favor selecciona un archivo válido.")
        return
    
    directorio = os.path.dirname(archivo_origen)
    archivo_destino = os.path.join(directorio, "Empleados_por_Departamento_limpio.xlsx")
    
    try:
        limpiar_empleados_departamento(archivo_origen, archivo_destino)
        messagebox.showinfo("Éxito", f"¡Archivo generado exitosamente!\n\nUbicación:\n{archivo_destino}")
    except Exception as e:
        messagebox.showerror("Error al procesar", f"Detalle del error:\n{str(e)}")

def seleccionar_archivo():
    filename = filedialog.askopenfilename(
        title="Selecciona el archivo de Empleados por Departamento",
        filetypes=[("Archivos Excel", "*.xls *.xlsx")]
    )
    if filename:
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, filename)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Automatización de Nómina - Limpieza de Reportes")
ventana.geometry("550x180")

label = tk.Label(ventana, text="Selecciona el reporte crudo de Empleados por Departamento:", font=("Arial", 10))
label.pack(pady=10)

entrada_ruta = tk.Entry(ventana, width=60)
entrada_ruta.pack(pady=5)

btn_examinar = tk.Button(ventana, text="Buscar Archivo", command=seleccionar_archivo)
btn_examinar.pack(pady=5)

btn_procesar = tk.Button(ventana, text="Limpiar y Generar Archivo", command=ejecutar_proceso, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_procesar.pack(pady=10)

ventana.mainloop()