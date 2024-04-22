import hashlib

def generarHash(archivo):
    with open(archivo, 'rb') as f:
        data = f.read()
    return hashlib.sha512(data).hexdigest()

archivo = './python/imageai_1/image.jpg'
print(generarHash(archivo))