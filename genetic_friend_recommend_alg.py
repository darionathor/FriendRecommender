import data_loader
import random
import operator
from clustering_coefficient import clustering_coeff
import genetic_algorithm as ga
from friend_value import Val
import numpy as np
# load the network
data_loader.load_network()
print 'loading complete'
usersLen = data_loader.network.number_of_nodes()
print usersLen
testResults = []
for center in range(0, usersLen):
    scores = []
    #filter
    firstCircle = set(data_loader.network.neighbors(center))
    print ('process: ', center)
    testFriends = random.sample(firstCircle, len(firstCircle)/10)
    for item in testFriends:
        firstCircle.remove(item)

    potentialFriends = set()
    for item in firstCircle:
        potentialFriends.add((item))
        for item2 in list(data_loader.network.neighbors((item))):
            potentialFriends.add(item2)

    #order
    for person in potentialFriends:

        neighbours = set(data_loader.network.neighbors((person)))
        shared_friends = firstCircle.intersection(neighbours)
        first_index = len(shared_friends)
        counted = set()
        edge_count = 0
        for friend in shared_friends:
            edges = set(data_loader.network.neighbors((friend)))
            countable_edges = []
            for item in edges:
                if item not in counted:
                    if item in shared_friends:
                        countable_edges.append(item)
                counted.add(item)
            edge_count = edge_count + len(countable_edges)
            counted.add(friend)
        shared_friends_count = len(shared_friends)

        second_index = clustering_coeff(shared_friends_count, edge_count)
        #
        counted = set()
        all_friends = firstCircle.union(neighbours)
        edge_count = 0
        for friend in all_friends:
            edges = set(data_loader.network.neighbors((friend)))
            countable_edges = []
            for item in edges:
                if item not in counted:
                    if item in all_friends:
                        countable_edges.append(item)
                counted.add(item)
            edge_count = edge_count + len(countable_edges)
            counted.add(friend)
        all_friends_count = len(all_friends)

        third_index = clustering_coeff(all_friends_count,edge_count)

        scores.append(Val(person,first_index,second_index,third_index))
    print 'generated indexes'

    weights = ga.genetic_alg(scores,firstCircle)

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