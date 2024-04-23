import pymongo
import os
import imageai
from imageai.Detection import ObjectDetection

# Ruta donde se encuentran los modelos de IA
rutaModelosIA = "/mnt/local/datos/Desarrollo/ModelosIA"

# Lista de extensiones permitidas
extensionesValidas = ["jpg", "jpeg", "png"]

# Funcion para leer la base de datos
def leeBaseDatos():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["inventario"]
    coleccion = db["archivos"]    
    return coleccion.find()

# Funcion para actualizar la base de datos
def actualizarBaseDatos(id, objetosDetectados, contador):
    try:
        client = pymongo.MongoClient("localhost", 27017)
        db = client["inventario"]
        coleccion = db["archivos"]
        coleccion.update_one({"_id": id}, {"$set": {f"objeto{contador}": objetosDetectados}})
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
        try:
            os.system("clear")
            if documento["extensioArchivo"] in extensionesValidas:            
                objetosDetectados = detectarObjetos(documento["ruta_archivo"])
                if len(objetosDetectados) > 0:
                    contador = 0
                    print("Se detectaron objetos en el archivo: " + documento["nombre_archivo"])           
                    for objeto in objetosDetectados:
                        contador += 1
                        actualizarBaseDatos(documento["_id"], objeto, contador)
                        print(objeto)
        except Exception as e:
            print("Error al procesar el archivo: " + documento["nombre_archivo"] + " - " + str(e))
            pass
                   