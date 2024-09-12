import pandas as pd
import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

RAD_ANGLE = 180.0 / np.pi
arm_length = 225
ALL = 1

class SC_MOD:
    def __init__(self):
        self.d1 = 10
        self.d3 = 10
        self.d4 = 10
        self.d5 = 10
        self.L3 = 225
        self.L4 = 225
        self.L5 = 320
        self.Lm3 = 10
        self.Lm4 = 10
        self.Lm5 = 10
sc_mod = SC_MOD()

class TRANS:
    def __init__(self):
        self.n = np.zeros(3)
        self.o = np.zeros(3)
        self.a = np.zeros(3)
        self.p = np.zeros(3)

def create_transform_matrix(p1,p2,p3):
    t = TRANS()
    t.n[0] = p1[0]
    t.n[1] = p1[1]
    t.n[2] = p1[2]
    t.o[0] = p2[0]
    t.o[1] = p2[1]
    t.o[2] = p2[2]
    t.a = [0, 0, 1]
    t.p[0] = p3[0]
    t.p[1] = p3[1]
    t.p[2] = p3[2]
    return t

def mm_multi(t1, t2, choice):
    result = TRANS()

    result.n[0] = t1.n[0] * t2.n[0] + t1.o[0] * t2.n[1] + t1.a[0] * t2.n[2]
    result.n[1] = t1.n[1] * t2.n[0] + t1.o[1] * t2.n[1] + t1.a[1] * t2.n[2]
    result.n[2] = t1.n[2] * t2.n[0] + t1.o[2] * t2.n[1] + t1.a[2] * t2.n[2]

    result.o[0] = t1.n[0] * t2.o[0] + t1.o[0] * t2.o[1] + t1.a[0] * t2.o[2]
    result.o[1] = t1.n[1] * t2.o[0] + t1.o[1] * t2.o[1] + t1.a[1] * t2.o[2]
    result.o[2] = t1.n[2] * t2.o[0] + t1.o[2] * t2.o[1] + t1.a[2] * t2.o[2]

    result.a[0] = t1.n[0] * t2.a[0] + t1.o[0] * t2.a[1] + t1.a[0] * t2.a[2]
    result.a[1] = t1.n[1] * t2.a[0] + t1.o[1] * t2.a[1] + t1.a[1] * t2.a[2]
    result.a[2] = t1.n[2] * t2.a[0] + t1.o[2] * t2.a[1] + t1.a[2] * t2.a[2]

    if choice == 'ALL':
        result.p[0] = t1.n[0] * t2.p[0] + t1.o[0] * t2.p[1] + t1.a[0] * t2.p[2] + t1.p[0]
        result.p[1] = t1.n[1] * t2.p[0] + t1.o[1] * t2.p[1] + t1.a[1] * t2.p[2] + t1.p[1]
        result.p[2] = t1.n[2] * t2.p[0] + t1.o[2] * t2.p[1] + t1.a[2] * t2.p[2] + t1.p[2]

    return result

def EFEM3x_joint_to_jtin(joint):
    jtin = np.zeros(4)
    jtin[0] = joint[0]
    jtin[1] = joint[1]
    jtin[2] = np.arcsin(joint[2] / (2.0 * arm_length)) * RAD_ANGLE
    jtin[3] = joint[3]
    return jtin

def EFEM3x_joint_to_world(jtin):
    T01 = create_transform_matrix([1,0,0,],[0,1,0],[0,0,jtin[0]+sc_mod.d1])
    T12 = create_transform_matrix([np.cos(np.radians(jtin[1])), np.sin(np.radians(jtin[1])), 0],
                                  [-np.sin(np.radians(jtin[1])), np.cos(np.radians(jtin[1])), 0],
                                  [0, 0, 0])
    T23 = create_transform_matrix([np.cos(np.radians(jtin[2])), np.sin(np.radians(jtin[2])), 0],
                                  [-np.sin(np.radians(jtin[2])), np.cos(np.radians(jtin[2])), 0],
                                  [0, 0,sc_mod.d3])
    T34 = create_transform_matrix([np.cos(np.radians(180 - 2 * jtin[2])), np.sin(np.radians(180 - 2 * jtin[2])), 0],
                                  [-np.sin(np.radians(180 - 2 * jtin[2])), np.cos(np.radians(180 - 2 * jtin[2])), 0],
                                  [sc_mod.L3, 0, sc_mod.d4])
    T45 = create_transform_matrix([np.cos(np.radians(-90 + jtin[2])), np.sin(np.radians(-90 + jtin[2])), 0],
                                  [-np.sin(np.radians(-90 + jtin[2])), np.cos(np.radians(-90 + jtin[2])),0],
                                  [sc_mod.L4, 0, sc_mod.d5])
    T5E = create_transform_matrix([1, 0, 0],
                                  [0, 1, 0],
                                  [sc_mod.L5, 0, 0])

    Tmp1 = mm_multi(T01, T12, 'ALL')
    Tmp2 = mm_multi(Tmp1, T23, 'ALL')
    Tmp1 = mm_multi(Tmp2, T34, 'ALL')
    Tmp2 = mm_multi(Tmp1, T45, 'ALL')
    t = mm_multi(Tmp2, T5E, 'ALL')

    return t

def joint_to_world(joint):
    jtin = EFEM3x_joint_to_jtin(joint)
    t6 = EFEM3x_joint_to_world(jtin)
    return t6

def process_txt_file(file_path):
    df = pd.read_csv(file_path, sep=r'\s*:\s*|\s+|,|;', engine='python', header=None)
    return df

def process_data(file_path):
    file_name = os.path.basename(os.path.dirname(file_path))
    number = ''.join(filter(str.isdigit, file_name))
    output_file_path = f'D:\\HuaweiMoveData\\Users\\12088\\Desktop\\数据\\out_data_{number}.xlsx'

    data = process_txt_file(file_path)
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
        print(f"DATA WRITTEN TO {output_file_path} - Sheet1")

    z = data.iloc[:,5].to_numpy()
    t = data.iloc[:,9].to_numpy()
    r = data.iloc[:,13].to_numpy()
    x = data.iloc[:,17].to_numpy()
    joint = []
    xx = []
    yy = []
    zz = []
    for i in range(len(x)):
        index = i-1
        joint.append([z[index],t[index],r[index],x[index]])
        result = joint_to_world(joint[i])
        xx.append(result.p[0])
        yy.append(result.p[1])
        zz.append(result.p[2])

    vx = np.zeros(len(xx))
    vy = np.zeros(len(yy))
    vx[1:] = np.diff(xx)
    vy[1:] = np.diff(yy)

    data_second = {
        'x':xx,
        'y':yy,
        'z':zz,
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
    plt.axis('equal')  # 保持x和y的比例相�?
    plt.show()