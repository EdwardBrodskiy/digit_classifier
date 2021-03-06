from analyzer_tools import DataAnalyser
from data_managers import DataHandler

training_data = DataHandler.read_mnist("../training_data/train/train-images.idx3-ubyte", "training_data/train/train-labels.idx1-ubyte")

sizes = DataAnalyser.brightness(training_data)




# width and height training_data
'''
with open("sizes.txt", 'wb') as file:
    pickle.dump(sizes, file)
'''
total_x, total_y = 0, 0

for label in range(len(sizes)):
    print(label, ":", sizes[label])
    total_x += sizes[label][0]
    total_y += sizes[label][1]

total_x /= len(sizes)
total_y /= len(sizes)

print("total average in x:", total_x)
print("total average in y:", total_y)
