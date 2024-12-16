from numpy import random
import numpy as np

courses, schedule = [int(i) for i in input('Enter N, T: ').split()]
course_arr = []
for i in range(courses):
    course_arr.append(input(f'Course {i+1}: '))

def fitness(chromosome, n, t):
    overlap = 0
    consistency = 0
    y = ''
    for i in chromosome:
        for j in i:
            y += str(j)
    chromosome = y

    for i in range(0, len(chromosome), t):
        overlap += chromosome[i:i + t].count('1') - 1

    for i in range(t):
        consistency += abs(chromosome[i::t].count('1') - 1)

    fitness_value = -(overlap + consistency)
    return fitness_value

def chromosome_maker(n, t):
    x = random.randint(2, size=(courses, schedule))
    for i in x:
        if sum(i) == 0:
            i[random.randint(0, schedule)] = 1
    return x

chromosome = chromosome_maker(courses, schedule)

y = ''
for i in chromosome:
    for j in i:
        y += str(j)


def selection(population, n, t):
    fitnesses = []
    for i in population:
        fitnesses.append(fitness(i, n, t))
    fitnesses = np.array(fitnesses)
    population = np.array(population)
    sort = np.argsort(fitnesses)

    population = population[sort]
    fitnesses = fitnesses[sort]

    population = population[:2]

    new_population = []
    for i in range(0, 2):
        y = ''
        for J in population[i]:
            for K in J:
                y += str(K)
        new_population.append(y)

    return new_population

def crossover(chromosome1, chromosome2,p=1):
    flag = True
    while flag:
        cross_point = [random.randint(1, len(chromosome1) - 2) for _ in range(p)]
        flag = False
        if p>1:
          for i in range(p-1):
            if cross_point[i] > cross_point[i+1]:
              flag = True
              break


    population = []

    if p == 1:
        offspring1 = chromosome1[:cross_point[0]] + chromosome2[cross_point[0]:]
        offspring2 = chromosome2[:cross_point[0]] + chromosome1[cross_point[0]:]

    else:
        offspring1 = chromosome1[:cross_point[0]] + chromosome2[cross_point[0]:cross_point[1]] + chromosome1[cross_point[1]:]
        offspring2 = chromosome2[:cross_point[0]] + chromosome1[cross_point[0]:cross_point[1]] + chromosome2[cross_point[1]:]

    population = []

    population.append(offspring1)
    population.append(offspring2)
    return population

def mutation(chromosome,n):
    chromosome = list(chromosome)
    mutation_point = random.randint(0, len(chromosome))
    temp = chromosome.copy()
    temp[mutation_point] = '1' if temp[mutation_point] == '0' else '0'
    flag = True
    for i in range(0,len(chromosome),n):
      if temp[i:i+n].count('1') == 0:
        flag = False
        break
    if flag:
      chromosome = temp
    

    return ''.join(chromosome)

def genetic_algorithm(n, t, generations=4, p=1):
    population = []
    for i in range(4):
        population.append(chromosome_maker(n, t))

    population = selection(population, n, t)
    for _ in range(generations):

        population = crossover(population[0], population[1], p)

        for i in range(len(population)):
            if fitness(population[i], n, t) == 0:
                return population[i], fitness(population[i], n, t)

            population[i] = mutation(population[i],n)

            if fitness(population[i], n, t) == 0:
                return population[i], fitness(population[i], n, t)

    fitnesses = []

    for i in population:
        fitnesses.append(fitness(i, n, t))
    fitnesses = np.array(fitnesses)


    population = np.array(population)
    sort = np.argsort(fitnesses)

    population = population[sort]
    fitnesses = fitnesses[sort]


    population = population.tolist()
    return population[0], fitnesses[0]

generation = 400
cross_point = 1
print('Task1',genetic_algorithm(courses, schedule, generation, cross_point))
cross_point = 2
print('Task2',genetic_algorithm(courses, schedule, generation, cross_point))

