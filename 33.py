import math
import matplotlib.pyplot as plt
import pandas as pd

def get_data():
    df = pd.read_excel('2024-07-31-16-33-25/out_data_20240731163325.xlsx',sheet_name='Sheet1') 
    angles = df.iloc[1:, 4].tolist()
    distances = df.iloc[1:, 6].tolist()
    return angles, distances

def calculate_trajectory(angle_degrees, distance):
    # 将角度转换为弧度
    angle_radians = math.radians(angle_degrees)
    
    # 手臂的初始长度
    arm_length = 156
    
    # 计算末端点的位置
    x = (arm_length + distance) * math.cos(angle_radians)
    y = (arm_length + distance) * math.sin(angle_radians)
    
    return x, y

def plot_trajectory(angles, distances):
    x_coords = []
    y_coords = []
    
    for angle, distance in zip(angles, distances):
        x, y = calculate_trajectory(angle, distance)
        x_coords.append(x)
        y_coords.append(y)
    
    plt.figure(figsize=(8, 8))
    plt.plot(x_coords, y_coords, marker='o')
    plt.title('Track')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.axis('equal')  # 保持比例一致
    plt.show()

angles ,distances = get_data()

plot_trajectory(angles, distances)
