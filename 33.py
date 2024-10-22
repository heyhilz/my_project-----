import struct
import os

# Constants
SYSTEM_AXES = 9
LOG_PLAN_NUM = 1000
LOG_ARGU_NUM = 100
LOG_OUT_NUM = 20000
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

file_name = "my_log.log"
file_name_1 = "my_log_1.log"

class CF_LOG_PLAN:
    def __init__(self):
        self.sec = [0] * LOG_PLAN_NUM
        self.nsec = [0] * LOG_PLAN_NUM
        self.joint = [[0.0] * LOG_PLAN_NUM for _ in range(SYSTEM_AXES)]

class CF_LOG_ARGU:
    def __init__(self):
        self.sec = [0] * LOG_ARGU_NUM
        self.nsec = [0] * LOG_ARGU_NUM
        self.argu = [[0.0] * LOG_ARGU_NUM for _ in range(20)]

class CF_LOG_OUT:
    def __init__(self):
        self.sec = [0] * LOG_OUT_NUM
        self.nsec = [0] * LOG_OUT_NUM
        self.enco = [[0] * LOG_OUT_NUM for _ in range(SYSTEM_AXES)]
        self.joint = [[0.0] * LOG_OUT_NUM for _ in range(SYSTEM_AXES)]

class CF_LOG_IN:
    def __init__(self):
        self.sec = [0] * LOG_IN_NUM
        self.nsec = [0] * LOG_IN_NUM
        self.enci = [[0] * LOG_IN_NUM for _ in range(SYSTEM_AXES)]
        self.joint = [[0.0] * LOG_IN_NUM for _ in range(SYSTEM_AXES)]
        self.roll = [[0] * LOG_IN_NUM for _ in range(SYSTEM_AXES)]

class CF_LOG_KEY:
    def __init__(self):
        self.sec = [0] * LOG_KEY_NUM
        self.nsec = [0] * LOG_KEY_NUM
        self.key = [0] * LOG_KEY_NUM

class CF_LOG_CAN:
    def __init__(self):
        self.sec = [0] * LOG_CAN_NUM
        self.nsec = [0] * LOG_CAN_NUM
        self.shifttime = [0] * LOG_CAN_NUM

class CF_LOG_MD:
    def __init__(self):
        self.sec = [0] * LOG_MD_NUM
        self.nsec = [0] * LOG_MD_NUM
        self.enci_bef = [[0] * LOG_MD_NUM for _ in range(SYSTEM_AXES)]
        self.enci_aft = [[0] * LOG_MD_NUM for _ in range(SYSTEM_AXES)]
        self.roll = [[0] * LOG_MD_NUM for _ in range(SYSTEM_AXES)]
        self.awc_joint = [[0.0] * LOG_MD_NUM for _ in range(SYSTEM_AXES)]

class CF_LOG_APP_COMMU:
    def __init__(self):
        self.sec = [0] * LOG_APP_COMMU_NUM
        self.nsec = [0] * LOG_APP_COMMU_NUM
        self.type = [''] * LOG_APP_COMMU_NUM
        self.rev_buff = [[''] * APP_COMMU_REV_LENGTH for _ in range(LOG_APP_COMMU_NUM)]

class CF_LOG_ERR:
    def __init__(self):
        self.sec = [0] * LOG_ERR_NUM
        self.nsec = [0] * LOG_ERR_NUM
        self.err_discription = [[''] * ERR_DISCRIPTION_LENGTH for _ in range(LOG_ERR_NUM)]

class CF_LOG_HINT:
    def __init__(self):
        self.sec = [0] * LOG_HINT_NUM
        self.nsec = [0] * LOG_HINT_NUM
        self.hint_discription = [[''] * HINT_DISCRIPTION_LENGTH for _ in range(LOG_HINT_NUM)]

class CF_LOG_ETHCAT:
    def __init__(self):
        self.sec = [0] * LOG_ETHCAT_NUM
        self.nsec = [0] * LOG_ETHCAT_NUM
        self.ethcat_data_flag = [0] * LOG_ETHCAT_NUM
        self.ethcat_string = [[''] * ETHCAT_DATA_LENGTH for _ in range(LOG_ETHCAT_NUM)]

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

