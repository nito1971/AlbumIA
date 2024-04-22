import os

ruta = "/mnt/local/datos"

for directorio, subdirectorio, archivos in os.walk(ruta):
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio, archivo)
        print(ruta_archivo)