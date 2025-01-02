import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

data = pd.read_excel('data.xlsx', sheet_name='Sheet2')

x_coords = data.iloc[:, 0].values
y_coords = data.iloc[:, 1].values

# 创建图形和坐标轴对象
fig, ax = plt.subplots()
# 设置坐标轴范围
ax.set_xlim(np.min(x_coords) - 1, np.max(x_coords) + 1)
ax.set_ylim(np.min(y_coords) - 1, np.max(y_coords) + 1)

# 初始化一个点对象，用于后续更新显示
point, = ax.plot([], [], 'ro')

# 新增：用于存储历史轨迹的列表，每个元素是一个包含x、y坐标的元组
trajectory = []

# 初始化函数，用于设置动画开始时的画面
def init():
    point.set_data([], [])
    return point,

# 更新函数，每一帧更新点的坐标位置，并记录历史轨迹，确保逐行绘制逻辑更严谨
def update(frame):
    global trajectory
    x = np.array([x_coords[frame]])
    y = np.array([y_coords[frame]])
    point.set_data(x, y)
    # 将当前坐标点添加到历史轨迹列表中
    trajectory.append((x[0], y[0]))  # 这里添加元组时取数组中的值，确保是单个数值组成的元组
    # 绘制历史轨迹，确保只有存在历史轨迹点时才进行绘制，避免空数据绘制报错
    if len(trajectory) > 1:
        x_trajectory = [pos[0] for pos in trajectory]
        y_trajectory = [pos[1] for pos in trajectory]
        ax.plot(x_trajectory, y_trajectory, 'b-', linewidth=1)
    return point,

# 创建动画对象，设置相关参数
ani = animation.FuncAnimation(fig, update, frames=len(x_coords), init_func=init, interval=200, blit=True)

# 展示动画
plt.show()