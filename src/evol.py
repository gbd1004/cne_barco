import random
from deap import base, tools, algorithms, creator
import src.datosBarco as db
import numpy as np

def configurarPoblacion(toolbox):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("individual", crearIndividuo, creator.Individual, rows=db.__tamano_compartimento__,
                     cols=db.__tamano_compartimento__, compartimentos=db.__compartimentos__)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def configurarEvolucion(toolbox):
    toolbox.register("mate", cruzar)
    toolbox.register("mutate", mutar, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=4)
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
    evaluacion_puerto = 0

    contenedores = {}
    peso_compartimentos = [0 for i in range(0, compartimentos)]

    for i in range(0,compartimentos):
        peso_compartimentos[i] = 0
        for j in range(0,filas):
            for k in range(0, cols):
                posicion = i * (filas * cols) + (j * cols) + k
                contenedor = individuo[posicion]
                superior = obtenerSuperior(i, posicion, individuo)

                if contenedor != -1:
                    existe = contenedores.get(contenedor)
                    if existe != None:
                        return -1,
                    else:
                        contenedores[contenedor] = 1

                    peso = db.__contenedores__[contenedor][1]
                    puerto = db.__contenedores__[contenedor][2]

                    puerto_superior = 0
                    if superior != -1:
                        puerto_superior = db.__contenedores__[superior][2]

                    if puerto_superior <= puerto:
                        evaluacion_puerto += 1

                    peso_compartimentos[i] += peso
                else:
                    vacios += 1

    # No valido
    if vacios != num_vacios:
        return -1,

    # Sumar recompensas
    evaluacion_puerto = evaluacion_puerto / db.__num_contenedores__
    eval += evaluacion_puerto * 20

    max_peso = max(peso_compartimentos)
    min_peso = min(peso_compartimentos)
    # diferencia = max_peso - min_peso
    # if diferencia == 0:
    #     diferencia = 1
    # eval += np.exp((1 / diferencia) * db.__num_contenedores__ * 20)
    div = min_peso / max_peso
    eval += np.exp(div * 5)

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
    cols = db.__tamano_compartimento__

    for compartimento in range(0, compartimentos):
        for col in range(0, cols):
            columna = obtenerColumna(individuo, compartimento, col)
            peso_columna = obtenerPeso(columna)
            colocarColumna(individuo, peso_columna, compartimento, col)

def obtenerColumna(individuo, compartimento, col):
    filas = db.__tamano_compartimento__

    elementos = []
    pos = compartimento * (filas ** 2) + col
    for i in range(0, filas):
        elementos.append(individuo[pos])
        pos += filas

    return elementos

def colocarColumna(individuo, columna: list, compartimento, col):
    filas = db.__tamano_compartimento__
    columna.sort(reverse=True)

    pos = compartimento * (filas ** 2) + col
    for i in range(0, filas):
        individuo[pos] = columna[i][1]
        pos += filas

def obtenerPeso(columna):
    elementos = []

    for i in columna:
        if i == -1:
            elementos.append((0, i))
        else:
            elementos.append((db.__contenedores__[i][1], i))

    return elementos

def obetenerPosSuperior(cont, posicion):
    tamano = db.__tamano_compartimento__**2
    ultima_pos = (cont + 1) * tamano

    superior = posicion + db.__tamano_compartimento__
    if superior >= ultima_pos:
        return -1

    return superior

def obtenerSuperior(cont, posicion, individuo):
    pos_superior = obetenerPosSuperior(cont, posicion)
    if pos_superior != -1:
        superior = individuo[pos_superior]
    else:
        superior = -1
    return superior


def crearIndividuo(ind, rows, cols, compartimentos):
    lista_contenedores = listaPorPeso()

    barco = ind([-1 for i in range(0, rows * cols * compartimentos)])

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
