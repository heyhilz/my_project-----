# -*- coding: utf-8 -*-
import struct
import os

# ����� CF_LOG �ṹ
SYSTEM_AXES = 6  # ������6���ؽ�

# �����ļ���
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
            # ����ÿ����¼�Ĵ�С�ǹ̶���
            record_size = 8 + 8 + SYSTEM_AXES * 4  # sec + nsec + joint data
            data = f.read(record_size)

            if not data:
                break  # EOF

            # ���� CF_LOG �ṹ��ȡ����
            sec, nsec = struct.unpack('Q Q', data[:16])  # ��ȡ sec �� nsec
            joints = struct.unpack(f'{SYSTEM_AXES}f', data[16:])  # ��ȡ�ؽ�����

            # ������Ӧ������
            plan_data.append(f"{sec}.{nsec} " + " ".join(map(str, joints)))
            argu_data.append(f"{sec}.{nsec} " + " ".join(map(str, joints)))

    return plan_data, argu_data

def write_to_file(data, file_name):
    with open(file_name, 'w') as f:
        for line in data:
            f.write(line + '\n')

def main():
    plan_data, argu_data = read_my_log(LOG_FILE)

    # д�뵽��Ӧ���ı��ļ�
    write_to_file(plan_data, PLAN_DATA_FILE)
    write_to_file(argu_data, ARGU_DATA_FILE)

    print(f"DATA WRITTEN TO {PLAN_DATA_FILE} AND {ARGU_DATA_FILE}.")

if __name__ == "__main__":
    main()
