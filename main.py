import src.datosBarco as db
import src.csv as csv
import src.evol as evol
from deap import base, algorithms, tools, creator
import matplotlib.pyplot as plt
import os

import matplotlib
matplotlib.use('TkAgg',force=True)

test = "boat_test06"

def main():
    toolbox = base.Toolbox()
    csv.read_csv(f'datos/{test}.csv')

    evol.configurarPoblacion(toolbox)
    evol.configurarEvolucion(toolbox)
    stats = evol.configuraEstadisticasEvolucion()

    n = 100

    population = toolbox.population(n)
    hof = tools.HallOfFame(n)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, verbose=True, stats=stats, halloffame=hof)
    # population, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=n, lambda_=n * 2,
    #                                         cxpb=0.5, mutpb=0.5, ngen=100, 
    #                                         stats=stats, halloffame=hof)

    output(logbook, hof)

def verBarco(debug, frente):
    if os.path.exists(f"salida/{test}_out.csv"):
        os.remove(f"salida/{test}_out.csv")
    for sol in frente:
        printBarco(sol)
        if debug:
            print(strBarco(sol))
            print(strBarcoPesos(sol))
            print(strBarcoPuerto(sol))
            print(strBarcoPeligro(sol))
            testVaido(sol)

        csv.write_csv(sol, test) 

def output(logbook, hof, debug=True):
    frentes = tools.sortNondominated(hof, len(hof))

    verBarco(debug, frentes[0])

    gen = logbook.select("gen")
    avgs = logbook.select("avg")
    maxs = logbook.select("max")
    mins = logbook.select("min")

    frentes_x = []
    frentes_y = []
    mejor_x = []
    mejor_y = []

    for i, frente in enumerate(frentes):
        for ind in frente:
            if i == 0:
                mejor_x.append(ind.fitness.values[0])
                mejor_y.append(ind.fitness.values[1])
            else:
                frentes_x.append(ind.fitness.values[0])
                frentes_y.append(ind.fitness.values[1])

 
    f, (ax1, ax2, ax3) = plt.subplots(1, 3)

    maxs_x = [i[0] for i in maxs]
    maxs_y = [i[1] for i in maxs]
    avgs_x = [i[0] for i in avgs]
    avgs_y = [i[1] for i in avgs]
    mins_x = [i[0] for i in mins]
    mins_y = [i[1] for i in mins]

    ax1.scatter(frentes_x, frentes_y, label="Average Fitness")
    ax1.scatter(mejor_x, mejor_y, label="Average Fitness")
    ax1.set_xlabel("Peso y puertos")
    ax1.set_ylabel("Peligrosidad")

    ax2.plot(gen, avgs_x, "r-", label="Average Fitness")
    ax2.plot(gen, maxs_x, "g-", label="Max Fitness")
    ax2.plot(gen, mins_x, "b-", label="Min Fitness")
    ax2.set_xlabel("Peso y puertos")
    ax2.set_ylabel("Generación")

    ax3.plot(gen, avgs_y, "r-", label="Average Fitness")
    ax3.plot(gen, maxs_y, "g-", label="Max Fitness")
    ax3.plot(gen, mins_y, "b-", label="Min Fitness")
    ax3.set_xlabel("Peligrosidad")
    ax3.set_ylabel("Generación")

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
                print(num)
                return
        seen.add(num)
    print("Valido")

if __name__ == "__main__":
    main()

