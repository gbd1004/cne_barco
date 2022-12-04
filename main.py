import src.datosBarco as db
import src.leer as leer
import src.evol as evol
from deap import base, algorithms, tools
import matplotlib.pyplot as plt

def main():
    toolbox = base.Toolbox()
    leer.read_csv('datos/boat_test03.csv')

    evol.configurarPoblacion(toolbox)
    evol.configurarEvolucion(toolbox)
    stats = evol.configuraEstadisticasEvolucion()
    
    # hof = tools.HallOfFame(5)

    population = toolbox.population(n=20)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=500, verbose=False, stats=stats)

    output(logbook, population)
    
    
def output(logbook, population):
    # print("El resultado de la evolución es: ")
    # print(logbook)

    print("La mejor solucion encontrada es: ")
    sol = tools.selBest(population,1)[0]
    # print(strBarco(sol))
    # testVaido(sol)

    gen = logbook.select("gen")
    avgs = logbook.select("avg")
    maxs = logbook.select("max")
    mins = logbook.select("min")
    
    fig, ax1 = plt.subplots()
    
    # line1 = ax1.plot(gen, avgs, "r-", label="Average Fitness")    
    line2 = ax1.plot(gen, maxs, "g-", label="Max Fitness")
    # line3 = ax1.plot(gen, mins, "b-", label="Min Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    
    plt.show()


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

