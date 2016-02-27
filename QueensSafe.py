import random
import numpy as np
from deap import algorithms, base, creator, tools


creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# This is the fitness evaluation method. Using the check direction checks how many times
# queens are threaning each other. We are trying to minimize this number.
def evalNumThreaten(individual):
    numThreaten = 0
    for i in range(0,7,1):
        currentQRow = individual[i]
        currentQCol = i
        for j in range(i+1,8,1):
            otherQRow = individual[j]
            otherQCol = j
            if currentQRow == otherQRow:
                numThreaten += 1
            if checkDirection(currentQRow,currentQCol,otherQRow,otherQCol,1,1):
                numThreaten += 1
            if checkDirection(currentQRow,currentQCol,otherQRow,otherQCol,1,-1):
                numThreaten += 1
            if checkDirection(currentQRow,currentQCol,otherQRow,otherQCol,-1,1):
                numThreaten += 1
            if checkDirection(currentQRow,currentQCol,otherQRow,otherQCol,-1,-1):
                numThreaten += 1
    return (numThreaten,)
# Checks the direction for threatens according to different parameters.
def checkDirection(currentQRow,currentQCol,otherQRow,otherQCol,rowChange,colChange):
    while ((currentQRow < 8) & (currentQRow >= 0) & (currentQCol <8) & (currentQCol>=0)):
        if (currentQRow == otherQRow) & (currentQCol == otherQCol):
            return True
        currentQRow += rowChange
        currentQCol += colChange
    return False
# We randomize ints between 0 - 7 since every queen is going to be in a different row.
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint,0,7)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=8)
toolbox.register("population", tools.initRepeat, list, 
                 toolbox.individual)
# Uses uniform crossover.
# Mutation is uniform integers between 0 and 7.
# Selection is tournament selection and tournament size is 2.
toolbox.register("evaluate", evalNumThreaten)
toolbox.register("mate", tools.cxUniform,indpb = 0.5)
toolbox.register("mutate", tools.mutUniformInt, indpb=0.05,low = 0,up=7)
toolbox.register("select", tools.selTournament, tournsize=2)
hof = tools.HallOfFame(100)
# Size of every population is 300
pop = toolbox.population(n=300)

# This method is copy pasted from the DEAP source code but its modified to loop until finding the optimal solution.
# It is also modified to print out the number of generations it took to find the optimal solution
def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    gen = 1
    while evalNumThreaten(tools.selBest(population, k=1)[0])[0] != 0:
        gen += 1
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream
    print 'total generations is',gen
    return population, logbook
# 150 generations are being created
result = eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.4, 
                             ngen=150,halloffame=hof, verbose=False)

bestBoard = tools.selBest(pop, k=1)[0]
# Prints the best individual from the population
print 'Number of threatens is', evalNumThreaten(tools.selBest(pop, k=1)[0])[0]

board = [['*' for x in range(8)] for x in range(8)]
print 'Rows for the queens are',bestBoard, '.Every Queen has its own column'
for i in range(0,8,1):
    board[bestBoard[i]][i] = 'Q'
for j in range(8):
    print board[j]
