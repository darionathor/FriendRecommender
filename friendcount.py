import loadData

# load the network
loadData.load_network()

for i in range(0,150):
    firstCircle = set(loadData.network.neighbors(i))
    print i
    print len(firstCircle)
    print '-------'