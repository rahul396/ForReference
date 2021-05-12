import numpy


def find_coefficients(data):
    X = [x for x in data]
    Y = [data[x] for x in data]
    mean_x = numpy.mean(X)
    mean_y = numpy.mean(Y)
    mean_diff_x = [x - mean_x for x in X]
    mean_diff_y = [y - mean_y for y in Y]
    mean_diff_x_squared = [x ** 2 for x in X]
    mean_diff_y_squared = [y ** 2 for y in Y]
    product_x_y = []
    for i in range(len(X)):
        product_x_y.append(X[i] * Y[i])
    r_n = numpy.sum(product_x_y)
    r_d = numpy.sqrt(numpy.sum(mean_diff_x_squared) * numpy.sum(mean_diff_y_squared))
    r = r_n / float(r_d)
    print ('Correlation Coefficient: ' + str(r))

    sigma_x = numpy.sqrt(numpy.divide(numpy.sum(mean_diff_x_squared), len(data) - 1))
    sigma_y = numpy.sqrt(numpy.divide(numpy.sum(mean_diff_y_squared), len(data) - 1))

    b = r * numpy.divide(sigma_y, sigma_x)
    a = mean_y - b * mean_x
    return (a, b)


def predict_y(x):
    (a, b) = find_coefficients(data)
    print (a, b)
    return a + b * x


if __name__ == '__main__':
    data = {1: 2, 2: 3, 3: 5, 6: 8, 8: 11, 11: 14}
    print (predict_y(40))
