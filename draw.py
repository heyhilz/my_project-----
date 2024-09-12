# -*- coding: utf-8 -*-
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("XY Trajectory Drawer")
        self.root.geometry("800x800")

        # �Ϸ�����
        self.drop_area = tk.Label(root, text="Drag and drop your .xlsx file here", width=100, height=10, bg="lightgray")
        self.drop_area.pack(pady=20)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_file_drop)

        # ��̬ͼ
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # ��ť������ͼ���·���
        self.plot_button = tk.Button(root, text="Play", command=self.plot_trajectory)
        self.plot_button.pack(pady=10)

        self.data = None  # �洢����

    def on_file_drop(self, event):
        # ��ȡ��ק�ļ���·��
        file_path = event.data
        self.load_data(file_path)

    def load_data(self, file_path):
        # ��ȡ.xlsx�ļ�
        try:
            df = pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
            self.data = df.to_numpy()
            
            if self.data.shape[1] < 2:
                raise ValueError("The data must contain at least two columns.")

            self.ax.clear()  # �����ͼ
            self.ax.plot(self.data[:, 0], self.data[:, 1], label='Static XY Path', color='blue')
            self.ax.set_title("Static XY Path")
            self.ax.set_xlabel("X-axis")
            self.ax.set_ylabel("Y-axis")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            print(f"Error loading data: {e}")

    def plot_trajectory(self):
        if self.data is None:
            print("No data to plot.")
            return

        # ��յ�ǰͼ��
        self.ax.clear()  
        self.ax.plot(self.data[:, 0], self.data[:, 1], label='Dynamic XY Path', color='blue')
        self.canvas.draw()

        # ��̬չʾ�켣
        for i in range(len(self.data)):
            self.ax.scatter(self.data[i, 0], self.data[i, 1], color='red')  # ����Ϊ��̬����
            self.canvas.draw()
            self.root.update()  # ���½���
            plt.pause(0.05)  # ��ͣ�Բ�������Ч��

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # ����TkinterDnD��Tk����
    app = App(root)
    root.mainloop()
