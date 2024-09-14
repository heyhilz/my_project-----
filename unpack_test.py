# -*- coding: utf-8 -*-
import struct
import os

# 假设的 CF_LOG 结构
SYSTEM_AXES = 6  # 假设有6个关节

# 定义文件名
LOG_FILE = 'my_log.log'
PLAN_DATA_FILE = 'plan_data.txt'
ARGU_DATA_FILE = 'argu_data.txt'

def read_my_log(file_path):
    if not os.path.exists(file_path):
        print(f" {file_path} NOT exist!")
        return

    plan_data = []
    argu_data = []

    with open(file_path, 'rb') as f:
        while True:
            # 假设每条记录的大小是固定的
            record_size = 8 + 8 + SYSTEM_AXES * 4  # sec + nsec + joint data
            data = f.read(record_size)

            if not data:
                break  # EOF

            # 按照 CF_LOG 结构读取数据
            sec, nsec = struct.unpack('Q Q', data[:16])  # 读取 sec 和 nsec
            joints = struct.unpack(f'{SYSTEM_AXES}f', data[16:])  # 读取关节数据

            # 生成相应的数据
            plan_data.append(f"{sec}.{nsec} " + " ".join(map(str, joints)))
            argu_data.append(f"{sec}.{nsec} " + " ".join(map(str, joints)))

    return plan_data, argu_data

def write_to_file(data, file_name):
    with open(file_name, 'w') as f:
        for line in data:
            f.write(line + '\n')

def main():
    plan_data, argu_data = read_my_log(LOG_FILE)

    # 写入到相应的文本文件
    write_to_file(plan_data, PLAN_DATA_FILE)
    write_to_file(argu_data, ARGU_DATA_FILE)

    print(f"DATA WRITTEN TO {PLAN_DATA_FILE} AND {ARGU_DATA_FILE}.")

if __name__ == "__main__":
    main()
