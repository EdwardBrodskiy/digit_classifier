import numpy as np
from networks import network
from file_managers import DataHandler

'''

top = tk.Tk()
top.title("Digit Classifier")

window = Visual.Visual(top)
'''
save_to = input("Save to what file: ")

training_data = DataHandler.read_mnist("../training_data/train/train-images.idx3-ubyte", "training_data/train/train-labels.idx1-ubyte")
testing_data = DataHandler.read_mnist("../training_data/test/t10k-images.idx3-ubyte", "training_data/test/t10k-labels.idx1-ubyte")
structure = [784, 16, 16, 10]
net = network.ClassifierTrainer(*structure)
# net = network.Network([784, 256, 16, 10]).load('best.txt')
'''
schedule = scheduler.Scheduler()
schedule.add_event("window update", 0.001)
'''
gradient = None
points = {l: 0 for l in training_data}
training_set = dict()
record = 0
while True:
    training_set, points = DataHandler.take_out_each(training_data, 5, points)

    gradient = net.train(training_set)
    gradient = gradient.__idiv__(50)
    net -= gradient
    if len(training_set[0]) == 0:
        accuracies = np.zeros(shape=(10, 1))
        for label in testing_data:
            for i in testing_data[label]:
                if net.pick(net.calculate(i)) == label:
                    accuracies[label, 0] += 1
            accuracies[label, 0] = accuracies[label, 0] / len(testing_data[label])
        accuracies *= 100
        print(np.transpose(accuracies))
        accuracy = accuracies.sum() / 10
        print(accuracy)

        points = {l: len(training_data[l]) for l in training_data}
        if accuracy > record:
            record = accuracy
            net.save(save_to + '.txt')
    '''
    if schedule.check_event("window update"):
        top.update_idletasks()
        top.update()
    '''
