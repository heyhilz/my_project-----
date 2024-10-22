# -*- coding: utf-8 -*-
import numpy as np

SYSTEM_AXES = 9

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
LOG_ERR_FORMAT_LENGTH = 1024
HINT_DISCRIPTION_LENGTH = 1024
ETHCAT_DATA_LENGTH = 256

base_path = '2024-09-18-14-50-44'

# 定义数据结构
class CF_LOG_PLAN:
    def __init__(self):
        self.sec = np.zeros(LOG_PLAN_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_PLAN_NUM, dtype=np.uint64)
        self.joint = np.zeros((SYSTEM_AXES, LOG_PLAN_NUM), dtype=np.float32)

class CF_LOG_ARGU:
    def __init__(self):
        self.sec = np.zeros(LOG_ARGU_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_ARGU_NUM, dtype=np.uint64)
        self.argu = np.zeros((20, LOG_ARGU_NUM), dtype=np.float32)

class CF_LOG_OUT:
    def __init__(self):
        self.sec = np.zeros(LOG_OUT_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_OUT_NUM, dtype=np.uint64)
        self.enco = np.zeros((SYSTEM_AXES, LOG_OUT_NUM), dtype=np.int32)
        self.joint = np.zeros((SYSTEM_AXES, LOG_OUT_NUM), dtype=np.float32)

class CF_LOG_IN:
    def __init__(self):
        self.sec = np.zeros(LOG_IN_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_IN_NUM, dtype=np.uint64)
        self.enci = np.zeros((SYSTEM_AXES, LOG_IN_NUM), dtype=np.int32)
        self.joint = np.zeros((SYSTEM_AXES, LOG_IN_NUM), dtype=np.float32)
        self.roll = np.zeros((SYSTEM_AXES, LOG_IN_NUM), dtype=np.int32)

class CF_LOG_KEY:
    def __init__(self):
        self.sec = np.zeros(LOG_KEY_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_KEY_NUM, dtype=np.uint64)
        self.key = np.zeros(LOG_KEY_NUM, dtype=np.int32)

class CF_LOG_CAN:
    def __init__(self):
        self.sec = np.zeros(LOG_CAN_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_CAN_NUM, dtype=np.uint64)
        self.shifttime = np.zeros(LOG_CAN_NUM, dtype=np.int32)

class CF_LOG_MD:
    def __init__(self):
        self.sec = np.zeros(LOG_MD_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_MD_NUM, dtype=np.uint64)
        self.enci_bef = np.zeros((SYSTEM_AXES, LOG_MD_NUM), dtype=np.int32)
        self.enci_aft = np.zeros((SYSTEM_AXES, LOG_MD_NUM), dtype=np.int32)
        self.roll = np.zeros((SYSTEM_AXES, LOG_MD_NUM), dtype=np.int32)
        self.awc_joint = np.zeros((SYSTEM_AXES, LOG_MD_NUM), dtype=np.float32)

class CF_LOG_APP_COMMU:
    def __init__(self):
        self.sec = np.zeros(LOG_APP_COMMU_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_APP_COMMU_NUM, dtype=np.uint64)
        self.type = np.zeros(LOG_APP_COMMU_NUM, dtype=np.int32)
        self.rev_buff = np.zeros((LOG_APP_COMMU_NUM, APP_COMMU_REV_LENGTH), dtype=np.uint8)

class CF_LOG_ERR:
    def __init__(self):
        self.sec = np.zeros(LOG_ERR_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_ERR_NUM, dtype=np.uint64)
        self.err_discription = np.zeros((LOG_ERR_NUM, ERR_DISCRIPTION_LENGTH), dtype='U1024')

class CF_LOG_HINT:
    def __init__(self):
        self.sec = np.zeros(LOG_HINT_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_HINT_NUM, dtype=np.uint64)
        self.hint_discription = np.zeros((LOG_HINT_NUM, HINT_DISCRIPTION_LENGTH), dtype='U1024')

class CF_LOG_ETHCAT:
    def __init__(self):
        self.sec = np.zeros(LOG_ETHCAT_NUM, dtype=np.uint64)
        self.nsec = np.zeros(LOG_ETHCAT_NUM, dtype=np.uint64)
        self.ethcat_data_flag = np.zeros(LOG_ETHCAT_NUM, dtype=np.int32)
        self.ethcat_string = np.zeros((LOG_ETHCAT_NUM, ETHCAT_DATA_LENGTH), dtype=np.uint8)

