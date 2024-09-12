# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class AnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Animation with Progress Bar')
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 9))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

        self.slider = QSlider()
        self.slider.setOrientation(1)  # Horizontal
        self.layout.addWidget(self.slider)

        self.button = QPushButton('Start Animation')
        self.button.clicked.connect(self.start_animation)
        self.layout.addWidget(self.button)

        self.file_path = 'D:\\HuaweiMoveData\\Users\\12088\\Desktop\\数据\\新建 XLSX 工作表5.xlsx'
        self.data = pd.read_excel(self.file_path)

        self.x = self.data.iloc[:, 0].dropna().to_numpy()
        self.y = self.data.iloc[:, 1].dropna().to_numpy()
        self.z = self.data.iloc[:, 2].dropna().to_numpy()

        self.scatter = self.ax1.scatter([], [], c='b', s=50, edgecolor='black', alpha=0.5, facecolor='none')
        self.line1, = self.ax1.plot([], [], 'bo-', lw=1, alpha=0.5)
        self.line2, = self.ax2.plot([], [], 'r-', lw=2)

        self.static_scatter1 = self.ax1.scatter(self.x, self.y, c='b', s=10, alpha=1.0)
        self.static_scatter2 = self.ax2.scatter(range(len(self.z)), self.z, c='r', s=10, alpha=1.0)

        self.ani = None
        self.animating = False
        self.current_frame = 0
        self.click = False

        self.init_plot()

    def init_plot(self):
        self.ax1.set_xlim(min(self.x) - 10, max(self.x) + 10)
        self.ax1.set_ylim(min(self.y) - 10, max(self.y) + 10)
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_title('XY Track')
        self.ax1.grid(True)

        self.ax2.set_xlim(0, len(self.z))
        self.ax2.set_ylim(min(self.z) - 10, max(self.z) + 10)
        self.ax2.set_xlabel('Index')
        self.ax2.set_ylabel('Z')
        self.ax2.set_title('Z Track')
        self.ax2.grid(True)

        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.x) - 1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.slider_update)

    def update(self, frame):
        self.current_frame = frame
        self.line1.set_data(self.x[:frame + 1], self.y[:frame + 1])
        offsets = np.array([self.x[:frame + 1], self.y[:frame + 1]]).T
        self.scatter.set_offsets(offsets)

        sizes = np.full(frame + 1, 50)
        sizes[-1] = 100
        colors = np.full(frame + 1, 'b')
        colors[-1] = 'r'
        self.scatter.set_edgecolor(colors)
        self.scatter.set_facecolor(colors)
        self.scatter.set_sizes(sizes)

        self.line2.set_data(range(frame + 1), self.z[:frame + 1])

        self.slider.blockSignals(True)
        self.slider.setValue(frame)
        self.slider.blockSignals(False)

        return self.scatter, self.line1, self.line2

    def start_animation(self):
        if not self.click:
            if self.static_scatter1 is not None:
                self.static_scatter1.remove()
                self.static_scatter2.remove()
                self.static_scatter1 = None
                self.static_scatter2 = None

            self.ani = animation.FuncAnimation(
                self.fig, self.update, frames=self.frame_generator(),
                init_func=self.init_plot, interval=20, blit=False, repeat=False
            )
            self.button.setText('Pause Animation')
            self.animating = True
            self.click = True
        else:
            if self.animating:
                if self.ani is not None:
                    self.ani.event_source.stop()
                self.button.setText('Start Animation')
                self.animating = False
            else:
                if self.ani is None:
                    self.ani = animation.FuncAnimation(
                        self.fig, self.update, frames=self.frame_generator(),
                        init_func=self.init_plot, interval=20, blit=False, repeat=False
                    )
                self.update(self.current_frame)  # Ensure it starts from current_frame
                self.ani.event_source.stop()  # Stop before starting
                self.ani.event_source.start()
                self.button.setText('Pause Animation')
                self.animating = True
        self.canvas.draw()

    def frame_generator(self):
        for frame in range(self.current_frame, len(self.x)):
            yield frame

    def slider_update(self):
        if self.ani is not None:
            self.ani.event_source.stop()
            self.animating = False
            self.button.setText('Start Animation')
        self.current_frame = self.slider.value()
        self.update(self.current_frame)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AnimationWindow()
    ex.show()
    sys.exit(app.exec_())
