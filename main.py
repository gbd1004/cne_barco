import src.datosBarco as db
import src.leer as leer
import src.evol as evol
from deap import base

def main():
    toolbox = base.Toolbox()
    leer.read_csv('datos/boat_test01.csv')

    # print(db.__compartimentos__)
    # print(db.__num_contenedores__)
    # print(db.__contenedores__)
    # print(db.__dimensiones_compartimento__)

    evol.configurarPoblacion(toolbox)

    ind = toolbox.individual()
    print(ind)

    # ind_test = evol.crearIndividuo(db.__dimensiones_compartimento__[1], db.__dimensiones_compartimento__[0], 
    #                                db.__compartimentos__, db.__num_contenedores__);
    # print(ind.count(-1))
    # print(ind_test)

    evol.listaPorPeso()

if __name__ == "__main__":
    main()

