import rasterio
import numpy as np
import os
ruta_archivo_tif = "GEBCO-UTM.tif"
with rasterio.open(ruta_archivo_tif) as src:
    metadatos = src.meta
    datos_raster = src.read(1)
transformacion = metadatos['transform']
muestreo = 10
filas, columnas = datos_raster.shape
coordenadas_X = []
coordenadas_Y = []
coordenadas_Z = []
for i in range(0, filas, muestreo):
    for j in range(0, columnas, muestreo):
        valor_pixel = datos_raster[i, j]
        x, y = rasterio.transform.xy(transformacion, i, j)
        coordenadas_X.append(x)
        coordenadas_Y.append(y)
        coordenadas_Z.append(valor_pixel)
datos_xyz = np.column_stack((coordenadas_X, coordenadas_Y, coordenadas_Z))
ruta_archivo_xyz = "datos_convertidos.xyz"
np.savetxt(ruta_archivo_xyz, datos_xyz, fmt='%.9f', delimiter=',')


