import random
from deap import base, tools, algorithms, creator
import src.datosBarco as db
import numpy as np

def configurarPoblacion(toolbox):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax, pesos=list)
    toolbox.register("individual", crearIndividuo, creator.Individual, rows=db.__tamano_compartimento__,
                     cols=db.__tamano_compartimento__, compartimentos=db.__compartimentos__)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def configurarEvolucion(toolbox):
    # toolbox.register("mate", tools.cxPartialyMatched)
    # toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("mate", cruzar)
    toolbox.register("mutate", mutar, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("evaluate", evaluar)

def configuraEstadisticasEvolucion():
    stats = tools.Statistics(lambda ind: ind.fitness.values) 
    stats.register("avg", np.mean) 
    stats.register("std", np.std) 
    stats.register("min", np.min) 
    stats.register("max", np.max) 
    
    return stats

def cruzar(ind1, ind2):
    ind1, ind2 = tools.cxPartialyMatched(ind1, ind2)

    corregir(ind1)
    corregir(ind2)

    return ind1, ind2

def mutar(individual, indpb):
    individual = tools.mutShuffleIndexes(individual, indpb)

    corregir(individual[0])

    return individual

def evaluar(individuo):
    compartimentos = db.__compartimentos__
    filas = db.__tamano_compartimento__
    cols = db.__tamano_compartimento__

    num_vacios = compartimentos * filas ** 2 - db.__num_contenedores__
    vacios = 0

    eval = 0
    penalizacion = 0
    penalizacion_repetido = 0
    penalizacion_peso = 0

    evaluacion_puerto = 0

    contenedores = {}
    peso_compartimentos = [0 for i in range(0, compartimentos)]

    for i in range(0,compartimentos):
        peso_compartimentos[i] = 0
        for j in range(0,filas):
            for k in range(0, cols):
                posicion = i * (filas * cols) + (j * cols) + k
                contenedor = individuo[posicion]
                pos_superior = obetenerPosSuperior(i, posicion)
                if pos_superior != -1:
                    superior = individuo[pos_superior]
                else:
                    superior = -1

                if contenedor != -1:
                    existe = contenedores.get(contenedor)
                    if existe != None:
                        penalizacion_repetido = 50000
                    else:
                        contenedores[contenedor] = 1

                    peso = db.__contenedores__[contenedor][1]
                    puerto = db.__contenedores__[contenedor][2]
                    
                    peso_superior = 0
                    puerto_superior = 0
                    if superior != -1:
                        puerto_superior = db.__contenedores__[superior][2]
                        peso_superior = db.__contenedores__[superior][1]

                    if peso_superior > peso:
                        penalizacion_peso += 1

                    if puerto_superior <= puerto:
                        evaluacion_puerto += 1

                    peso_compartimentos[i] += peso
                else:
                    vacios += 1


    # Sumar penalizaciones
    if vacios != num_vacios:
        penalizacion += 50000

    penalizacion_peso = penalizacion_peso / db.__num_contenedores__
    penalizacion += penalizacion_peso * 10000
    penalizacion += penalizacion_repetido

    # Sumar recompensas
    evaluacion_puerto = evaluacion_puerto / db.__num_contenedores__
    eval += evaluacion_puerto * 10

    # desv = np.std(peso_compartimentos)
    # if desv == 0:
    #     desv = 1

    # eval += (1 / desv) * 50000
    max_peso = max(peso_compartimentos)
    min_peso = min(peso_compartimentos)
    diferencia = max_peso - min_peso
    if diferencia == 0:
        diferencia = 1
    eval += np.exp((1 / diferencia) * 100) * 10

    eval -= penalizacion

    return eval,


def strBarco(ind):
    out = ""
    for i in range(db.__tamano_compartimento__ - 1, -1, -1):
        out += "| "
        for j in range(0, db.__compartimentos__):
            for k in range(0, db.__tamano_compartimento__):
                out += str(ind[j * (db.__tamano_compartimento__ ** 2) + (i * db.__tamano_compartimento__) + k]).rjust(4) + " "
            out += "| "
        out += "\n"

    return out

def corregir(individuo):
    compartimentos = db.__compartimentos__
    filas = db.__tamano_compartimento__
    cols = db.__tamano_compartimento__

    for i in range(0,compartimentos):
        for j in range(0,filas):
            for k in range(0, cols):
                posicion = i * (filas * cols) + (j * cols) + k
                contenedor = individuo[posicion]
                pos_superior = obetenerPosSuperior(i, posicion)
                if pos_superior != -1:
                    superior = individuo[pos_superior]
                else:
                    superior = -1

                if contenedor == -1:
                    if superior != -1:
                        individuo[posicion], individuo[pos_superior] = individuo[pos_superior], individuo[posicion]
                else:
                    if superior != -1:
                        peso = db.__contenedores__[contenedor][1]
                        peso_superior = db.__contenedores__[superior][1]

                        if peso_superior > peso:
                            individuo[posicion], individuo[pos_superior] = individuo[pos_superior], individuo[posicion]

def obetenerPosSuperior(cont, posicion):
    tamano = db.__tamano_compartimento__**2
    ultima_pos = (cont + 1) * tamano

    superior = posicion + db.__tamano_compartimento__
    if superior >= ultima_pos:
        return -1

    return superior


def crearIndividuo(ind, rows, cols, compartimentos):
    lista_contenedores = listaPorPeso()

    barco = ind([-1 for i in range(0, rows * cols * compartimentos)])
    barco.pesos = [0 for i in range(0, compartimentos)]

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

        barco[pos] = contenedor[1]
        barco.pesos[compartimento] += db.__contenedores__[contenedor[1]][1]

        if posicion[0] < rows - 1:
            posiciones_validas[compartimento][posicion_][0] += 1
        else:
            posiciones_validas[compartimento].remove(posiciones_validas[compartimento][posicion_])

        

    return barco

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
