import math
import pandas as pd
import os
import numpy as np
import matplotlib
# matplotlib.use('Qt5Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import struct

arm_lenth = 156

LOG_PLAN_NUM = 1000
LOG_ARGU_NUM = 100
LOG_OUT_NUM = 3000
LOG_IN_NUM = 10000

SYSTEM_AXES = 9
R_AXES = 6

CF_LOG_PLAN_SIZE = (8 * LOG_PLAN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_PLAN_NUM)
CF_LOG_ARGU_SIZE = (8 * LOG_ARGU_NUM) * 2 + (4 * 20 * LOG_ARGU_NUM)
CF_LOG_OUT_SIZE = (8 * LOG_OUT_NUM) * 2 + (4 * SYSTEM_AXES * LOG_OUT_NUM * 2)
CF_LOG_IN_SIZE = (8 * LOG_IN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_IN_NUM * 3)

offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE
LOG_SIZE = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE

log_name = 'my_log.log'

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
    return degree * (180 / math.pi)

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

def joint_to_world(joint):
    jtin = assign_joint_values_to_both_hands(joint)
    t6 = joint_to_world_d156_main(jtin)
    return t6

def data_to_dataframe(data):
    records = []
    for sec, nsec, encoders, joints in data:
        for i in range(LOG_OUT_NUM):
            time = sec[i] + 0.000000001 * nsec[i]  # 计算时间部分
            record = {
                'time': time
            }
            for axis in range(SYSTEM_AXES):
                record[f'enco_{axis}'] = encoders[axis][i]
                record[f'joint_{axis}'] = joints[axis][i]
            records.append(record)
    
    df = pd.DataFrame(records)
    return df

def process_data2(file_path):
    global offset

    file_name = os.path.basename(file_path)
    number = ''.join(filter(str.isdigit, file_name))
    output_xlsx_path = os.path.join(file_path, f"out_data_{number}.xlsx")

    log_file = os.path.join(file_path, log_name)
    
    data = []
    with open(log_file, 'rb') as log:
        while True:
            record = log.read()
            if not record:
                break
            
            out_sec = struct.unpack_from('Q' * LOG_OUT_NUM, record, offset)
            offset += 8 * LOG_OUT_NUM
            out_nsec = struct.unpack_from('Q' * LOG_OUT_NUM, record, offset)
            offset += 8 * LOG_OUT_NUM
            out_encoders = []
            out_joints = []
            for _ in range(SYSTEM_AXES):
                enco_data = struct.unpack_from('i' * LOG_OUT_NUM, record, offset)
                out_encoders.append(enco_data)
                offset += 4 * LOG_OUT_NUM
            for _ in range(SYSTEM_AXES):
                joint_data = struct.unpack_from('f' * LOG_OUT_NUM, record, offset)
                out_joints.append(joint_data)
                offset += 4 * LOG_OUT_NUM
            data.append((out_sec, out_nsec, out_encoders, out_joints))
    
    df = data_to_dataframe(data)

    z = df.iloc[:,2].to_numpy()
    t = df.iloc[:,4].to_numpy()
    r1 = df.iloc[:,6].to_numpy()
    r2 = df.iloc[:,8].to_numpy()
    x = df.iloc[:,10].to_numpy()

    joint = []
    xx = []
    yy = []
    zz = []
    for i in range(len(x)):
        index = i-1
        joint.append([z[index],t[index],r1[index],r2[index],x[index]])
        result = joint_to_world(joint[i])
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
        with pd.ExcelWriter(output_xlsx_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            df_second.to_excel(writer, index=False, sheet_name='Sheet2')
            print(f"DATA WRITTEN TO {output_xlsx_path}")
    except Exception as e:
        print(f"Error writing data: {e}")

    plt.figure(figsize=(8, 8))
    plt.plot(xx, yy, marker='o', linestyle='-', color='b')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Track')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
