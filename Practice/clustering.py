import numpy
# import matplotlib.pyplot as plot


def makeClusters(array, k, iterations):
    """Will return k clusters. It will decrease the number of clusters if the clusters are redundant"""
    randomIndices = numpy.random.choice(range(len(array)), k)
    # means = numpy.random.choice(array, k)
    means = numpy.array(array)[randomIndices].tolist()
    while iterations > 0:
        clusters = {key: [] for key in range(k)}
        for element in array:
            differences = [numpy.absolute(element - m) for m in means]
            minIndex = differences.index(min(differences))  # will give the index of the min value. Will return the first index incase multiple min values
            clusters[minIndex].append(element)
        means = [numpy.mean(clusters[key]) for key in clusters if clusters[key]]
        isnan = numpy.isnan(means)
        means = numpy.array(means)[~isnan]
        iterations -= 1
    clusters = [clusters[key] for key in clusters if clusters[key]]
    return clusters


if __name__ == '__main__':
    size = input('Enter array size: ')
    A = [numpy.random.randint(100) for _ in range(int(size))]
    k = input('Enter number of clusters: ')
    iterations = input('Enter number of iterations: ')
    clusters = makeClusters(A, k, iterations)
    # arr = numpy.array(clusters)
    print ("Number of cluster: ", str(len(clusters)))
    y = []
    for row in clusters:
        for i in row:
            y.append(i)

    x = numpy.linspace(1, len(y), len(y))
    # plot.scatter(x, y)
    # plot.show()
