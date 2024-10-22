# -*- coding: utf-8 -*-
import tkinter as tk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
from join import process_data
from joint2world_5axes import process_data2


class App:
    def __init__(self, root):
        self.root = root
        self.history = []  # 存储历史记录
        self.base_path = ""  # 存储当前�?�?

        root.title(":)")
        root.geometry("500x200")
        root.resizable(False, False)

        # 创建一�?框架用于输入
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 输入�?1
        label1 = tk.Label(input_frame, text="Enter Log Name:")
        label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(input_frame)
        self.entry1.grid(row=1, column=0)

        # 输入�?2
        label2 = tk.Label(input_frame, text="Enter Axis-Number:")
        label2.grid(row=2, column=0)
        self.entry2 = tk.Entry(input_frame)
        self.entry2.grid(row=3, column=0)

        # 按钮
        greet_button = tk.Button(input_frame, text="Go", width=15, height=1, command=self.on_button_click)
        greet_button.grid(row=4, column=0, pady=(0, 5))

        # 结果标�??
        self.result_label = tk.Label(input_frame, text="", fg="red")
        self.result_label.grid(row=5, column=0)

        # 设置拖放事件
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.on_file_drop)

        # 历史记录框架
        history_frame = tk.Frame(root)
        history_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # 历史记录标�??
        self.history_label = tk.Label(history_frame, text="History:")
        self.history_label.pack()

        # 历史记录�?
        self.history_listbox = tk.Listbox(history_frame, width=30, height=6)
        self.history_listbox.pack()
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

        # 设置列权�?
        root.grid_columnconfigure(0, weight=1)  # 输入框所在列
        root.grid_columnconfigure(1, weight=0)  # 历史记录�?

    def on_file_drop(self, event):
        # 获取拖拽文件的路�?
        file_path = event.data

        # 设置 base_path 为文件所在目�?
        self.base_path = os.path.dirname(file_path)
        print(self.base_path)

        # 获取文件名并更新输入�?
        file_name = os.path.basename(file_path)
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, file_name)

    def on_button_click(self):
        self.result_label.config(text="")

        file_name = self.entry1.get()
        file_path = os.path.join(self.base_path, file_name)
 
        axis_number = self.entry2.get()

        try:
            axis_number = int(axis_number)
        except ValueError:
            self.result_label.config(text="Check your axis number plz:/")
            return

        # 判断 axis_number
        if axis_number == 4 or axis_number == 3:
            process_data(file_path)
        else:
            process_data2(file_path)

        # 更新历史记录
        self.update_history(file_name, axis_number)

    def update_history(self, file_name, axis_number):
        # 将当前输入添加到历史记录
        entry = f"{file_name}, Axis: {axis_number}"
        self.history.append(entry)

        if len(self.history) > 6:
            self.history.pop(0)

        # 更新历史记录列表�?
        self.history_listbox.delete(0, tk.END)  # 清空列表�?
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def on_history_select(self, event):
        # 获取当前选择的历史�?�录
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_entry = self.history_listbox.get(selected_index)
            file_name, axis_number = selected_entry.split(", Axis: ")
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, file_name)
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, axis_number)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()
