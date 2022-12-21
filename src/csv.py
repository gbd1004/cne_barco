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
        db.__num_peligrosos__ = 0

        contenedores_compartimento = db.__num_contenedores__ / db.__compartimentos__
        db.__tamano_compartimento__ = math.ceil(math.sqrt(contenedores_compartimento))

        for row in reader:
            db.__contenedores__.append([row[0], int(row[1]), int(row[2]), int(row[3])])
            if int(row[3]) == 1:
                db.__num_peligrosos__ += 1

def write_csv(ind, path):
    with open(f"salida/{path}_out.csv", "a") as file:
        csvwriter = csv.writer(file)
        cabecera = [str(db.__compartimentos__), str(db.__num_contenedores__)]

        csvwriter.writerow(cabecera)

        for i in range(0, db.__compartimentos__):
            row = []
            for j in range(0, db.__tamano_compartimento__ ** 2):
                indiv = ind[i * (db.__tamano_compartimento__ ** 2) + j]
                if indiv >= db.__num_contenedores__:
                    istr = "-1"
                else:
                    istr = str(ind[i * (db.__tamano_compartimento__ ** 2) + j])
                row.append(istr)

            csvwriter.writerow(row)