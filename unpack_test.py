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

CF_LOG_PLAN_SIZE = (8 * LOG_PLAN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_PLAN_NUM)
CF_LOG_ARGU_SIZE = (8 * LOG_ARGU_NUM) * 2 + (4 * 20 * LOG_ARGU_NUM)
CF_LOG_OUT_SIZE = (8 * LOG_OUT_NUM) * 2 + (4 * SYSTEM_AXES * LOG_OUT_NUM * 2)
CF_LOG_IN_SIZE = (8 * LOG_IN_NUM) * 2 + (4 * SYSTEM_AXES * LOG_IN_NUM * 3)
CF_LOG_KEY_SIZE = (8 * LOG_KEY_NUM) * 2 + (4 * LOG_KEY_NUM)
CF_LOG_CAN_SIZE = (8 * LOG_CAN_NUM) * 2 + (8 * LOG_CAN_NUM)
CF_LOG_MD_SIZE = (8 * LOG_MD_NUM) * 2 + (4 * SYSTEM_AXES * LOG_MD_NUM * 4)
CF_LOG_APP_COMMU_SIZE = (8 * LOG_APP_COMMU_NUM) * 2 + (1 * LOG_APP_COMMU_NUM) + (APP_COMMU_REV_LENGTH * LOG_APP_COMMU_NUM)
CF_LOG_ERR_SIZE = (8 * LOG_ERR_NUM) * 2 + (ERR_DISCRIPTION_LENGTH * LOG_ERR_NUM)
CF_LOG_HINT_SIZE = (8 * LOG_HINT_NUM) * 2 + (HINT_DISCRIPTION_LENGTH * LOG_HINT_NUM)
CF_LOG_ETHCAT_SIZE = (8 * LOG_ETHCAT_NUM) * 2 + (1 * LOG_ETHCAT_NUM) + (ETHCAT_DATA_LENGTH * LOG_ETHCAT_NUM)

CF_LOG_SIZE = (
    CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_OUT_SIZE +
    CF_LOG_IN_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE +
    CF_LOG_MD_SIZE + CF_LOG_APP_COMMU_SIZE + CF_LOG_ERR_SIZE +
    CF_LOG_HINT_SIZE + CF_LOG_ETHCAT_SIZE
)

def parse_my_log(log_file_path):
    with open(log_file_path, 'rb') as log_file:
        while True:
            # ��ȡһ����С�����ݿ飨�����������֪�����ݿ�Ĵ�С��
            data_block = log_file.read()  # ����ÿ�ζ�ȡ 1024 �ֽ�
            
            # �����ȡ���ļ�ĩβ
            if not data_block:
                break
            
            # �������ݣ�����������ݽṹ��
            try:
                # �����һ��������һ������ֵ��4 �ֽڣ�
                first_value = struct.unpack('I', data_block[0:4])[0]
                print(f"Parsed value: {first_value}")

                # ���������������ݣ�����ʵ�ʽṹ������
                
            except struct.error as e:
                print(f"Error while unpacking data: {e}")
                break

# ʹ��ʾ��
log_file_path = "my_log.log"  # �����ʵ��·������
parse_my_log(log_file_path)
