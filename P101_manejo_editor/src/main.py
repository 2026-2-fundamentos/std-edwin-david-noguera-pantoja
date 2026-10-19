import glob
import shutil
import os.path
import time
from pathlib import Path
import shutil

from P101_manejo_editor.src.helpers.mapper import mapper #imoortamos la funcion mapper desde el archivo mapper.py

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_FOLDER = ACTIVITY_DIR / "data"
INPUT_FOLDER = ACTIVITY_DIR / "temp" / "input"
OUTPUT_FOLDER = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_FOLDER = ACTIVITY_DIR / "submission"

# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------
#Refactorizacionde del codigo a funciones reutilizables

def clear_folder(folder):
    for file in glob.glob(f"{folder}/*"):
        os.remove(file)


def initialize_folder(folder):
    if os.path.exists(folder):
        clear_folder(folder)
    else: 
        os.makedirs(folder)


def delate_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def generate_files_copies (n):
    for file in glob.glob(f"{DATA_FOLDER}/*"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)

            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

            new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

            with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)



def reducer(pairs_sequence):
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result


#Empaquetamos todo el flujo de trabajo en una funcion para poder llamarla desde el main.py
def hadoop(imput_folder, output_folder, mapper,reducer):

    def read_recors_from_imput(): # se eencapsula porque es una funcion que solo se va a usar dentro de la funcion hadoop_word_count, no tiene sentido que sea global
        sequence = []
        files = glob.glob(f"{imput_folder}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence

    def shuffle_and_sort(pairs_sequence): # tambien es esclusicvo del hadoop
        pairs_sequence = sorted(pairs_sequence)
        return pairs_sequence

    def save_result_to_output(result): # no ponemos el output_folder como argumento porque ya esta definido en la funcion hadoop_word_count, no tiene sentido pasarlo como argumento a una funcion que solo se va a usar dentro de hadoop_word_count 
        with open(f"{output_folder}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")

    def create_sucess_file():
        with open(f"{output_folder}/_SUCCESS", "w", encoding="utf-8") as f:
            f.write("")

    def fail_if_output_exist():
        if os.path.exists(output_folder):
            raise Exception(
                f"La carpeta de salida {output_folder} ya existe."
                )


    fail_if_output_exist() # si la carpeta de salida existe, la borramos para evitar errores al crearla de nuevo
    sequence = read_recors_from_imput()
    pairs_sequence = mapper(sequence) 
    pairs_sequence = shuffle_and_sort(pairs_sequence)
    result = reducer(pairs_sequence)
    initialize_folder(output_folder) # Similar a la primera limpieza pero con otra carpeta, por eso solo pasamos la carpeta de salida como argumento a la funcion
    save_result_to_output(result)
    create_sucess_file()

#======================================0
#COPIA EL RESULTADO DESDE HDFS SIMULANDO EL DISCO LOCAL

def copy_hdf_output_to_submission(output_folder, submission_folder):
    initialize_folder(submission_folder)
    for file in glob.glob(f"{output_folder}/*"): # Itera sobre todos los archivos .txt en el directorio de envío
        shutil.copy2(file, submission_folder)

if __name__ == "__main__":
    initialize_folder(INPUT_FOLDER) # es igual o diferente al proceso de haddop? o se usa una funcion dentro de hadoop para verificar la existencia de la carpeta de salida?
    delate_folder(OUTPUT_FOLDER) # eliminamos la carpeta de salida para evitar errores al crearla de nuevo
    generate_files_copies(1000) # Genera copias de los archivos en raw/
    start_time = time.time()

    hadoop(imput_folder=INPUT_FOLDER, output_folder = OUTPUT_FOLDER, mapper = mapper, reducer = reducer)
    
    copy_hdf_output_to_submission(OUTPUT_FOLDER, SUBMISSION_FOLDER)

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")

# llamada a la funcion que contiene todo el flujo de trabajo


N = 1000
initialize_folder(INPUT_FOLDER) # es igual o diferente al proceso de haddop? o se usa una funcion dentro de hadoop para verificar la existencia de la carpeta de salida?
generate_files_copies(N)


# Lectura de los archivos, refactorizado a funciones reutilizables
# -----------------------------------------------------------------------------
start_time = time.time() # va por fuera de la funcion dado que es externo al flujo y no hace parte de la lógica



# Reporte de tiempo de ejecución
# -----------------------------------------------------------------------------





