import loadData

# load the network
loadData.load_network()

center = 14
scores = {}
#filter
firstCircle = set(loadData.network.neighbors(center))
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
    scores[person] = 0
#forming the second index
#take a group of persons, add up all the edges between them, divide by how many edges they could have max
