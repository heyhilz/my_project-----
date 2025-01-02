from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation

# 读取Excel文件中Sheet2的数据，这里假设你的文件名为data.xlsx，根据实际情况修改文件名
data = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# 获取x坐标列、y坐标列和z坐标列的数据
x_coords = data.iloc[:, 0].values
y_coords = data.iloc[:, 1].values
z_coords = data.iloc[:, 2].values

# 创建3D图形和坐标轴对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 设置坐标轴范围等，可根据实际坐标数据范围调整
ax.set_xlim(np.min(x_coords) - 1, np.max(x_coords) + 1)
ax.set_ylim(np.min(y_coords) - 1, np.max(y_coords) + 1)
ax.set_zlim(np.min(z_coords) - 1, np.max(z_coords) + 1)

# 初始化一个点对象，用于后续更新显示
point, = ax.plot([], [], [], 'ro')

# 新增：用于存储历史轨迹的列表，每个元素是一个包含x、y、z坐标的元组
trajectory = []

# 初始化函数，用于设置动画开始时的画面
def init():
    point.set_data([], [])
    point.set_3d_properties([])
    return point,

# 更新函数，每一帧更新点的坐标位置，并记录历史轨迹
def update(frame):
    global trajectory
    x = np.array([x_coords[frame]])
    y = np.array([y_coords[frame]])
    z = np.array([z_coords[frame]])
    point.set_data(x, y)
    point.set_3d_properties(z)
    # 将当前坐标点添加到历史轨迹列表中
    trajectory.append((x[0], y[0], z[0]))
    # 绘制历史轨迹，将轨迹列表中的坐标点拆分成x、y、z的列表
    x_trajectory = [pos[0] for pos in trajectory]
    y_trajectory = [pos[1] for pos in trajectory]
    z_trajectory = [pos[2] for pos in trajectory]
    ax.plot(x_trajectory, y_trajectory, z_trajectory, 'b-', linewidth=1)
    return point,

# 创建动画对象，设置相关参数
ani = animation.FuncAnimation(fig, update, frames=len(x_coords), init_func=init, interval=200, blit=True)

# 展示动画
plt.show()