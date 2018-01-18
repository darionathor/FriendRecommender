import loadData

# load the network
loadData.load_network()

print loadData.network.order()
print loadData.network.size()

# Look at a node's features
#print loadData.network.node[0]
list = loadData.network.neighbors(1)
for item in list:
    print item

# 0: feature not present for this user
# 1: user does not have this feature
# 2: user does have this feature

# look at the features of the whole network
#print loadData.feature_matrix()