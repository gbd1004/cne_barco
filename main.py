import src.datosBarco as db
import src.csv as csv
import src.evol as evol
from deap import base, algorithms, tools, creator
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

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=1000, verbose=False, stats=stats)

    output(logbook, population, True)


def output(logbook, population, debug=False):
    print("La mejor solucion encontrada es: ")
    sol = tools.selBest(population,1)[0]
    # sol = tools.selNSGA2(population, 1)[0]

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

    # f, (ax1, ax2, ax3) = plt.subplots(1, 3)

    # line1 = ax1.plot(gen, avgs, "r-", label="Average Fitness")
    # line2 = ax2.plot(gen, maxs, "g-", label="Max Fitness")
    # line3 = ax3.plot(gen, mins, "b-", label="Min Fitness")
    # ax1.set_xlabel("Generation")
    # ax1.set_ylabel("Fitness (AVG)", color="r")
    # ax2.set_xlabel("Generation")
    # ax2.set_ylabel("Fitness (MAX)", color="g")
    # ax3.set_xlabel("Generation")
    # ax3.set_ylabel("Fitness (MIN)", color="b")
    f, (ax1, ax2, ax3) = plt.subplots(1, 3)

    maxs_x = [i[0] for i in maxs]
    maxs_y = [i[1] for i in maxs]
    avgs_x = [i[0] for i in avgs]
    avgs_y = [i[1] for i in avgs]
    mins_x = [i[0] for i in mins]
    mins_y = [i[1] for i in mins]

    ax1.scatter(maxs_x, maxs_y, label="Average Fitness")
    ax1.set_xlabel("Puertos")
    ax1.set_ylabel("Peligrosidad")

    ax2.plot(gen, avgs_x, "r-", label="Average Fitness")
    ax2.plot(gen, maxs_x, "g-", label="Max Fitness")
    ax2.plot(gen, mins_x, "b-", label="Min Fitness")

    ax3.plot(gen, avgs_y, "r-", label="Average Fitness")
    ax3.plot(gen, maxs_y, "g-", label="Max Fitness")
    ax3.plot(gen, mins_y, "b-", label="Min Fitness")

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

