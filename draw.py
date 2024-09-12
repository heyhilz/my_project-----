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

        # 拖放区域
        self.drop_area = tk.Label(root, text="Drag and drop your .xlsx file here", width=100, height=10, bg="lightgray")
        self.drop_area.pack(pady=20)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_file_drop)

        # 静态图
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # 按钮（放在图形下方）
        self.plot_button = tk.Button(root, text="Play", command=self.plot_trajectory)
        self.plot_button.pack(pady=10)

        self.data = None  # 存储数据

    def on_file_drop(self, event):
        # 获取拖拽文件的路径
        file_path = event.data
        self.load_data(file_path)

    def load_data(self, file_path):
        # 读取.xlsx文件
        try:
            df = pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
            self.data = df.to_numpy()
            
            if self.data.shape[1] < 2:
                raise ValueError("The data must contain at least two columns.")

            self.ax.clear()  # 清除旧图
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

        # 清空当前图形
        self.ax.clear()  
        self.ax.plot(self.data[:, 0], self.data[:, 1], label='Dynamic XY Path', color='blue')
        self.canvas.draw()

        # 动态展示轨迹
        for i in range(len(self.data)):
            self.ax.scatter(self.data[i, 0], self.data[i, 1], color='red')  # 更新为动态绘制
            self.canvas.draw()
            self.root.update()  # 更新界面
            plt.pause(0.05)  # 暂停以产生动画效果

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # 创建TkinterDnD的Tk窗口
    app = App(root)
    root.mainloop()
