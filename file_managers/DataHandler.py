import numpy as np


def read_mnist(file_path_imgs, file_path_labels, amount=1):
    with open(file_path_imgs, "rb") as imgs:
        with open(file_path_labels, "rb") as labels:
            number_of_elements, img_resolution = get_meta_data(imgs, labels)
            elements_per_img = img_resolution[0] * img_resolution[1]

            data = {i: [] for i in range(10)}

            for i in range(int(round(number_of_elements * amount, 0))):
                label = int.from_bytes(labels.read(1), byteorder='big')
                image = []
                for j in range(elements_per_img):
                    image.append([int.from_bytes(imgs.read(1), byteorder='big') / 255])

                data[label].append(np.array(image, dtype='float32'))

    return data


def get_meta_data(imgs, labels):
    check_magic_numbers(imgs, labels)

    number_of_elements = check_number_of_elements(imgs, labels)
    img_resolution = get_resolution(imgs)

    return number_of_elements, img_resolution


def check_magic_numbers(imgs, labels):
    imgs_magic_num = int.from_bytes(imgs.read(4), byteorder="big")
    if imgs_magic_num != 2051:
        print("Not the correct file given for the images")
    labels_magic_num = int.from_bytes(labels.read(4), byteorder="big")
    if labels_magic_num != 2049:
        print("Not the correct file given for the labels")


def check_number_of_elements(imgs, labels):
    num_of_imgs = int.from_bytes(imgs.read(4), byteorder='big')
    num_of_labels = int.from_bytes(labels.read(4), byteorder='big')
    if num_of_imgs != num_of_labels:
        print("Label size doesn't match Image size")
    return min(num_of_labels, num_of_imgs)


def get_resolution(imgs):
    rows = int.from_bytes(imgs.read(4), byteorder='big')
    columns = int.from_bytes(imgs.read(4), byteorder='big')
    return rows, columns


def take_out_each(data, amount, points):
    sub_set = {i: [] for i in range(len(data))}
    for i in data:
        if amount > points[i]:
            sub_set = {i: [] for i in range(len(data))}
            break

        sub_set[i] += data[i][points[i]-amount:points[i]]
        points[i] -= amount

    return sub_set, points
