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
# CF_LOG_CAN_SIZE = (8 * LOG_CAN_NUM) * 2 + (20 * LOG_CAN_NUM)#s ns can #FIXME:can
CF_LOG_CAN_SIZE = 6200000
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

def create_folder_and_file(folder_name, file_name):
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, file_name)
    return file_path

def parse_my_log(input_file):
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

    with open(input_file, 'rb') as infile:
        while True:
            # record = infile.read(CF_LOG_SIZE)
            record = infile.read()
            if not record:
                break  # 到达文件末尾
            
            print(f'cf log size:{CF_LOG_SIZE}')
            print(CF_LOG_PLAN_SIZE)
            print(CF_LOG_ARGU_SIZE)
            print(CF_LOG_IN_SIZE)
            print(CF_LOG_OUT_SIZE)
            print(CF_LOG_KEY_SIZE)
            print(CF_LOG_CAN_SIZE)
            offset = 0
            
            # 解析 plan 数据
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

            offset = CF_LOG_PLAN_SIZE

            # 解析 argu 数据
            argu_sec = struct.unpack_from('Q' * LOG_ARGU_NUM, record, offset)
            offset += 8 * LOG_ARGU_NUM
            argu_nsec = struct.unpack_from('Q' * LOG_ARGU_NUM, record, offset)
            offset += 8 * LOG_ARGU_NUM
            argu_data = []
            for _ in range(R_AXES + 1):
                argu_values = struct.unpack_from('f' * LOG_ARGU_NUM, record, offset)
                argu_data.append(argu_values)
                offset += 4 * LOG_ARGU_NUM
            log_data['argu'].append((argu_sec, argu_nsec, argu_data))
            
            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE

            # 解析 in 数据
            in_sec = struct.unpack_from('Q' * LOG_IN_NUM, record, offset)
            offset += 8 * LOG_IN_NUM
            in_nsec = struct.unpack_from('Q' * LOG_IN_NUM, record, offset)
            offset += 8 * LOG_IN_NUM
            in_encoders = []
            in_joints = []
            in_rolls = []
            for _ in range(SYSTEM_AXES):
                enci_data = struct.unpack_from('i' * LOG_IN_NUM, record, offset)
                in_encoders.append(enci_data)
                offset += 4 * LOG_IN_NUM
            for _ in range(SYSTEM_AXES):
                joint_data = struct.unpack_from('f' * LOG_IN_NUM, record, offset)
                in_joints.append(joint_data)
                offset += 4 * LOG_IN_NUM
            for _ in range(SYSTEM_AXES):
                roll_data = struct.unpack_from('i' * LOG_IN_NUM, record, offset)
                in_rolls.append(roll_data)
                offset += 4 * LOG_IN_NUM
            log_data['in'].append((in_sec, in_nsec, in_encoders, in_joints, in_rolls))

            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE

            # 解析 out 数据
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
            log_data['out'].append((out_sec, out_nsec, out_encoders, out_joints))

            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE

            # 解析 key 数据 && 不解析 can
            key_sec = struct.unpack_from('Q' * LOG_KEY_NUM, record, offset)
            offset += 8 * LOG_KEY_NUM
            key_nsec = struct.unpack_from('Q' * LOG_KEY_NUM, record, offset)
            offset += 8 * LOG_KEY_NUM
            keys = struct.unpack_from('i' * LOG_KEY_NUM, record, offset)
            log_data['key'].append((key_sec, key_nsec, keys))
            offset += 4 * LOG_KEY_NUM

            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE
                        
            # 解析 md 数据
            md_sec = struct.unpack_from('Q' * LOG_MD_NUM, record, offset)
            offset += 8 * LOG_MD_NUM
            md_nsec = struct.unpack_from('Q' * LOG_MD_NUM, record, offset)
            offset += 8 * LOG_MD_NUM
            md_encoders_bef = []
            md_encoders_aft = []
            md_awc_joint = []
            md_rolls = []
            for _ in range(SYSTEM_AXES):
                enci_bef_data = struct.unpack_from('i' * LOG_MD_NUM, record, offset)
                md_encoders_bef.append(enci_bef_data)
                offset += 4 * LOG_MD_NUM
            for _ in range(SYSTEM_AXES):
                enci_aft_data = struct.unpack_from('i' * LOG_MD_NUM, record, offset)
                md_encoders_aft.append(enci_aft_data)
                offset += 4 * LOG_MD_NUM
            for _ in range(SYSTEM_AXES):
                awc_joint_data = struct.unpack_from('f' * LOG_MD_NUM, record, offset)
                md_awc_joint.append(awc_joint_data)
                offset += 4 * LOG_MD_NUM
            for _ in range(SYSTEM_AXES):
                roll_data = struct.unpack_from('i' * LOG_MD_NUM, record, offset)
                md_rolls.append(roll_data)
                offset += 4 * LOG_MD_NUM
            log_data['md'].append((md_sec, md_nsec, md_encoders_bef, md_encoders_aft, md_awc_joint, md_rolls))
 
            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE + CF_LOG_MD_SIZE

            # 解析 app_commu 数据
            app_commu_sec = struct.unpack_from('Q' * LOG_APP_COMMU_NUM, record, offset)
            offset += 8 * LOG_APP_COMMU_NUM
            app_commu_nsec = struct.unpack_from('Q' * LOG_APP_COMMU_NUM, record, offset)
            offset += 8 * LOG_APP_COMMU_NUM
            app_types = struct.unpack_from('B' * LOG_APP_COMMU_NUM, record, offset)
            offset += LOG_APP_COMMU_NUM
            app_data = []
            for i in range(LOG_APP_COMMU_NUM):
                rev_buff = struct.unpack_from('c' * APP_COMMU_REV_LENGTH, record, offset)
                app_data.append(rev_buff)
                offset += APP_COMMU_REV_LENGTH
            log_data['app_commu'].append((app_commu_sec, app_commu_nsec, app_types, app_data))
 
            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE + CF_LOG_APP_COMMU_SIZE

            # 解析 err 数据
            err_sec = struct.unpack_from('Q' * LOG_ERR_NUM, record, offset)
            offset += 8 * LOG_ERR_NUM
            err_nsec = struct.unpack_from('Q' * LOG_ERR_NUM, record, offset)
            offset += 8 * LOG_ERR_NUM
            err_descriptions = []
            for _ in range(LOG_ERR_NUM):
                err_description = struct.unpack_from('c' * ERR_DISCRIPTION_LENGTH, record, offset)
                err_descriptions.append(err_description)
                offset += ERR_DISCRIPTION_LENGTH
            log_data['err'].append((err_sec, err_nsec, err_descriptions))

            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE + CF_LOG_APP_COMMU_SIZE + CF_LOG_ERR_SIZE

            # 解析 hint 数据
            hint_sec = struct.unpack_from('Q' * LOG_HINT_NUM, record, offset)
            offset += 8 * LOG_HINT_NUM
            hint_nsec = struct.unpack_from('Q' * LOG_HINT_NUM, record, offset)
            offset += 8 * LOG_HINT_NUM
            hint_descriptions = []
            for _ in range(LOG_HINT_NUM):
                hint_description = struct.unpack_from('c' * HINT_DISCRIPTION_LENGTH, record, offset)
                hint_descriptions.append(hint_description)
                offset += HINT_DISCRIPTION_LENGTH
            log_data['hint'].append((hint_sec, hint_nsec, hint_descriptions))

            offset = CF_LOG_PLAN_SIZE + CF_LOG_ARGU_SIZE + CF_LOG_IN_SIZE + CF_LOG_OUT_SIZE + CF_LOG_KEY_SIZE + CF_LOG_CAN_SIZE + CF_LOG_APP_COMMU_SIZE + CF_LOG_ERR_SIZE + CF_LOG_HINT_SIZE

            # 解析 ethcat 数据
            ethcat_sec = struct.unpack_from('Q' * LOG_ETHCAT_NUM, record, offset)
            offset += 8 * LOG_ETHCAT_NUM
            ethcat_nsec = struct.unpack_from('Q' * LOG_ETHCAT_NUM, record, offset)
            offset += 8 * LOG_ETHCAT_NUM
            ethcat_flags = struct.unpack_from('B' * LOG_ETHCAT_NUM, record, offset)
            offset += LOG_ETHCAT_NUM
            ethcat_strings = []
            for i in range(LOG_ETHCAT_NUM):
                ethcat_string = struct.unpack_from('B' * ETHCAT_DATA_LENGTH, record, offset)
                ethcat_strings.append(ethcat_string)
                offset += ETHCAT_DATA_LENGTH
            log_data['ethcat'].append((ethcat_sec, ethcat_nsec, ethcat_flags, ethcat_strings))

    return log_data

