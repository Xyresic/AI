import csv,math,random

class Point:
    def __init__(self,index,x,y):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Individual:
    def __init__(self,genes):
        self.genes = genes

    def __repr__(self):
        return str(fitness(self))
        #return str(self.genes)

def fitness(ind):
    dist = lambda a,b: math.sqrt(math.pow(a.x-b.x,2)+math.pow(a.y-b.y,2))
    fitval = 0
    for i in range(num_genes-1):
        fitval += dist(ind.genes[i],ind.genes[i+1])
    fitval += dist(ind.genes[0],ind.genes[-1])
    return fitval

def crossover(mother,father):
    choices = random.sample(range(num_genes),2)
    choices.sort()
    lbound = choices[0]
    ubound = choices[1]
    chromosome = [0]*num_genes
    for i in range(lbound,ubound):
        chromosome[i] = mother.genes[i]
    index = ubound
    while 0 in chromosome:
        if father.genes[index] not in chromosome:
            chromosome[ubound] = father.genes[index]
            ubound = (ubound + 1) % num_genes
        index = (index + 1) % num_genes
    return chromosome

def mutate(ind):
    choices = random.sample(range(num_genes),2)
    first = choices[0]
    second = choices[1]
    gene = ind.genes[first]
    ind.genes[first] = ind.genes[second]
    ind.genes[second] = gene

def mate(mother,father):
    child = Individual(crossover(mother,father))
    if random.random() < mutation_chance:
        mutate(child)
    return child

population_size = 10000
generations = 1000
mutation_chance = 0.2
elitism = 0.1
pool_size = 0.25
num_genes = 0

def evolve(puzzle_id):
    global num_genes
    points = []
    lines_after = -1
    with open('points.csv','r') as f:
        r = csv.reader(f)
        for line in r:
            if -1 < lines_after < 2:
                points.append(line)
                lines_after += 1
            if puzzle_id in line:
                lines_after += 1
    for i in range(len(points[0])):
        points.append(Point(i,int(points[0][i]),int(points[1][i])))
    points = points[2:]
    num_genes = len(points)

    population = []
    for i in range(population_size):
        chromosome = points
        random.shuffle(chromosome)
        seed = Individual(chromosome)
        population.append(seed)

    new_generation = []
    for i in range(generations):
        population.sort(key=fitness)
        num_elites = math.floor(math.floor(population_size*elitism))
        new_generation = population[:num_elites]
        top = population[:math.floor(population_size*pool_size)]
        for i in range(population_size-num_elites):
            parents = random.sample(top,2)
            new_generation.append(mate(parents[0],parents[1]))
        population = new_generation

    population.sort(key=fitness)
    return population[0]

puzzles = ['A4','A8','A9','A9-2','A10','A11','A12','A12-2','A13','A13-2','A30','A50']
#puzzles = ['A50']
for puzzle in puzzles:
    best = evolve(puzzle)
    path = [point.index for point in best.genes]
    #print(fitness(best))
    #print(path)
    with open('StudentPaths.csv','w' if puzzle == puzzles[0] else 'a') as f:
        w = csv.writer(f)
        f.write(puzzle+'\n')
        w.writerow(path)