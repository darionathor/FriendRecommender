import loadData
import random
import operator
from friendValue import Val
import numpy as np
# load the network
loadData.load_network()
print 'loading complete'
usersLen = loadData.network.number_of_nodes()
print usersLen
testResults = []
for center in range(0, usersLen):
    scores = []
    #filter
    firstCircle = set(loadData.network.neighbors(center))
    if len(firstCircle)>100 or len(firstCircle)<10:
        continue
    print ('process: ', center)
    testFriends = random.sample(firstCircle, len(firstCircle)/10)
    for item in testFriends:
        firstCircle.remove(item)

    potentialFriends = set()
    for item in firstCircle:
        potentialFriends.add((item))
        for item2 in list(loadData.network.neighbors((item))):
            potentialFriends.add(item2)

    #order
    for person in potentialFriends:

        neighbours = set(loadData.network.neighbors((person)))
        shared_friends = firstCircle.intersection(neighbours)
        first_index = len(shared_friends)
        counted = set()
        edge_count = 0
        for friend in shared_friends:
            edges = set(loadData.network.neighbors((friend)))
            countable_edges = []
            for item in edges:
                if item not in counted:
                    if item in shared_friends:
                        countable_edges.append(item)
                counted.add(item)
            edge_count = edge_count + len(countable_edges)
            counted.add(friend)
        shared_friends_count = len(shared_friends)
        max_edge_count = (shared_friends_count*(shared_friends_count-1))/2.0
        if max_edge_count!=0:
            second_index = edge_count/float(max_edge_count)
        else:
            second_index = 0.0
        #
        counted = set()
        all_friends = firstCircle.union(neighbours)
        edge_count = 0
        for friend in all_friends:
            edges = set(loadData.network.neighbors((friend)))
            countable_edges = []
            for item in edges:
                if item not in counted:
                    if item in all_friends:
                        countable_edges.append(item)
                counted.add(item)
            edge_count = edge_count + len(countable_edges)
            counted.add(friend)
        all_friends_count = len(all_friends)
        max_edge_count = (all_friends_count*(all_friends_count-1))/2.0
        if max_edge_count!=0:
            third_index = edge_count/float(all_friends_count)
        else:
            third_index = 0.0
        scores.append(Val(person,first_index,second_index,third_index))
    print 'generated indexes'

    DNA_SIZE = 30            # DNA length
    RNA_SIZE = 10
    POP_SIZE = 200           # population size
    CROSS_RATE = 0.8         # mating probability (DNA crossover)
    MUTATION_RATE = 0.04    # mutation probability
    N_GENERATIONS = 100
    X_BOUND = [0, 1000]         #
    #  x upper and lower bounds

    def F(dnas):
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


    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))   # initialize the pop DNA

    for _ in range(N_GENERATIONS):
        translatedDNA = translateDNA(pop)
        F_values = F(translatedDNA)    # compute function value by extracting DNA
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
    y = pop[np.argmax((fitness))][RNA_SIZE:2*RNA_SIZE]
    z = pop[np.argmax((fitness))][2*RNA_SIZE:3*RNA_SIZE]
    weights = [x.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2**RNA_SIZE-1) * X_BOUND[1],
                y.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1],
                z.dot(2 ** np.arange(RNA_SIZE)[::-1]) / float(2 ** RNA_SIZE - 1) * X_BOUND[1]]
    positions = []
    sorted_ranking = []
    ranking = {}
    for value in scores:
        ranking[value.friend_index]=weights[0]*value.first_index + weights[1]*value.second_index + weights[2]*value.third_index     # to find the maximum of this function
    for key, value in sorted(ranking.items(), key=operator.itemgetter(1)):
        sorted_ranking.append(key)
    for key in range(0, len(sorted_ranking)):
        if sorted_ranking[key] not in firstCircle:
            positions.append(sorted_ranking[key])
    correctSuggestions = 0
    testSize = len(testFriends)
    for i in range(len(positions)-testSize,len(positions)):
        if(i<len(positions)):
            if(positions[i] in testFriends):
                correctSuggestions = correctSuggestions +1
    testResults.append(correctSuggestions/float(testSize))
    print '% of test friends recommended'
    print correctSuggestions/float(testSize)

print sum(testResults)/float(len(testResults))