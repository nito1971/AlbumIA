from imageai.Detection import ObjectDetection
import os
import hashlib
import pymongo

# Declaramos variables.
execution_path = os.getcwd()
ruta = "/mnt/10.0.0.13/dos"
rutaModelosIA = "/mnt/local/datos/ModelosIA"
extensioneArchivosABuscar = ["jpg", "jpeg", "png", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "mp4", "avi", "mkv", "mov", "wmv", "flv"]

def obtenerRutaArchvosMongoDb(ruta_archivo):
    cliente = pymongo.MongoClient("mongodb://localhost:27017")
    db = cliente["inventario"]
    coleccion = db["archivos"]
    documento = coleccion.find_one({"ruta_archivo": ruta_archivo})
    return documento

def insert_mongo(_id, nombre_archivo, ruta_archivo, extensionArchivo, hash_archivo, peso):
    try:
      # Conexión a la base de datos local
      cliente = pymongo.MongoClient("mongodb://localhost:27017")
      # Seleccionar la base de datos y la colección
      db = cliente["inventario"]
      coleccion = db["archivos"]
      # Datos a insertar
      datos = [
        {
          "_id": _id,
          "nombre_archivo": nombre_archivo,
          "ruta_archivo": ruta_archivo,
          "extensioArchivo": extensionArchivo,
          "hash_archivo": hash_archivo, 
          "peso": peso               
        }      
      ]

      # Insertar los datos en la colección
      coleccion.insert_many(datos)

      # Cerrar la conexión a la base de datos
      cliente.close()
    except Exception as e:
       print(f"Error al insertar en MongoDB: {e}")
       cliente.close()
       return False

def generarHashId(cadena):
    return hashlib.sha512(cadena.encode()).hexdigest()

def generarHash(archivo):
    try:
        with open(archivo, 'rb') as f:
            data = f.read()
        return hashlib.sha512(data).hexdigest()
    except Exception as e:
        print(f"Error al generar el hash: {e}")
        return None
'''
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolov3.pt"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image1.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"), minimum_percentage_probability=30)
print(len(detections))

for eachObject in detections:    
    nombre = eachObject["name"]
    probabilidad = eachObject["percentage_probability"]
    coordenadas = eachObject["box_points"]
    x1 = coordenadas[0]
    y1 = coordenadas[1]
    x2 = coordenadas[2]
    y2 = coordenadas[3]
    print("*" * 40)
    print(f"Nombre objeto detectado: {nombre}")
    print(f"Probalidas: {probabilidad}")
    print(f"x1: {x1} y1: {y1} x2: {x2} y2: {y2}")

'''

def convertir_bytes_a_gb(bytes):
    # 1 Gigabyte es igual a 1,073,741,824 bytes
    gigabytes = bytes / 1073741824
    return gigabytes


def detectarObjetos(imagen):
    salida = []
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(rutaModelosIA , "yolov3.pt"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , imagen), minimum_percentage_probability=30)
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



'''
os.system("clear")
objetosDetectados = detectarObjetos("image1.jpg")
for objetos in objetosDetectados:
    print(objetos)
'''



def process_file(file_path):
    try:        
        
        if obtenerRutaArchvosMongoDb(file_path) != file_path:            
            file_name = os.path.basename(file_path) 
            extension = file_name.split(".")[-1]       
            size = convertir_bytes_a_gb(os.path.getsize(file_path))
            if extension in extensioneArchivosABuscar:                
                if size < 1024*3:
                    _id = generarHash(file_path)
                    hash_archivo = generarHashId(file_path)
                    insert_mongo(_id, file_name, file_path, extension, hash_archivo, size)
                    print(f"File: {file_name} - Size: {size} GB")            
                else:
                    _id = generarHashId(file_path)
                    hash_archivo = None
                    insert_mongo(_id, file_name, file_path, extension, hash_archivo, size)
                    print(f"File: {file_name} - Size: {size} GB")
            else:
                print(f"El archivo {file_name} no es un archivo válido!")
        else:
            print(f"El archivo {file_path} existe!")
        
    except Exception as e:
        print(f"Error: {e}")
        pass

if __name__ == "__main__":
    for root, dirs, files in os.walk(ruta):
        for file in files:
            process_file(os.path.join(root, file))