def read_log_file(file_name, log_type):
    log_data = log_type()

    with open(file_name, "rb") as f:
        if log_type == CF_LOG:
            for i in range(LOG_PLAN_NUM):
                log_data.plan_data.sec[i], log_data.plan_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.plan_data.joint[i] = list(struct.unpack(f"{SYSTEM_AXES}f", f.read(4 * SYSTEM_AXES)))
            
            for i in range(LOG_ARGU_NUM):
                log_data.argu_data.sec[i], log_data.argu_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.argu_data.argu[i] = list(struct.unpack("20f", f.read(4 * 20)))
            
            for i in range(LOG_IN_NUM):
                log_data.in_data.sec[i], log_data.in_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.in_data.enci[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
                log_data.in_data.joint[i] = list(struct.unpack(f"{SYSTEM_AXES}f", f.read(4 * SYSTEM_AXES)))
                log_data.in_data.roll[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
            
            for i in range(LOG_OUT_NUM):
                log_data.out_data.sec[i], log_data.out_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.out_data.enco[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
                log_data.out_data.joint[i] = list(struct.unpack(f"{SYSTEM_AXES}f", f.read(4 * SYSTEM_AXES)))
            
            for i in range(LOG_KEY_NUM):
                log_data.key_data.sec[i], log_data.key_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.key_data.key[i], = struct.unpack("i", f.read(4))
            
            for i in range(LOG_CAN_NUM):
                log_data.can_data.sec[i], log_data.can_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.can_data.shifttime[i], = struct.unpack("i", f.read(4))
            
            for i in range(LOG_MD_NUM):
                log_data.md_data.sec[i], log_data.md_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.md_data.enci_bef[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
                log_data.md_data.enci_aft[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
                log_data.md_data.roll[i] = list(struct.unpack(f"{SYSTEM_AXES}i", f.read(4 * SYSTEM_AXES)))
                log_data.md_data.awc_joint[i] = list(struct.unpack(f"{SYSTEM_AXES}f", f.read(4 * SYSTEM_AXES)))
            
            for i in range(LOG_APP_COMMU_NUM):
                log_data.app_commu_data.sec[i], log_data.app_commu_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.app_commu_data.type[i], = struct.unpack("c", f.read(1))
                log_data.app_commu_data.rev_buff[i] = list(struct.unpack(f"{APP_COMMU_REV_LENGTH}s", f.read(APP_COMMU_REV_LENGTH)))
            
            for i in range(LOG_ERR_NUM):
                log_data.err_data.sec[i], log_data.err_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.err_data.err_discription[i] = list(struct.unpack(f"{ERR_DISCRIPTION_LENGTH}s", f.read(ERR_DISCRIPTION_LENGTH)))
            
            for i in range(LOG_HINT_NUM):
                log_data.hint_data.sec[i], log_data.hint_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.hint_data.hint_discription[i] = list(struct.unpack(f"{HINT_DISCRIPTION_LENGTH}s", f.read(HINT_DISCRIPTION_LENGTH)))
            
            for i in range(LOG_ETHCAT_NUM):
                log_data.ethcat_data.sec[i], log_data.ethcat_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.ethcat_data.ethcat_data_flag[i], = struct.unpack("b", f.read(1))
                log_data.ethcat_data.ethcat_string[i] = list(struct.unpack(f"{ETHCAT_DATA_LENGTH}s", f.read(ETHCAT_DATA_LENGTH)))
        
        if log_type == CF_LOG_1:
            for i in range(LOG_APP_COMMU_NUM):
                log_data.app_commu_data.sec[i], log_data.app_commu_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.app_commu_data.type[i], = struct.unpack("c", f.read(1))
                log_data.app_commu_data.rev_buff[i] = list(struct.unpack(f"{APP_COMMU_REV_LENGTH}s", f.read(APP_COMMU_REV_LENGTH)))
            
            for i in range(LOG_ERR_NUM):
                log_data.err_data.sec[i], log_data.err_data.nsec[i] = struct.unpack("Q Q", f.read(16))
                log_data.err_data.err_discription[i] = list(struct.unpack(f"{ERR_DISCRIPTION_LENGTH}s", f.read(ERR_DISCRIPTION_LENGTH)))

    return log_data

def write_to_text_file(log_data):
    # Write plan data
    with open("plan_data.txt", "w") as f:
        for i in range(LOG_PLAN_NUM):
            time_d = log_data.plan_data.sec[i] + log_data.plan_data.nsec[i] * 0.000000001
            plan_text = f"time:{time_d:.9f};plan:joint0:{log_data.plan_data.joint[0][i]},joint1:{log_data.plan_data.joint[1][i]},joint2:{log_data.plan_data.joint[2][i]},joint3:{log_data.plan_data.joint[3][i]},joint4:{log_data.plan_data.joint[4][i]},joint5:{log_data.plan_data.joint[5][i]}\n"
            f.write(plan_text)

    # Write argu data
    with open("argu_data.txt", "w") as f:
        for i in range(LOG_ARGU_NUM):
            time_d = log_data.argu_data.sec[i] + log_data.argu_data.nsec[i] * 0.000000001
            argu_text = f"time:{time_d:.9f};argu0:{log_data.argu_data.argu[0][i]},argu1:{log_data.argu_data.argu[1][i]},argu2:{log_data.argu_data.argu[2][i]},argu3:{log_data.argu_data.argu[3][i]},argu4:{log_data.argu_data.argu[4][i]},argu5:{log_data.argu_data.argu[5][i]},argu6:{log_data.argu_data.argu[6][i]},argu7:{log_data.argu_data.argu[7][i]},argu8:{log_data.argu_data.argu[8][i]}\n"
            f.write(argu_text)

    # Write in data
    with open("in_data.txt", "w") as f:
        for i in range(LOG_IN_NUM):
            time_d = log_data.in_data.sec[i] + log_data.in_data.nsec[i] * 0.000000001
            in_text = f"time:{time_d:.9f};enci0:{log_data.in_data.enci[0][i]},joint0:{log_data.in_data.joint[0][i]},roll0:{log_data.in_data.roll[0][i]},enci1:{log_data.in_data.enci[1][i]},joint1:{log_data.in_data.joint[1][i]},roll1:{log_data.in_data.roll[1][i]},enci2:{log_data.in_data.enci[2][i]},joint2:{log_data.in_data.joint[2][i]},roll2:{log_data.in_data.roll[2][i]},enci3:{log_data.in_data.enci[3][i]},joint3:{log_data.in_data.joint[3][i]},roll3:{log_data.in_data.roll[3][i]},enci4:{log_data.in_data.enci[4][i]},joint4:{log_data.in_data.joint[4][i]},roll4:{log_data.in_data.roll[4][i]},enci5:{log_data.in_data.enci[5][i]},joint5:{log_data.in_data.joint[5][i]},roll5:{log_data.in_data.roll[5][i]}\n"
            f.write(in_text)

    # Write out data
    with open("out_data.txt", "w") as f:
        for i in range(LOG_OUT_NUM):
            time_d = log_data.out_data.sec[i] + log_data.out_data.nsec[i] * 0.000000001
            out_text = f"time:{time_d:.9f};enco0:{log_data.out_data.enco[0][i]},joint0:{log_data.out_data.joint[0][i]},enco1:{log_data.out_data.enco[1][i]},joint1:{log_data.out_data.joint[1][i]},enco2:{log_data.out_data.enco[2][i]},joint2:{log_data.out_data.joint[2][i]},enco3:{log_data.out_data.enco[3][i]},joint3:{log_data.out_data.joint[3][i]},enco4:{log_data.out_data.enco[4][i]},joint4:{log_data.out_data.joint[4][i]},enco5:{log_data.out_data.enco[5][i]},joint5:{log_data.out_data.joint[5][i]}\n"
            f.write(out_text)

    # Write key data
    with open("key_data.txt", "w") as f:
        for i in range(LOG_KEY_NUM):
            time_d = log_data.key_data.sec[i] + log_data.key_data.nsec[i] * 0.000000001
            key_text = f"time:{time_d:.9f};{log_data.key_data.key[i]}\n"
            f.write(key_text)

    # Write can data
    with open("can_data.txt", "w") as f:
        for i in range(LOG_CAN_NUM):
            time_d = log_data.can_data.sec[i] + log_data.can_data.nsec[i] * 0.000000001
            can_text = f"time:{time_d:.9f};shifttime:{log_data.can_data.shifttime[i]}\n"
            f.write(can_text)

    # Write md data
    with open("md_data.txt", "w") as f:
        for i in range(LOG_MD_NUM):
            time_d = log_data.md_data.sec[i] + log_data.md_data.nsec[i] * 0.000000001
            md_text = f"time:{time_d:.9f};md:enci_bef0:{log_data.md_data.enci_bef[0][i]},enci_aft0:{log_data.md_data.enci_aft[0][i]},roll0:{log_data.md_data.roll[0][i]},awc_joint0:{log_data.md_data.awc_joint[0][i]},enci_bef1:{log_data.md_data.enci_bef[1][i]},enci_aft1:{log_data.md_data.enci_aft[1][i]},roll1:{log_data.md_data.roll[1][i]},awc_joint1:{log_data.md_data.awc_joint[1][i]},enci_bef2:{log_data.md_data.enci_bef[2][i]},enci_aft2:{log_data.md_data.enci_aft[2][i]},roll2:{log_data.md_data.roll[2][i]},awc_joint2:{log_data.md_data.awc_joint[2][i]},enci_bef3:{log_data.md_data.enci_bef[3][i]},enci_aft3:{log_data.md_data.enci_aft[3][i]},roll3:{log_data.md_data.roll[3][i]},awc_joint3:{log_data.md_data.awc_joint[3][i]}\n"
            f.write(md_text)

    # Write app_commu data
    with open("app_commu_data.txt", "w") as f:
        for i in range(LOG_APP_COMMU_NUM):
            time_d = log_data.app_commu_data.sec[i] + log_data.app_commu_data.nsec[i] * 0.000000001
            app_commu_text = f"time:{time_d:.9f};type:{log_data.app_commu_data.type[i]},buff:{''.join(log_data.app_commu_data.rev_buff[i])}\n"
            f.write(app_commu_text)

    # Write err data
    with open("err_data.txt", "w") as f:
        for i in range(LOG_ERR_NUM):
            time_d = log_data.err_data.sec[i] + log_data.err_data.nsec[i] * 0.000000001
            err_text = f"time:{time_d:.9f};err:{''.join(log_data.err_data.err_discription[i])}\n"
            f.write(err_text)

    # Write hint data
    with open("hint_data.txt", "w") as f:
        for i in range(LOG_HINT_NUM):
            time_d = log_data.hint_data.sec[i] + log_data.hint_data.nsec[i] * 0.000000001
            hint_text = f"time:{time_d:.9f};hint:{''.join(log_data.hint_data.hint_discription[i])}\n"
            f.write(hint_text)

    # Write ethcat data
    with open("ethcat_data.txt", "w") as f:
        for i in range(LOG_ETHCAT_NUM):
            time_d = log_data.ethcat_data.sec[i] + log_data.ethcat_data.nsec[i] * 0.000000001
            ethcat_text = f"time:{time_d:.9f};flag:{log_data.ethcat_data.ethcat_data_flag[i]},data:{''.join(format(x, '#04x') for x in log_data.ethcat_data.ethcat_string[i])}\n"
            f.write(ethcat_text)

if __name__ == "__main__":
    # Read CF_LOG data
    cf_log_data = read_log_file(file_name, CF_LOG)
    write_to_text_file(cf_log_data)

    # Read CF_LOG_1 data
    cf_log_data_1 = read_log_file(file_name_1, CF_LOG_1)
    write_to_text_file(cf_log_data_1)
