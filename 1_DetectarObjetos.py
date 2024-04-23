import pymongo
import os
import imageai
from imageai.Detection import ObjectDetection

# Ruta donde se encuentran los modelos de IA
rutaModelosIA = "/mnt/local/datos/Desarrollo/ModelosIA"

# Funcion para leer la base de datos
def leeBaseDatos():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["inventario"]
    coleccion = db["archivos"]    
    return coleccion.find()

# Funcion para actualizar la base de datos
def actualizarBaseDatos(id, objetosDetectados):
    try:
        client = pymongo.MongoClient("localhost", 27017)
        db = client["inventario"]
        coleccion = db["archivos"]
        coleccion.update_one({"_id": id}, {"$set": {"objetos": objetosDetectados}})
    except Exception as e:
        print("Error al actualizar la base de datos: " + str(e))

# Funcion para detectar objetos en una imagen
def detectarObjetos(imagen):
    salida = []
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(rutaModelosIA , "yolov3.pt"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=imagen, minimum_percentage_probability=30)
    numeroObjetos = len(detections)
    contador = 0
    objeto = []
    for eachObject in detections:        
        contador += 1    
        nombre = eachObject["name"]
        probabilidad = eachObject["percentage_probability"]
        coordenadas = eachObject["box_points"]
        x1, y1, x2, y2 = coordenadas
        objeto = [contador, nombre, probabilidad, coordenadas]        
        salida.append(objeto)
        objeto = []              
    return salida

# Funcion principal
if __name__ == '__main__':
    for documento in leeBaseDatos():
        if documento["extensioArchivo"] == "jpg":            
           objetosDetectados = detectarObjetos(documento["ruta_archivo"])
           if len(objetosDetectados) > 0:
               print("Se detectaron objetos en el archivo: " + documento["nombre_archivo"])           
               for objeto in objetosDetectados:
                   print(objeto)
                   