class CF_LOG:
    def __init__(self):
        self.plan_data = CF_LOG_PLAN()
        self.argu_data = CF_LOG_ARGU()
        self.in_data = CF_LOG_IN()
        self.out_data = CF_LOG_OUT()
        self.key_data = CF_LOG_KEY()
        self.can_data = CF_LOG_CAN()
        self.md_data = CF_LOG_MD()
        self.app_commu_data = CF_LOG_APP_COMMU()
        self.err_data = CF_LOG_ERR()
        self.hint_data = CF_LOG_HINT()
        self.ethcat_data = CF_LOG_ETHCAT()

class CF_LOG_1:
    def __init__(self):
        self.app_commu_data = CF_LOG_APP_COMMU()
        self.err_data = CF_LOG_ERR()

# 读取二进制文件
def read_binary_file(file_name, cf_log_data):
    try:
        with open(file_name, "rb") as fp:
            print(f"Reading binary file: {file_name}")
            # 读取CF_LOG数据
            fp.readinto(cf_log_data.plan_data.sec)
            fp.readinto(cf_log_data.plan_data.nsec)
            fp.readinto(cf_log_data.plan_data.joint)
            fp.readinto(cf_log_data.argu_data.sec)
            fp.readinto(cf_log_data.argu_data.nsec)
            fp.readinto(cf_log_data.argu_data.argu)
            fp.readinto(cf_log_data.in_data.sec)
            fp.readinto(cf_log_data.in_data.nsec)
            fp.readinto(cf_log_data.in_data.enci)
            fp.readinto(cf_log_data.in_data.joint)
            fp.readinto(cf_log_data.in_data.roll)
            fp.readinto(cf_log_data.out_data.sec)
            fp.readinto(cf_log_data.out_data.nsec)
            fp.readinto(cf_log_data.out_data.enco)
            fp.readinto(cf_log_data.out_data.joint)
            fp.readinto(cf_log_data.key_data.sec)
            fp.readinto(cf_log_data.key_data.nsec)
            fp.readinto(cf_log_data.key_data.key)
            fp.readinto(cf_log_data.can_data.sec)
            fp.readinto(cf_log_data.can_data.nsec)
            fp.readinto(cf_log_data.can_data.shifttime)
            fp.readinto(cf_log_data.md_data.sec)
            fp.readinto(cf_log_data.md_data.nsec)
            fp.readinto(cf_log_data.md_data.enci_bef)
            fp.readinto(cf_log_data.md_data.enci_aft)
            fp.readinto(cf_log_data.md_data.roll)
            fp.readinto(cf_log_data.md_data.awc_joint)
            fp.readinto(cf_log_data.app_commu_data.sec)
            fp.readinto(cf_log_data.app_commu_data.nsec)
            fp.readinto(cf_log_data.app_commu_data.type)
            fp.readinto(cf_log_data.app_commu_data.rev_buff)
            fp.readinto(cf_log_data.err_data.sec)
            fp.readinto(cf_log_data.err_data.nsec)
            fp.readinto(cf_log_data.err_data.err_discription)
            fp.readinto(cf_log_data.hint_data.sec)
            fp.readinto(cf_log_data.hint_data.nsec)
            fp.readinto(cf_log_data.hint_data.hint_discription)
            fp.readinto(cf_log_data.ethcat_data.sec)
            fp.readinto(cf_log_data.ethcat_data.nsec)
            fp.readinto(cf_log_data.ethcat_data.ethcat_data_flag)
            fp.readinto(cf_log_data.ethcat_data.ethcat_string)

        print(f"sizeof(CF_LOG) = {fp.tell()} bytes")
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")

# 读取二进制文件 CF_LOG_1
def read_binary_file_1(file_name, cf_log_data_1):
    try:
        with open(file_name, "rb") as fp:
            print(f"Reading binary file: {file_name}")
            # 读取CF_LOG_1数据
            fp.readinto(cf_log_data_1.app_commu_data.sec)
            fp.readinto(cf_log_data_1.app_commu_data.nsec)
            fp.readinto(cf_log_data_1.app_commu_data.type)
            fp.readinto(cf_log_data_1.app_commu_data.rev_buff)
            fp.readinto(cf_log_data_1.err_data.sec)
            fp.readinto(cf_log_data_1.err_data.nsec)
            fp.readinto(cf_log_data_1.err_data.err_discription)

        print(f"sizeof(CF_LOG_1) = {fp.tell()} bytes")
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")

