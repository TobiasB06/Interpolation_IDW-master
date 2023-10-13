import pandas as pd
import openpyxl as pxl

hola = pd.read_excel("Archivo_angularesP1.xlsx", sheet_name="P2-10000", header=6)
# Obtiene el número de filas y columnas
num_filas, num_columnas = hola.shape

print(f"El archivo Excel tiene {num_filas} filas de información.")