import shutil #Librería para operaciones de alto nivel con archivos y colecciones de archivos
import string # Librería para operaciones con cadenas de texto
from pathlib import Path # importamos la clase Path de la librería pathlib para trabajar con rutas de archivos y carprtas
import time # Librería para interactuar con el sistema operativo y medir el tiempo de ejecución
import os.path # Librería para interactuar con el sistema operativo
import glob # Librería para buscar archivos 

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Obtiene la ruta absoluta del directorio donde se encuentra el archivo actual
#sube un nivel para obtener la carpeta del proyecto

DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data") # Define la ruta del directorio de datos
INPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "input") # Define la ruta del directorio de entrada
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "output") # Define la ruta del directorio de salida
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission") # Define la ruta del directorio de envío

#la carpeta input debe existir y esta vacia, si no existe se crea
if os.path.exists(INPUT_FOLDER): #Simula el HDFS.
    for file in glob.glob(f"{INPUT_FOLDER}/*"): # Itera sobre todos los archivos .txt en el directorio de datos):
        os.remove(file) # Elimina el archivo
else:
    os.makedirs(INPUT_FOLDER) # Crea el directorio de entrada, al principio porque ni existe
    

# print("Directorio de trabajo:", os.getcwd())
# print("Carpeta del proyecto:", ACTIVITY_FOLDER)
# print("Carpeta data:", DATA_FOLDER)

#Generar copia de los archivos de data a la carpeta input en raw/

N = 1000
for file in glob.glob(f"{DATA_FOLDER}/*.txt"): # Itera sobre todos los archivos .txt en el directorio de y los debe copiar a la carpeta input ej: [text1.txt, text2.txt, text3.txt]
    with open(file, "r", encoding="utf-8") as f: # Abre el archivo en modo lectura cada texto y lo lee
        text = f.read() # Lee el contenido del archivo
        for i in range(1, N+1): # Itera N=1000 veces para crear N copias del archivo
            raw_file_name_with_extension = os.path.basename(file) # Obtiene el nombre del archivo con la extensión
            raw_file_name_without_extension = os.path.splitext(raw_file_name_with_extension)[0] # Obtiene el nombre del archivo sin la extensión, (mi_archivo, .txt)
            new_file_name = f"{raw_file_name_without_extension}_{i:05d}.txt" # Crea un nuevo nombre de archivo con un número incremental ej: mi_archivo_001.txt, mi_archivo_002.txt, ..., i:05d para formato 00100, 00101 ...
            with open(f"{INPUT_FOLDER}/{new_file_name}", "w", encoding="utf-8") as f2: # Crea los 1000 archivos de salida en la carpeta input con el nuevo nombre separados por coma
                f2.write(text) # Escribe el contenido del archivo original en el nuevo archivo

#imprimir los 10 primeros archivos de la carpeta input
# print("Archivos de entrada generados en la carpeta input:")
# for i, file in enumerate(glob.glob(f"{INPUT_FOLDER}/*.txt")):
#     if i >= 10:
#         break
#     print(f"  {os.path.basename(file)}")


#imprimir los primeros 10 archivos de la carpeta input del texto 2
# archivos_texto2 = sorted(glob.glob(f"{INPUT_FOLDER}/file2_*.txt"))
# print("Primeros 10 archivos de la carpeta input del texto 2:")
# for i, file in enumerate(archivos_texto2):
#     if i >= 10:
#         break
#     print(f"  {os.path.basename(file)}")

#=========================================================================================               
#Emulacion del HADOOP Distributed File System (HDFS) en la carpeta input, donde se almacenan los archivos de entrada para el procesamiento de MapReduce.

start_time = time.time() # Se inicia el temporizador para medir el tiempo de ejecución del programa
sequency = []
files = glob.glob(f"{INPUT_FOLDER}/*.txt") # Obtiene una lista de todos los archivos .txt en el directorio de entrada
for file in files: # Itera sobre cada archivo en la lista de archivos
    with open(file, "r", encoding="utf-8") as f: # Abre el archivo en modo lectura
        for line in f: # Itera sobre cada línea del archivo
            sequency.append((file, line)) # Agrega el archivo y la línea a la lista sequency como una tupla (archivo, línea)

 #imprimir los 10 primeros elementos de la lista sequency
#print(sequency[:10])

#=========================================================
#MAPER

