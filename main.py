import src.datosBarco as db
import src.csv as csv
import src.evol as evol
from deap import base, algorithms, tools
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg',force=True)

test = "boat_test01"

def main():
    toolbox = base.Toolbox()
    csv.read_csv(f'datos/{test}.csv')

    evol.configurarPoblacion(toolbox)
    evol.configurarEvolucion(toolbox)
    stats = evol.configuraEstadisticasEvolucion()

    population = toolbox.population(n=20)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, verbose=True, stats=stats)

    output(logbook, population, debug=True)
    
    
def output(logbook, population, debug=False):
    print("La mejor solucion encontrada es: ")
    sol = tools.selBest(population,1)[0]
    
    printBarco(sol)
    if debug:
        print(strBarco(sol))
        print(strBarcoPesos(sol))
        print(strBarcoPuerto(sol))
        print(strBarcoPeligro(sol))
        testVaido(sol)

    csv.write_csv(sol, test)

    gen = logbook.select("gen")
    avgs = logbook.select("avg")
    maxs = logbook.select("max")
    mins = logbook.select("min")
    
    f, ax1 = plt.subplots(1, 1)
    
    line1 = ax1.plot(gen, avgs, "r-", label="Average Fitness")    
    line2 = ax1.plot(gen, maxs, "g-", label="Max Fitness")
    line3 = ax1.plot(gen, mins, "b-", label="Min Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_xlabel("Generation")

    plt.legend(loc="upper left")

    plt.show()

def printBarco(ind):
    print(str(db.__compartimentos__) + "," + str(db.__num_contenedores__))
    for i in range(0, db.__compartimentos__):
        for j in range(0, db.__tamano_compartimento__ ** 2):
            if j == db.__tamano_compartimento__ ** 2 - 1:
                end = ""
            else:
                end = ","
            print(str(ind[i * (db.__tamano_compartimento__ ** 2) + j]), end=end)
        print()

# Funciones auxiliares para debuggear
def strBarco(ind):
    out = ""
    for i in range(db.__tamano_compartimento__ - 1, -1, -1):
        out += "| "
        for j in range(0, db.__compartimentos__):
            for k in range(0, db.__tamano_compartimento__):
                indiv = ind[j * (db.__tamano_compartimento__ ** 2) + (i * db.__tamano_compartimento__) + k]
                if indiv >= db.__num_contenedores__:
                    out += " ".rjust(4) + " "
                else:
                    out += str(indiv).rjust(4) + " "
            out += "| "
        out += "\n"
    return out

def strBarcoPesos(ind):
    out = ""
    pesos = [0 for i in range(0, db.__compartimentos__)]
    for i in range(db.__tamano_compartimento__ - 1, -1, -1):
        out += "| "
        for j in range(0, db.__compartimentos__):
            for k in range(0, db.__tamano_compartimento__):
                indiv = ind[j * (db.__tamano_compartimento__ ** 2) + (i * db.__tamano_compartimento__) + k]
                if indiv >= db.__num_contenedores__:
                    peso = 0
                    pesostr = " "
                else:
                    peso = db.__contenedores__[indiv][1]
                    pesostr = str(db.__contenedores__[indiv][1])
                out += pesostr.rjust(4) + " "
                pesos[j] += peso
            out += "| "
        out += "\n"
    print(pesos)
    return out

def strBarcoPuerto(ind):
    out = ""
    for i in range(db.__tamano_compartimento__ - 1, -1, -1):
        out += "| "
        for j in range(0, db.__compartimentos__):
            for k in range(0, db.__tamano_compartimento__):
                indiv = ind[j * (db.__tamano_compartimento__ ** 2) + (i * db.__tamano_compartimento__) + k]
                if indiv >= db.__num_contenedores__:
                    puerto = " "
                else:
                    puerto = str(db.__contenedores__[indiv][2])
                out += puerto.rjust(4) + " "
            out += "| "
        out += "\n"
    return out

def strBarcoPeligro(ind):
    out = ""
    for i in range(db.__tamano_compartimento__ - 1, -1, -1):
        out += "| "
        for j in range(0, db.__compartimentos__):
            for k in range(0, db.__tamano_compartimento__):
                indiv = ind[j * (db.__tamano_compartimento__ ** 2) + (i * db.__tamano_compartimento__) + k]
                if indiv >= db.__num_contenedores__:
                    peligro = " "
                else:
                    peligro = str(db.__contenedores__[indiv][3])
                out += peligro.rjust(4) + " "
            out += "| "
        out += "\n"
    return out

def testVaido(ind):
    seen = set()
    for num in ind:
        if num in seen:
            if num != -1:
                print("INVALIDO")
                return
        seen.add(num)
    print("Valido")

if __name__ == "__main__":
    main()

