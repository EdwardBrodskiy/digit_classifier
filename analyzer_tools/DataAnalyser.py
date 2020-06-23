import numpy as np


def get_size_range(data):
    result = [[0, 0] for _ in data]

    for label in data:
        for image in data[label]:
            min_x, min_y = 28, 28
            max_x, max_y = -1, -1
            for i in range(image.shape[0]):
                if image[i, 0]:
                    x = i % 28
                    y = i // 28
                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    if y > max_y:
                        max_y = y
            result[label][0] += max_x - min_x
            result[label][1] += max_y - min_y

        result[label][0] /= len(data[label])
        result[label][1] /= len(data[label])

    return result


def brightness(data):
    result = [[0, 0] for _ in data]

    for label in data:

        for image in data[label]:
            mean = 0
            mx = 0
            for i in range(784):
                if image[i, 0] > 0.01:
                    mean += image[i, 0]
                    if image[i, 0] > mx:
                        mx = image[i, 0]
            result[label][0] += mean
            result[label][1] += mx

        result[label][0] /= 784 * len(data[label])
        result[label][1] /= len(data[label])

    return result
