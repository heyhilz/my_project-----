# -*- coding: utf-8 -*-
import os
import struct

LOG_PLAN_NUM = 1000
LOG_ARGU_NUM = 100
LOG_OUT_NUM = 3000
LOG_IN_NUM = 10000
LOG_KEY_NUM = 1000
LOG_CAN_NUM = 310000
LOG_MD_NUM = 3000
LOG_APP_COMMU_NUM = 1000
LOG_ERR_NUM = 200
LOG_HINT_NUM = 500
LOG_ETHCAT_NUM = 10000

APP_COMMU_REV_LENGTH = 256
ERR_DISCRIPTION_LENGTH = 1024
HINT_DISCRIPTION_LENGTH = 1024
ETHCAT_DATA_LENGTH = 256

SYSTEM_AXES = 9 #4.6.89

R_AXES = 6
S_AXES = 3

CF_LOG_PLAN_SIZE = (8 * LOG_PLAN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_PLAN_NUM)#s ns joint
CF_LOG_ARGU_SIZE = (8 * LOG_ARGU_NUM) * 2 + (4 * 20 * LOG_ARGU_NUM)#s ns argu
CF_LOG_OUT_SIZE = (8 * LOG_OUT_NUM) * 2 + (4 * SYSTEM_AXES * LOG_OUT_NUM * 2)#s ns enco joint
CF_LOG_IN_SIZE = (8 * LOG_IN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_IN_NUM * 3)#s ns enci joint roll
CF_LOG_KEY_SIZE = (8 * LOG_KEY_NUM) * 2 + (4 * LOG_KEY_NUM)#s ns key
CF_LOG_CAN_SIZE = (8 * LOG_CAN_NUM) * 2 + (20 * LOG_CAN_NUM)#s ns can #FIXME:can
CF_LOG_MD_SIZE = (8 * LOG_MD_NUM) * 2 + (4 * SYSTEM_AXES * LOG_MD_NUM * 4)#s ns enci_bef enci_aft awc_joint roll
CF_LOG_APP_COMMU_SIZE = (8 * LOG_APP_COMMU_NUM) * 2 + (LOG_APP_COMMU_NUM) + (APP_COMMU_REV_LENGTH * LOG_APP_COMMU_NUM)#s ns type rev_buff
CF_LOG_ERR_SIZE = (8 * LOG_ERR_NUM) * 2 + (ERR_DISCRIPTION_LENGTH * LOG_ERR_NUM)#s ns err_dis
CF_LOG_HINT_SIZE = (8 * LOG_HINT_NUM) * 2 + (HINT_DISCRIPTION_LENGTH * LOG_HINT_NUM)#s ns hint_dis
CF_LOG_ETHCAT_SIZE = (8 * LOG_ETHCAT_NUM) * 2 + (LOG_ETHCAT_NUM) + (ETHCAT_DATA_LENGTH * LOG_ETHCAT_NUM)#s ns flag string

CF_LOG_SIZE = (
    CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_OUT_SIZE +
    CF_LOG_IN_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE +
    CF_LOG_MD_SIZE + CF_LOG_APP_COMMU_SIZE + CF_LOG_ERR_SIZE +
    CF_LOG_HINT_SIZE + CF_LOG_ETHCAT_SIZE
)

base_path = '2024-09-18-14-50-44'

input_file = '2024-09-18-14-50-44\\my_log.log'
output_file = '2024-09-18-14-50-44\\plan.txt'

log_data = {
        'plan': [],
        'argu': [],
        'out': [],
        'in': [],
        'key': [],
        'can': [],
        'md': [],
        'app_commu': [],
        'err': [],
        'hint': [],
        'ethcat': [],
    }

print(f'cf log size{CF_LOG_SIZE}')
print(f'cf plan log size{CF_LOG_PLAN_SIZE}')

with open(input_file, 'rb') as infile:
    while True:
        record = infile.read()
        print(len(record))
        if len(record) == 0:
            break  # 到达文件末尾

        offset = 0
        
        plan_sec = struct.unpack_from('Q' * LOG_PLAN_NUM, record, offset)
        offset += 8 * LOG_PLAN_NUM
        plan_nsec = struct.unpack_from('Q' * LOG_PLAN_NUM, record, offset)
        offset += 8 * LOG_PLAN_NUM
        plan_joint = []
        for _ in range(SYSTEM_AXES):
            joint_data = struct.unpack_from('f' * LOG_PLAN_NUM, record, offset)
            plan_joint.append(joint_data)
            offset += 4 * LOG_PLAN_NUM
        log_data['plan'].append((plan_sec, plan_nsec, plan_joint))

        print(f's{len(plan_sec)},ns{len(plan_nsec)},joint{len(plan_joint)}')
        # print(plan_sec)
        # print(plan_nsec)
        print(plan_joint)

        print(f"{plan_sec[0]}.{plan_nsec[0]}")
        # print(log_data['plan'][0])
        print(plan_joint[0][0])