# 写入文本文件
def write_to_text_file(filename, text_data):
    try:
        with open(filename, "w") as fp:
            for line in text_data:
                fp.write(line + '\n')
    except Exception as e:
        print(f"Cannot open {filename}: {e}")

# 处理日志数据
def process_log_data(cf_log_data):
    plan_text = []
    argu_text = []
    in_text = []
    out_text = []
    key_text = []
    md_text = []
    app_commu_text = []
    err_text = []
    hint_text = []
    ethcat_text = []

    for i in range(LOG_PLAN_NUM):
        time_d = cf_log_data.plan_data.sec[i] + cf_log_data.plan_data.nsec[i] * 0.000000001
        plan_line = f"time:{time_d:.9f};plan:joint0:{cf_log_data.plan_data.joint[0][i]:.6f},joint1:{cf_log_data.plan_data.joint[1][i]:.6f},joint2:{cf_log_data.plan_data.joint[2][i]:.6f},joint3:{cf_log_data.plan_data.joint[3][i]:.6f},joint4:{cf_log_data.plan_data.joint[4][i]:.6f},joint5:{cf_log_data.plan_data.joint[5][i]:.6f}"
        plan_text.append(plan_line)

    for i in range(LOG_ARGU_NUM):
        time_d = cf_log_data.argu_data.sec[i] + cf_log_data.argu_data.nsec[i] * 0.000000001
        argu_line = f"time:{time_d:.9f};argu0:{cf_log_data.argu_data.argu[0][i]:.6f},argu1:{cf_log_data.argu_data.argu[1][i]:.6f},argu2:{cf_log_data.argu_data.argu[2][i]:.6f},argu3:{cf_log_data.argu_data.argu[3][i]:.6f},argu4:{cf_log_data.argu_data.argu[4][i]:.6f},argu5:{cf_log_data.argu_data.argu[5][i]:.6f},argu6:{cf_log_data.argu_data.argu[6][i]:.6f},argu7:{cf_log_data.argu_data.argu[7][i]:.6f},argu8:{cf_log_data.argu_data.argu[8][i]:.6f}"
        argu_text.append(argu_line)

    for i in range(LOG_IN_NUM):
        time_d = cf_log_data.in_data.sec[i] + cf_log_data.in_data.nsec[i] * 0.000000001
        in_line = f"time:{time_d:.9f};enci0:{cf_log_data.in_data.enci[0][i]},joint0:{cf_log_data.in_data.joint[0][i]:.6f},roll0:{cf_log_data.in_data.roll[0][i]},enci1:{cf_log_data.in_data.enci[1][i]},joint1:{cf_log_data.in_data.joint[1][i]:.6f},roll1:{cf_log_data.in_data.roll[1][i]},enci2:{cf_log_data.in_data.enci[2][i]},joint2:{cf_log_data.in_data.joint[2][i]:.6f},roll2:{cf_log_data.in_data.roll[2][i]},enci3:{cf_log_data.in_data.enci[3][i]},joint3:{cf_log_data.in_data.joint[3][i]:.6f},roll3:{cf_log_data.in_data.roll[3][i]},enci4:{cf_log_data.in_data.enci[4][i]},joint4:{cf_log_data.in_data.joint[4][i]:.6f},roll4:{cf_log_data.in_data.roll[4][i]},enci5:{cf_log_data.in_data.enci[5][i]},joint5:{cf_log_data.in_data.joint[5][i]:.6f},roll5:{cf_log_data.in_data.roll[5][i]}"
        in_text.append(in_line)

    for i in range(LOG_OUT_NUM):
        time_d = cf_log_data.out_data.sec[i] + cf_log_data.out_data.nsec[i] * 0.000000001
        out_line = f"time:{time_d:.9f};enco0:{cf_log_data.out_data.enco[0][i]},joint0:{cf_log_data.out_data.joint[0][i]:.6f},enco1:{cf_log_data.out_data.enco[1][i]},joint1:{cf_log_data.out_data.joint[1][i]:.6f},enco2:{cf_log_data.out_data.enco[2][i]},joint2:{cf_log_data.out_data.joint[2][i]:.6f},enco3:{cf_log_data.out_data.enco[3][i]},joint3:{cf_log_data.out_data.joint[3][i]:.6f},enco4:{cf_log_data.out_data.enco[4][i]},joint4:{cf_log_data.out_data.joint[4][i]:.6f},enco5:{cf_log_data.out_data.enco[5][i]},joint5:{cf_log_data.out_data.joint[5][i]:.6f}"
        out_text.append(out_line)

    for i in range(LOG_KEY_NUM):
        time_d = cf_log_data.key_data.sec[i] + cf_log_data.key_data.nsec[i] * 0.000000001
        key_line = f"time:{time_d:.9f};{cf_log_data.key_data.key[i]}"
        key_text.append(key_line)

    for i in range(LOG_MD_NUM):
        time_d = cf_log_data.md_data.sec[i] + cf_log_data.md_data.nsec[i] * 0.000000001
        md_line = f"time:{time_d:.9f};md:enci_bef0:{cf_log_data.md_data.enci_bef[0][i]},enci_aft0:{cf_log_data.md_data.enci_aft[0][i]},roll0:{cf_log_data.md_data.roll[0][i]},awc_joint0:{cf_log_data.md_data.awc_joint[0][i]:.6f},enci_bef1:{cf_log_data.md_data.enci_bef[1][i]},enci_aft1:{cf_log_data.md_data.enci_aft[1][i]},roll1:{cf_log_data.md_data.roll[1][i]},awc_joint1:{cf_log_data.md_data.awc_joint[1][i]:.6f},enci_bef2:{cf_log_data.md_data.enci_bef[2][i]},enci_aft2:{cf_log_data.md_data.enci_aft[2][i]},roll2:{cf_log_data.md_data.roll[2][i]},awc_joint2:{cf_log_data.md_data.awc_joint[2][i]:.6f},enci_bef3:{cf_log_data.md_data.enci_bef[3][i]},enci_aft3:{cf_log_data.md_data.enci_aft[3][i]},roll3:{cf_log_data.md_data.roll[3][i]},awc_joint3:{cf_log_data.md_data.awc_joint[3][i]:.6f}"
        md_text.append(md_line)

    for i in range(LOG_APP_COMMU_NUM):
        time_d = cf_log_data.app_commu_data.sec[i] + cf_log_data.app_commu_data.nsec[i] * 0.000000001
        app_commu_line = f"time:{time_d:.9f};type:{cf_log_data.app_commu_data.type[i]},buff:{cf_log_data.app_commu_data.rev_buff[i].tobytes().decode('utf-8', 'ignore').strip()}"
        app_commu_text.append(app_commu_line)

    for i in range(LOG_ERR_NUM):
        time_d = cf_log_data.err_data.sec[i] + cf_log_data.err_data.nsec[i] * 0.000000001
        err_line = f"time:{time_d:.9f};err:{cf_log_data.err_data.err_discription[i]}"
        err_text.append(err_line)

    for i in range(LOG_HINT_NUM):
        time_d = cf_log_data.hint_data.sec[i] + cf_log_data.hint_data.nsec[i] * 0.000000001
        hint_line = f"time:{time_d:.9f};hint:{cf_log_data.hint_data.hint_discription[i]}"
        hint_text.append(hint_line)

    for i in range(LOG_ETHCAT_NUM):
        time_d = cf_log_data.ethcat_data.sec[i] + cf_log_data.ethcat_data.nsec[i] * 0.000000001
        ethcat_line = f"time:{time_d:.9f};"
        if cf_log_data.ethcat_data.ethcat_data_flag[i] == 1:
            ethcat_line += "send:"
        elif cf_log_data.ethcat_data.ethcat_data_flag[i] == 2:
            ethcat_line += "rece:"
        ethcat_line += ','.join([f"0x{byte:x}" for byte in cf_log_data.ethcat_data.ethcat_string[i]])
        ethcat_text.append(ethcat_line)

    return plan_text, argu_text, in_text, out_text, key_text, md_text, app_commu_text, err_text, hint_text, ethcat_text

if __name__ == "__main__":
    cf_log_data = CF_LOG()
    read_binary_file("2024-09-18-14-50-44\\my_log.log", cf_log_data)
    plan_text, argu_text, in_text, out_text, key_text, md_text, app_commu_text, err_text, hint_text, ethcat_text = process_log_data(cf_log_data)
    write_to_text_file("plan.txt", plan_text)
    write_to_text_file("argu.txt", argu_text)
    write_to_text_file("in.txt", in_text)
    write_to_text_file("out.txt", out_text)
    write_to_text_file("key.txt", key_text)
    write_to_text_file("md.txt", md_text)
    write_to_text_file("app_commu.txt", app_commu_text)
    write_to_text_file("err.txt", err_text)
    write_to_text_file("hint.txt", hint_text)
    write_to_text_file("ethcat.txt", ethcat_text)