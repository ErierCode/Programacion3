# [S5] Implementación y Visualización de Algoritmos de Ordenamiento

import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("S5: Algoritmos de Ordenamiento")

        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.grid(row=0, column=0)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=1, column=0)

        ttk.Label(self.frame, text="Seleccionar Método:").grid(row=0, column=0, padx=5, pady=5)
        
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.algo_menu = ttk.Combobox(self.frame, textvariable=self.algorithm_var, values=["Bubble Sort", "Selection Sort"])
        self.algo_menu.grid(row=0, column=1, padx=5, pady=5)

        self.generate_btn = ttk.Button(self.frame, text="Generar Lista", command=self.generate_list)
        self.generate_btn.grid(row=0, column=2, padx=5, pady=5)

        self.sort_btn = ttk.Button(self.frame, text="Ordenar", command=self.sort)
        self.sort_btn.grid(row=0, column=3, padx=5, pady=5)

        self.numbers = []
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack()

    def generate_list(self):
        self.numbers = [random.randint(1, 100) for _ in range(10)]
        self.draw_bars()

    def draw_bars(self, highlight=[]):
        self.ax.clear()
        colors = ['green' if i not in highlight else 'blue' for i in range(len(self.numbers))]
        self.ax.bar(range(len(self.numbers)), self.numbers, color=colors)
        self.ax.set_ylim(0, 110)
        self.canvas.draw()
        self.root.update()
    
    def bubble_sort(self):
        n = len(self.numbers)
        for i in range(n):
            swapped = False
            for j in range(n - 1 - i):
                if self.numbers[j] > self.numbers[j + 1]:
                    self.numbers[j], self.numbers[j + 1] = self.numbers[j + 1], self.numbers[j]
                    swapped = True
                    self.draw_bars([j, j + 1])
                    time.sleep(0.3)
            if not swapped:
                break

    def selection_sort(self):
        n = len(self.numbers)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if self.numbers[j] < self.numbers[min_idx]:
                    min_idx = j
            self.numbers[i], self.numbers[min_idx] = self.numbers[min_idx], self.numbers[i]
            self.draw_bars([i, min_idx])
            time.sleep(0.3)

    def sort(self):
        if not self.numbers:
            return

        algo = self.algorithm_var.get()
        if algo == "Bubble Sort":
            self.bubble_sort()
        elif algo == "Selection Sort":
            self.selection_sort()

        self.draw_bars()

root = tk.Tk()
app = SortingVisualizer(root)
root.mainloop()
