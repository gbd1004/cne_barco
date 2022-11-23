import csv
import math
import src.datosBarco as db

def read_csv(path: str) -> None:
    with open(path, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        primera_linea = reader.__next__()
        db.__compartimentos__ = int(primera_linea[0])
        db.__num_contenedores__ = int(primera_linea[1])
        db.__contenedores__ = []


        contenedores_compartimento = db.__num_contenedores__ / db.__compartimentos__
        db.__tamano_compartimento__ = math.ceil(math.sqrt(contenedores_compartimento))
        # db.__dimensiones_compartimento__ = [, math.floor(math.sqrt(contenedores_compartimento))]

        for row in reader:
            db.__contenedores__.append([row[0], int(row[1]), int(row[2]), int(row[3])])