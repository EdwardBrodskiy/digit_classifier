# Digit Classifier

This project is a handwritten digit classifier network, trained on the MNIST dataset of normalized handwritten digit images. It leverages the numpy library to manage the matrix operations inherent in neural network computations. Alongside the classifier, the program also features a tool that allows you to draw your own digits and receive immediate feedback from the network.

Originally, I created this project as a learning experience to understand the inner workings of basic classifiers, shunning the use of high-level Python libraries like TensorFlow. Instead, I opted for numpy. This choice enriched my understanding of neural network fundamentals as it required me to personally implement key algorithms, such as back propagation.

## Preview at Current stage

![Classification of a 2](https://github.com/EdwardBrodskiy/digit_classifier/blob/master/sample-images/example-2.png)

## Installation

```bash
git clone https://github.com/EdwardBrodskiy/digit_classifier ./digit_classifier
```

### Windows:

```bash
pip install -r requirements.txt
```

### Linux:

```bash
pip3 install -r requirements.txt

sudo apt install python-tk \
```

## Functionality

- Run a selected Network with drawing gui

- Create new, load and save networks

- Non GUI training program available in networks/main_train.py

## Current Problems

The accuracy on testing data ends up being rather high however when actually drawing digits in the tool the accuracy is much lower. Currently I believe it is due to a bad scaling system(from image drawn to what gets fed to the network). I doubt that it is due to over fitting but I will be able to fully test it when I add monitoring tools.