def write_txt(log_data, folder_name):
    for log_type, entries in log_data.items():
        output_file_path = os.path.join(base_path, f"{log_type}_data.txt")
        with open(output_file_path, 'w') as f:
            for entry in entries:
                if log_type == 'plan':
                    sec, nsec, plan_joint = entry
                    for k in range(LOG_PLAN_NUM):
                        joint_str = " ".join(f"joint{j}:{plan_joint[j][k]}" for j in range(R_AXES))
                        f.write(f"time:{sec[k]}.{nsec[k]}: {joint_str}\n")

                elif log_type == 'argu':
                    sec, nsec, argu_data = entry
                    for k in range(LOG_ARGU_NUM):
                        argu_str = " ".join(f"argu{j}:{argu_data[j][k]}" for j in range(R_AXES + 1))
                        f.write(f"time:{sec[k]}.{nsec[k]}: {argu_str}\n")

                elif log_type == 'out':
                    sec, nsec, out_encoders, out_joints = entry
                    for k in range(LOG_OUT_NUM):
                        encoder_joint_str = " ".join(f"enco{j}:{out_encoders[j][k]}, joint{j}:{out_joints[j][k]}" for j in range(R_AXES))
                        time = sec[k] + 0.000000001 * nsec[k]
                        f.write(f"time:{time}: {encoder_joint_str}\n")

                elif log_type == 'in':
                    sec, nsec, in_encoders, in_joints, in_rolls = entry
                    for k in range(LOG_IN_NUM):
                        in_data_str = " ".join(f"enci{j}:{in_encoders[j][k]}, joint{j}:{in_joints[j][k]}, roll{j}:{in_rolls[j][k]}" for j in range(R_AXES))
                        f.write(f"time:{sec[k]}.{nsec[k]}: {in_data_str}\n")

                elif log_type == 'key':
                    sec, nsec, keys = entry
                    for k in range(LOG_KEY_NUM):
                        f.write(f"time:{sec[k]}.{nsec[k]}: Key: {keys[k]}\n")

                elif log_type == 'can':
                    sec, nsec, can_messages = entry
                    for k in range(LOG_CAN_NUM):
                        f.write(f"time:{sec[k]}.{nsec[k]}: CAN Message: {can_messages[k]}\n")

                elif log_type == 'md':
                    sec, nsec, md_encoders_bef, md_encoders_aft, md_awc_joint, md_rolls = entry
                    for k in range(LOG_MD_NUM):
                        md_data_str = " ".join(f"Enci Bef {j}:{md_encoders_bef[j][k]}, Enci Aft {j}:{md_encoders_aft[j][k]}, AWC Joint {j}:{md_awc_joint[j][k]}, Roll {j}:{md_rolls[j][k]}" for j in range(SYSTEM_AXES))
                        f.write(f"time:{sec[k]}.{nsec[k]}: {md_data_str}\n")

                elif log_type == 'app_commu':
                    app_sec, app_nsec, app_types, app_data = entry
                    for k in range(LOG_APP_COMMU_NUM):
                        f.write(f"time:{app_sec[k]}.{app_nsec[k]}: Type: {app_types[k]}, Rev Data: {app_data[k]}\n")

                elif log_type == 'err':
                    sec, nsec, err_descriptions = entry
                    for k in range(LOG_ERR_NUM):
                        f.write(f"time:{sec[k]}.{nsec[k]}: Error Description: {err_descriptions[k]}\n")

                elif log_type == 'hint':
                    sec, nsec, hint_descriptions = entry
                    for k in range(LOG_HINT_NUM):
                        f.write(f"time:{sec[k]}.{nsec[k]}: Hint Description: {hint_descriptions[k]}\n")

                elif log_type == 'ethcat':
                    sec, nsec, ethcat_flags, ethcat_strings = entry
                    for k in range(LOG_ETHCAT_NUM):
                        f.write(f"time:{sec[k]}.{nsec[k]}: Flag: {ethcat_flags[k]}, String: {ethcat_strings[k]}\n")

if __name__ == "__main__":
    log_file_path = os.path.join(base_path, "my_log.log")

    log_data = parse_my_log(log_file_path)
    write_txt(log_data, base_path)