pairs_sequence = []
for _, line in sequency: # Itera sobre cada tupla (archivo, línea) en la lista sequency
    line = line.lower() # Convierte la línea a minúsculas
    line = line.translate(str.maketrans("", "", string.punctuation)) # Elimina los signos de puntuación de la línea, para que solo queden palabras y espacios
    line = line.replace("\n", " ") # Reemplaza los saltos de línea por espacios, dado que son espacion invisibles, para que no afecten el conteo de palabras
    words = line.split() # Divide la línea en palabras usando espacios como delimitadores ej: "hola mundo" -> ["hola", "mundo"]
    pairs_sequence.extend([(word, 1) for word in words]) # Agrega una tupla (palabra, 1) a la lista pairs_sequence para cada palabra en la línea


#========================================
#ORDENAR
sorted_pairs = sorted(pairs_sequence)

# print ("Primeros 10 elementos de la lista pairs_sequence:")
# print(pairs_sequence[:10]) # Imprime los primeros 10 elementos de la lista pairs_sequence con salto de linea
# print(sorted_pairs[:10]) # Imprime los primeros 10 elementos de la lista sorted_pairs

from pprint import pprint
#pprint (sorted_pairs[:10]) # Imprime los primeros 10 elementos de la lista sorted_pairs con salto de linea


#========================================
#REDUCER

resulted = []
for key, value in sorted_pairs: # Itera sobre cada tupla (palabra, 1) en la lista sorted_pairs
    if resulted and resulted[-1][0] == key: # Si la lista resulted no está vacía y la última palabra agregada es igual a la palabra actual
        resulted[-1][1] += value # Suma el valor (1) a la última tupla en resulted, lo replaza con la nueva tupla (palabra, conteo acumulado) ej: ("hola", 1) + ("hola", 1) = ("hola", 2)
    else:
        resulted.append([key, value]) # Agrega una nueva tupla (palabra, 1) a la lista resulted

#pprint (resulted[:10]) # Imprime los primeros 10 elementos de la lista resulted con salto de linea


#=====================================
#CARPETA DE SALIDA (Debe estar vacia), de lo contrario en un sitema HADOOP real, se generaria un error de que la carpeta de salida ya existe y no se puede sobreescribir. Por eso se simula el HDFS eliminando los archivos de salida si existen.

if os.path.exists(OUTPUT_FOLDER): # Simula el HDFS.
    for file in glob.glob(f"{OUTPUT_FOLDER}/*"): # Itera sobre todos los archivos .txt en el directorio de salida
        os.remove(file) # Elimina el archivo
else:
    os.makedirs(OUTPUT_FOLDER) # Crea el directorio de salida

#CONTEO DE PALABRAS FINAL
with open(f"{OUTPUT_FOLDER}/part-00000", "w", encoding="utf-8") as f: # Crea un archivo temporal result como escritura en la carpeta de salida
    for key, value in resulted: # Itera sobre cada tupla (palabra, conteo) en la lista resulted
        f.write(f"{key}\t{value}\n") # Escribe la palabra y el conteo en el archivo part-00000 separados por tabulador

#==================================0
# MARCADOR DE EXITO

with open(f"{OUTPUT_FOLDER}/_SUCCESS", "w") as f: # Crea un archivo success en la carpeta de salida
    f.write("") # Escribe "success" en el archivo success, AUNQUE EN HADOOP SE CREA VACIO, SE CREA PARA SIMULAR EL HDFS

#======================================0
#COPIA EL RESULTADO DESDE HDFS SIMULANDO EL DISCO LOCAL

if os.path.exists(SUBMISSION_FOLDER): # Simula el HDFS.
    for file in glob.glob(f"{SUBMISSION_FOLDER}/*"): # Itera sobre todos los archivos .txt en el directorio de envío
        os.remove(file) # Elimina el archivo
else:
    os.makedirs(SUBMISSION_FOLDER) # Crea el directorio de envío

for file in glob.glob(f"{OUTPUT_FOLDER}/*"): # Itera sobre todos los archivos .txt en el directorio de salida
    shutil.copy2(file, SUBMISSION_FOLDER) # Copia el archivo a la carpeta de envío submision, shutil.copy2 mantiene la metadata del archivo original

pprint (resulted[:10]) # Imprime los primeros 10 elementos de la lista resulted con salto de linea


#======================================
#REPORTE DEL TIEMPO DE EJECUCION

end_time = time.time() # Obtiene el tiempo final de ejecución
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos") # Imprime el tiempo de ejecución en segundos con 2 decimales
