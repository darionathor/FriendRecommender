import numpy as np
import operator
DNA_SIZE = 30            # DNA length
RNA_SIZE = 10
POP_SIZE = 200           # population size
CROSS_RATE = 0.8         # mating probability (DNA crossover)
MUTATION_RATE = 0.04    # mutation probability
N_GENERATIONS = 100
X_BOUND = [0, 1000]         #
#  x upper and lower bounds

def F(dnas,scores,firstCircle):
    average_positions = []
    for i in range(0,len(dnas[0])):
        ranking = {}
        sorted_ranking = []
        positions = []
        for value in scores:
            ranking[value.friend_index]=dnas[0][i]*value.first_index + dnas[1][i]*value.second_index + dnas[2][i]*value.third_index     # to find the maximum of this function
        for key, value in sorted(ranking.items(), key=operator.itemgetter(1)):
            sorted_ranking.append(key)
        for key in range(0, len(sorted_ranking)):
            if sorted_ranking[key] in firstCircle:
                positions.append(key)
        average_position = sum(positions)/float(len(positions))
        average_positions.append(average_position)
    return average_positions


# find non-zero fitness for selection
def get_fitness(pred): return pred +1e-3- np.min(pred)


# convert binary DNA to decimal and normalize it to a range(0, 1000)
def translateDNA(pop):
    x = pop[:,0:RNA_SIZE]
    y = pop[:,RNA_SIZE:2*RNA_SIZE]
    z = pop[:,2*RNA_SIZE:3*RNA_SIZE]
    return [x.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2**RNA_SIZE-1) * X_BOUND[1],
            y.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1],
            z.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1]]


def select(pop, fitness):    # nature selection wrt pop's fitness
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=fitness/fitness.sum())
    return pop[idx]


def crossover(parent, pop):     # mating process (genes crossover)
    if np.random.rand() < CROSS_RATE:
        i_ = np.random.randint(0, POP_SIZE, size=1)                             # select another individual from pop
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)   # choose crossover points
        parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
    return parent


def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child


def genetic_alg(scores,firstCircle):
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))   # initialize the pop DNA

    for _ in range(N_GENERATIONS):
        translatedDNA = translateDNA(pop)
        F_values = F(translatedDNA,scores,firstCircle)    # compute function value by extracting DNA
        F_values = np.array(F_values)

        # GA part (evolution)
        fitness = get_fitness(F_values)
        pop = select(pop, fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = crossover(parent, pop_copy)
            child = mutate(child)
            parent[:] = child       # parent is replaced by its child
    print 'generated weights'
    fitness = get_fitness(F_values)
    x = pop[np.argmax((fitness))][0:RNA_SIZE]
    y = pop[np.argmax((fitness))][RNA_SIZE:2 * RNA_SIZE]
    z = pop[np.argmax((fitness))][2 * RNA_SIZE:3 * RNA_SIZE]
    weights = [x.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1],
               y.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1],
               z.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1]]
    return weights