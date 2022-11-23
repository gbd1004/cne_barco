import random
from deap import base, tools, algorithms, creator
import src.datosBarco as db

def configurarPoblacion(toolbox):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("individual", crearIndividuo, rows=db.__tamano_compartimento__,
                     cols=db.__tamano_compartimento__, compartimentos=db.__compartimentos__)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def crearIndividuo(rows, cols, compartimentos):
    lista_contenedores = listaPorPeso()
    ret = [-1 for i in range(0, rows * cols * compartimentos)]

    posiciones_validas = initPosicionesValidas(cols, compartimentos)

    while len(lista_contenedores) > 0:
        compartimento = random.randint(0, compartimentos - 1)
        posibles = posiciones_validas[compartimento]
        num_posibles = len(posibles)

        if num_posibles == 0:
            continue

        posicion_ = random.randint(0, num_posibles - 1)
        posicion = posibles[posicion_]
        
        pos = compartimento * (rows * cols) + (posicion[0] * cols) + posicion[1]

        contenedor = lista_contenedores[0]
        lista_contenedores.remove(contenedor)

        ret[pos] = contenedor[1]

        if posicion[0] < rows - 1:
            posiciones_validas[compartimento][posicion_][0] += 1
        else:
            posiciones_validas[compartimento].remove(posiciones_validas[compartimento][posicion_])

    return ret

def initPosicionesValidas(cols, compartimentos):
    posiciones_validas = []
    for i in range(0, compartimentos):
        compartimento = []
        for j in range(0, cols):
            compartimento.append([0, j])
        posiciones_validas.append(compartimento)
    
    return posiciones_validas

def listaPorPeso():
    lista = [[a[1], i] for i, a in enumerate(db.__contenedores__)]
    lista.sort(reverse=True)
    return lista
