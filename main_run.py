import numpy as np
import tkinter as tk
import network
import run_gui

root = tk.Tk()

load_from = input("What file: ")
net = network.Network([784, 256, 16, 10]).load(load_from + '.txt')

window = run_gui.RunGUI(root, net)

root.mainloop()
