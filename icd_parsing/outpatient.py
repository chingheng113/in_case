import glob
import pandas as pd
import os
import re


def get_inx(ls, re_str):
    idx = [i for i, item in enumerate(ls) if re.search(re_str, item)]
    if len(idx) == 0:
        return -1
    return idx[0]


def parsing(patient_info_text):
    p_inf = {}
    patient_info_chunks = re.split('\s+', patient_info_text)
    if get_inx(patient_info_chunks, '健保') != -1:
        sex_age_inx = get_inx(patient_info_chunks, '健保') + 1
        sex_age = patient_info_chunks[sex_age_inx]
        p_inf['sex'] = sex_age[0]
        p_inf['age'] = sex_age[1:]

    if get_inx(patient_info_chunks, '療程\S+') != -1:
        id_inx = get_inx(patient_info_chunks, '療程\S+') + 2
        id = patient_info_chunks[id_inx]
        p_inf['id'] = id

    if get_inx(patient_info_chunks, '民國\S+') != -1:
        b_day_inx = get_inx(patient_info_chunks, '民國\S+')
        b_day = patient_info_chunks[b_day_inx]
        name_inx = b_day_inx - 1
        name = patient_info_chunks[name_inx]
        p_inf['name'] = name
        p_inf['b_day'] = b_day
    return p_inf

root_path = os.path.join('/Users/linc9/Desktop/ICD_10')
folder_list = glob.glob(os.path.join(root_path, '*'))

for f in folder_list:
    print(f)
    ocr_result = pd.read_csv(os.path.join(f, 'ocr_result.csv'))
    patient_info_text = ocr_result.loc[0]['text']
    p_dic = parsing(patient_info_text)
    print(p_dic)
    print('done')
