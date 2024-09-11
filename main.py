# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import os

from joint2world import process_data
from joint2world_5axes import process_data2


class App:
    def __init__(self, root):
        self.root = root
        self.history = []  # 存储历史记录

        root.title(":)")
        root.geometry("400x160")  # 增大窗口大小以适应更大的历史记录框
        root.resizable(False, False)

        # 创建一个框架用于输入和历史记录
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=0, padx=10, pady=10)

        # 输入框1
        label1 = tk.Label(input_frame, text="Enter Log Name:")
        label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(input_frame)
        self.entry1.grid(row=1, column=0)

        # 输入框2
        label2 = tk.Label(input_frame, text="Enter Axis-Number:")
        label2.grid(row=2, column=0)
        self.entry2 = tk.Entry(input_frame)
        self.entry2.grid(row=3, column=0)

        # 按钮
        greet_button = tk.Button(input_frame, text="Go", width=15, height=1, command=self.on_button_click)  # 修改按钮大小
        greet_button.grid(row=4, column=0, pady=(10, 5))  # 增加下方的间距

        self.play_button = tk.Button(input_frame, text="Play", width=15, height=2, command=self.play_program)
        self.play_button.grid(row=5, column=0)
        self.play_button.grid_remove()

        # 结果标签
        self.result_label = tk.Label(input_frame, text="")
        self.result_label.grid(row=5, column=0)

        # 历史记录框架
        history_frame = tk.Frame(root)
        history_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # 历史记录标签
        self.history_label = tk.Label(history_frame, text="History:")
        self.history_label.pack()

        # 历史记录框
        self.history_listbox = tk.Listbox(history_frame, width=30, height=6)  # 修改宽度和高度
        self.history_listbox.pack()
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

    def on_button_click(self):
        file_name = self.entry1.get()
        base_path = "D:\\HuaweiMoveData\\Users\\12088\\Desktop\\数据\\"
        file_path = f"{base_path}{file_name}\\out_data.txt"

        axis_number = self.entry2.get()

        try:
            axis_number = int(axis_number)
        except ValueError:
            # self.result_label.config(text="Please enter a valid number for axis number.")
            # self.result_label.grid(row=0, column=0, padx=10, pady=10)
            return

        # 判断 axis_number
        if axis_number == 4 or axis_number == 3:
            process_data(file_path)
        else:
            process_data2(file_path)

        # 更新历史记录
        self.update_history(file_name, axis_number)

        self.play_button.grid()

    def play_program(self):
        print(1)

    def update_history(self, file_name, axis_number):
        # 将当前输入添加到历史记录
        entry = f"{file_name}, Axis: {axis_number}"
        self.history.append(entry)

        if len(self.history) > 6:
            self.history.pop(0)

        # 更新历史记录列表框
        self.history_listbox.delete(0, tk.END)  # 清空列表框
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def on_history_select(self, event):
        # 获取当前选择的历史记录
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_entry = self.history_listbox.get(selected_index)
            file_name, axis_number = selected_entry.split(", Axis: ")
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, file_name)
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, axis_number)

root = tk.Tk()
app = App(root)
root.mainloop()