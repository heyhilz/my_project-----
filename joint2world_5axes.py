import math
import pandas as pd
import os
import numpy as np
import matplotlib
# matplotlib.use('Qt5Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# file_path = 'D:\\HuaweiMoveData\\Users\\12088\\Desktop\\数据\\2024-09-04-09-02-44\\out_data.txt'

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class TRANS:
    def __init__(self):
        self.n = Vector3()
        self.o = Vector3()
        self.a = Vector3()
        self.p = Vector3()

def A2R(degree):
    return degree * (math.pi / 180)

def assign_joint_values_to_both_hands(joint_all):
    joint = np.zeros(5)
    joint[0] = joint_all[0]
    joint[1] = joint_all[1]
    joint[2] = joint_all[2]
    joint[3] = joint_all[4]
    joint[4] = 0.0

    # joint_aux[0] = joint_all[0]
    # joint_aux[1] = joint_all[1]
    # joint_aux[2] = joint_all[3]
    # joint_aux[3] = joint_all[4]
    # joint_aux[4] = 0.0

    return joint

def joint_to_world_d156_main(jt_value):
    t6 = TRANS()
    c2 = math.cos(A2R(jt_value[1]))
    s2 = math.sin(A2R(jt_value[1]))
    r = jt_value[2]

    t6.n.x = c2
    t6.n.y = s2
    t6.n.z = 0
    t6.o.x = -s2
    t6.o.y = c2
    t6.o.z = 0
    t6.a.x = 0
    t6.a.y = 0
    t6.a.z = 1
    t6.p.x = c2 * r
    t6.p.y = s2 * r
    t6.p.z = jt_value[0]

    return t6

def joint_to_world_d156_aux(jt_value):
    t6 = TRANS()
    c2 = math.cos(A2R(jt_value[1]))
    s2 = math.sin(A2R(jt_value[1]))
    rAux = jt_value[2]

    t6.n.x = c2
    t6.n.y = s2
    t6.n.z = 0
    t6.o.x = -s2
    t6.o.y = c2
    t6.o.z = 0
    t6.a.x = 0
    t6.a.y = 0
    t6.a.z = 1
    t6.p.x = c2 * rAux
    t6.p.y = s2 * rAux
    t6.p.z = jt_value[0]

    return t6

def process_txt_file(file_path):
    df = pd.read_csv(file_path, sep=r'\s*:\s*|\s+|,|;', engine='python', header=None)
    return df

def process_data2(path):
    file_name = os.path.basename(os.path.dirname(path))
    number = ''.join(filter(str.isdigit, file_name))
    output_file_path = f'D:\\HuaweiMoveData\\Users\\12088\\Desktop\\数据\\out_data_{number}.xlsx'
    data = process_txt_file(path)
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
        print(f"DATA WRITTEN TO {output_file_path} - Sheet1")

    z = data.iloc[:, 5].to_numpy()
    t = data.iloc[:, 9].to_numpy()
    r1 = data.iloc[:, 13].to_numpy()
    r2 = data.iloc[:, 17].to_numpy()
    x = data.iloc[:, 21].to_numpy()

    joint = []
    xx = []
    yy = []
    zz = []
    for i in range(len(x)):
        index = i - 1
        joint.append([z[index], t[index], r1[index], r2[index], x[index]])
        result = joint_to_world_d156_main(assign_joint_values_to_both_hands(joint[i]))
        xx.append(result.p.x)
        yy.append(result.p.y)
        zz.append(result.p.z)

    vx = np.zeros(len(xx))
    vy = np.zeros(len(yy))
    vx[1:] = np.diff(xx)
    vy[1:] = np.diff(yy)

    data_second = {
        'x': xx,
        'y': yy,
        'z': zz,
        'vx': vx,
        'vy': vy
    }

    df_second = pd.DataFrame(data_second)

    try:
        with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='a') as writer:
            df_second.to_excel(writer, index=False, sheet_name='Sheet2')
            print(f"DATA WRITTEN TO {output_file_path} - Sheet2")
    except Exception as e:
        print(f"Error writing data: {e}")

    plt.figure(figsize=(8, 8))
    plt.plot(xx, yy, marker='o', linestyle='-', color='b')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Track')
    plt.grid(True)
    plt.axis('equal')  # 保持x和y的比例相同
    plt.show()