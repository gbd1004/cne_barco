import random
from deap import base, tools, algorithms, creator
import src.datosBarco as db
import numpy as np

def configurarPoblacion(toolbox):
    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("individual", crearIndividuo, creator.Individual, rows=db.__tamano_compartimento__,
                     cols=db.__tamano_compartimento__, compartimentos=db.__compartimentos__)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def configurarEvolucion(toolbox):
    toolbox.register("mate", cruzar)
    toolbox.register("mutate", mutar, indpb=0.2)
    # toolbox.register("select", tools.selTournament, tournsize=4)
    # toolbox.register("select", tools.selSPEA2)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluar)


def configuraEstadisticasEvolucion():
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    return stats

def cruzar(ind1, ind2):
    ind1, ind2 = tools.cxPartialyMatched(ind1, ind2)

    corregirPesos(ind1)
    corregirPesos(ind2)

    return ind1, ind2

def mutar(individual, indpb):
    individual = tools.mutShuffleIndexes(individual, indpb)

    corregirPesos(individual[0])

    return individual

def tiene_adyacente(ind, contenedor, posicion, i, j):
    peligro_actual = obtenerValor(contenedor, 3)

    if peligro_actual == 0:
        return 0

    superior = obtenerSuperior(i, posicion, ind)
    peligro_superior = obtenerValor(superior, 3)
    if peligro_superior == 1:
        return 1

    inferior = obtenerInferior(i, posicion, ind)
    peligro_inferior = obtenerValor(inferior, 3)
    if peligro_inferior == 1:
        return 1

    izquierdo = obtenerIzquierdo(j, i, posicion, ind)
    peligro_izquierdo = obtenerValor(izquierdo, 3)
    if peligro_izquierdo == 1:
        return 1

    derecho = obtenerDerecho(j, i, posicion, ind)
    peligro_derecho = obtenerValor(derecho, 3)
    if peligro_derecho == 1:
        return 1

    return 0

def evaluar(ind):
    compartimentos = db.__compartimentos__
    filas = db.__tamano_compartimento__
    cols = db.__tamano_compartimento__

    peso_compartimentos = [0 for i in range(0, compartimentos)]
    
    evaluacion_puerto = 0

    evaluacion_peligro = db.__num_peligrosos__
    eval_puerto = 0
    eval_peligro = 0

    for i in range(0,compartimentos):
        peso_compartimentos[i] = 0
        for j in range(0,filas):
            for k in range(0, cols):
                posicion = i * (filas * cols) + (j * cols) + k
                contenedor = ind[posicion]
                superior = obtenerSuperior(i, posicion, ind)

                if contenedor >= db.__num_contenedores__:
                    continue

                peso = obtenerValor(contenedor, 1)
                puerto = obtenerValor(contenedor, 2)

                puerto_superior = obtenerValor(superior, 2)

                if puerto_superior <= puerto:
                    evaluacion_puerto += 1

                peso_compartimentos[i] += peso

                evaluacion_peligro -= tiene_adyacente(ind, contenedor, posicion, i, j)


    evaluacion_peligro = evaluacion_peligro / db.__num_peligrosos__
    eval_peligro += evaluacion_peligro * 40

    # Sumar recompensas
    evaluacion_puerto = evaluacion_puerto / db.__num_contenedores__
    eval_puerto += evaluacion_puerto * 40

    max_peso = max(peso_compartimentos)
    min_peso = min(peso_compartimentos)
    div = min_peso / max_peso
    eval_distribucion = np.exp(div * 5)

    eval_puerto += eval_distribucion

    return eval_puerto, eval_peligro

def obtenerValor(pos, indice):
    val = 0
    if pos != -1 and pos < db.__num_contenedores__:
        val = db.__contenedores__[pos][indice]

    return val

def corregirPesos(individuo):
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
        if i >= db.__num_contenedores__:
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

def obetenerPosInferior(cont, posicion):
    tamano = db.__tamano_compartimento__**2
    primera_pos = cont * tamano

    inferior = posicion - db.__tamano_compartimento__
    if inferior < primera_pos:
        return -1

    return inferior

def obtenerInferior(cont, posicion, individuo):
    pos_inferior = obetenerPosInferior(cont, posicion)
    if pos_inferior != -1:
        inferior = individuo[pos_inferior]
    else:
        inferior = -1
    return inferior

def obetenerPosIzquierdo(fila, cont, posicion):
    tamano = db.__tamano_compartimento__
    primera_pos = cont * (tamano ** 2) + fila * tamano

    izquierdo = posicion - 1
    if izquierdo < primera_pos:
        return -1

    return izquierdo

def obtenerIzquierdo(fila, cont, posicion, individuo):
    pos_izquierdo = obetenerPosIzquierdo(fila, cont, posicion)
    if pos_izquierdo != -1:
        izquierdo = individuo[pos_izquierdo]
    else:
        izquierdo = -1
    return izquierdo

def obetenerPosDerecho(fila, cont, posicion):
    tamano = db.__tamano_compartimento__
    ultima_pos = cont * (tamano ** 2) + (fila + 1) * tamano

    derecho = posicion + 1
    if derecho >= ultima_pos:
        return -1

    return derecho

def obtenerDerecho(fila, cont, posicion, individuo):
    pos_derecho = obetenerPosDerecho(fila, cont, posicion)
    if pos_derecho != -1:
        derecho = individuo[pos_derecho]
    else:
        derecho = -1
    return derecho

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

    id_vacio = db.__num_contenedores__
    for i in range(len(barco)):
        if barco[i] == -1:
            barco[i] = id_vacio
            id_vacio += 1

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
