import data_loader
import random
import operator
data_loader.load_network()
print 'loading complete'
usersLen = data_loader.network.number_of_nodes()
testResults = []
testResults1 = []
testResults2 = []
testResults3 = []
for center in range(0, usersLen):
    scores = {}
    #filter
    firstCircle = set(data_loader.network.neighbors(center))
    friend_count = len(firstCircle)
    if(friend_count<10):
        continue
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
        value = len(shared_friends)
        scores[person] = value
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    sorted_friends = []
    for key,value in sorted_scores:
        sorted_friends.append((key))
    testSize = len(testFriends)
    correctSuggestions = 0
    for i in range(len(sorted_friends) - testSize, len(sorted_friends)):
        if (i < len(sorted_friends)):
            if (sorted_friends[i] in testFriends):
                correctSuggestions = correctSuggestions + 1
    testResults.append(correctSuggestions / float(testSize))
    if friend_count>200:
        testResults1.append(correctSuggestions / float(testSize))
    if friend_count<200 and friend_count>100:
        testResults2.append(correctSuggestions / float(testSize))
    if friend_count<100:
        testResults3.append(correctSuggestions / float(testSize))
   # print '% of test friends recommended'
    #print correctSuggestions / float(testSize)
print sum(testResults)/float(len(testResults))
print ">200"
print sum(testResults1)/float(len(testResults1))
print ">100<200"
print sum(testResults2)/float(len(testResults2))
print "<100"
print sum(testResults3)/float(len(testResults3))