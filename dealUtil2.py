import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
# 获取每个道路的全年交通信息
def get_all_year_info():
    # 获取全部道路的信息


    # 获取选定道路的id
    road_data = pd.read_csv('D:\mxnetLearn\\traffic_forcast\\data\\selected_road1.csv',
                       dtype='str', sep=',', names=['road_id', 'info', 'end'])
    road_ids = road_data['road_id'].values

    for i in range(0,len(road_ids)):
        road_id = road_ids[i]
        print(road_id)
        # 获取全部道路的信息
        df_temp = pd.DataFrame(columns=['road_id', 'date', 'tti', 'speed'])
        data_reader = pd.read_csv('D:\\mxnetLearn\\traffic_forcast\\data\\chengdushi.txt',
                                  dtype='str', sep=',', chunksize=2000000,
                                  names=['road_id', 'date', 'tti', 'speed'])
        for data in data_reader:
            res = data[data['road_id'].isin([road_id])]
            df_temp = df_temp.append(res)

            df_temp = df_temp.reset_index(drop=True)
        print(df_temp)
        road_info_path ='D:\\mxnetLearn\\traffic_forcast\\selected_road_info\\' + road_id + '.csv'
        df_temp.to_csv(road_info_path)
# get_all_year_info()
#分割原始数据  生成用于训练的数据集

# 将dataframe格式数据转换成灰度图片
def df_to_imgarr(df):
    df = (df - df.min()) / (df.max() - df.min())    #  归一化
    img_array = df.values
    return img_array

# 将list写入csv文件
def lst_to_csv(name,lst,lst_path):
    temp = pd.DataFrame(columns=name, data=lst)
    temp.to_csv(lst_path,index=False)

# lst = [[1,(11,11,11)],
#        [2,(22,22,22)]]
# name = ['date_id','label']
# lst_path = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\lst_to_csv.csv'
# lst_to_csv(name=name,lst=lst,lst_path=lst_path)
# lst_df = pd.read_csv('D:\\mxnetLearn\\traffic_forcast\\test_data\\lst_to_csv.csv')
# lst_df['label']



def make_train_dataset(label_lst,day_path,filename_ = '01_01.csv',
                       store_path='D:\\mxnetLearn\\traffic_forcast\\test_data\\train_data\\'):

    # 该函数用来分割一天的原始数据，将其划分为114个子图片然后对应存储每个图片的内容和标签，分别存到img和label文件中
    # 首先列出选中要预测的22条道路
    select_road_id = [281897,281898,281899,282175,282176,282181,282182,
                      282183,282184,282185,282186,282697,282699,282701,
                      282791,282871,283055,283251,283260,283268,283269,283271]

    df = pd.read_csv(day_path, index_col=[0])

    # 获取要预测的道路的信息
    df_sel = df.loc[select_road_id]
    # print(df_sel)

    #切割文件一天切割成114份，每份是五小时的
    interval_ = 30     #  时间间隔  30个十分钟  也就是  五小时
    for start_time in range(0,114):
        end_time = start_time + interval_
        hr = (end_time * 10 // 60)   #  推算小时
        if hr < 10 :
            hr = '0' + str(hr)
        else:
            hr = str(hr)
        min = end_time * 10 - int(hr) * 60   #推算分钟
        if min < 10:
            min = '00'

        time_stack = hr + '-' + str(min)  #  构造时间戳  以便于生成文件名

        df_slice = df.iloc[:,start_time:end_time]  #  用作生成图片的数据
        pre_time = end_time + 1
        df_label = df_sel.iloc[:,end_time:pre_time]   # 用作标签的数据
        # print('time_stack:',time_stack,'\n',df_slice,'\n','label:','\n',df_label,'\n')

        im_array = df_to_imgarr(df_slice)
        day = filename_.split('.')[0]
        img_path = store_path + 'img\\' + day +'_'+ time_stack + '.png'      #  月 日 小时 分
        label_path = store_path + 'label\\' + day  +'_'+ time_stack + '.csv'
        id_str = day  +'_'+ time_stack
        mpimg.imsave(img_path,im_array,cmap='cool')   # 存入图片训练数据
        df_label.to_csv(label_path)                   # 存入标签数据

        label_lst.append(id_str)                      # 存入条目  在做训练的时候，通过访问该文件获取标签和图片路径

        # print(time_stack,'is OK!')
def make_valid_dataset(label_lst,day_path,filename_ = '01_01.csv',
                       store_path='D:\\mxnetLearn\\traffic_forcast\\test_data\\valid_data\\',
                       valid_ratio=0.1):
    n_ten_mintus = int(114 * valid_ratio)    #  每隔n_ten_minutes取一个

    # 该函数用来分割一天的原始数据，将其划分为114个子图片然后对应存储每个图片的内容和标签，分别存到img和label文件中
    # 首先列出选中要预测的22条道路
    select_road_id = [281897,281898,281899,282175,282176,282181,282182,
                      282183,282184,282185,282186,282697,282699,282701,
                      282791,282871,283055,283251,283260,283268,283269,283271]

    df = pd.read_csv(day_path, index_col=[0])

    # 获取要预测的道路的信息
    df_sel = df.loc[select_road_id]
    # print(df_sel)

    #切割文件一天切割成11份，每份是五小时的
    interval_ = 30     #  时间间隔  30个十分钟  也就是  五小时
    for start_time in range(0,114,n_ten_mintus):
        end_time = start_time + interval_
        hr = (end_time * 10 // 60)   #  推算小时
        if hr < 10 :
            hr = '0' + str(hr)
        else:
            hr = str(hr)
        min = end_time * 10 - int(hr) * 60   #推算分钟
        if min < 10:
            min = '00'

        time_stack = hr + '-' + str(min)  #  构造时间戳  以便于生成文件名

        df_slice = df.iloc[:,start_time:end_time]  #  用作生成图片的数据
        pre_time = end_time + 1
        df_label = df_sel.iloc[:,end_time:pre_time]   # 用作标签的数据
        # print('time_stack:',time_stack,'\n',df_slice,'\n','label:','\n',df_label,'\n')

        im_array = df_to_imgarr(df_slice)
        day = filename_.split('.')[0]
        img_path = store_path + 'img\\' + day +'_'+ time_stack + '.png'      #  月 日 小时 分
        label_path = store_path + 'label\\' + day  +'_'+ time_stack + '.csv'
        id_str = day  +'_'+ time_stack
        mpimg.imsave(img_path,im_array,cmap='cool')   # 存入图片训练数据
        df_label.to_csv(label_path)                   # 存入标签数据

        label_lst.append(id_str)                      # 存入条目  在做训练的时候，通过访问该文件获取标签和图片路径
    print(label_lst)
        # print(time_stack,'is OK!')
# 构造测试用的验证集
# label_lst = []
# day_path = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\01_01.csv'
# make_valid_dataset(label_lst,day_path)
# name = ['name']
# label_path = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\valid_data\\label_lst.csv'
# lst_to_csv(name,label_lst,label_path)
def make_all_train_dataset():
    #构建全年的数据集
    root_path = 'D:\\mxnetLearn\\traffic_forcast\\tti_table\\table\\'    #  根目录
    filenames = os.listdir(root_path) #  寻找该目录下所有的原始数据
    store_path = '/traffic_forcast/train_valid_data/train_data\\'
    label_lst = []
    for filename in filenames:
        print(filename)
        day_path = root_path + filename
        make_train_dataset(label_lst,day_path,filename,store_path)
        print(label_lst)
    name = ['name']
    # lst_to_csv(name,label_lst,'D:\\mxnetLearn\\traffic_forcast\\train_data\\label_lst.csv')
    label_path = store_path + 'label_lst.csv'
    lst_to_csv(name, label_lst, label_path)
def make_all_valid_dataset():
    #构建验证数据集 验证比率 0.1
    valid_ratio = 0.1
    root_path = 'D:\\mxnetLearn\\traffic_forcast\\tti_table\\table\\'    #  根目录
    filenames = os.listdir(root_path) #  寻找该目录下所有的原始数据
    store_path = 'D:\\mxnetLearn\\traffic_forcast\\train_valid_data\\valid_data\\'
    label_lst = []
    all_num = len(filenames)
    n_train_per_valid = int(all_num * valid_ratio)   #每隔n_train_per_valid 取一个

    for filename in filenames[::n_train_per_valid]:
        print(filename)
        day_path = root_path + filename
        make_valid_dataset(label_lst,day_path,filename,store_path,valid_ratio)
        # print(label_lst)
    name = ['name']
    label_path = store_path + 'label_lst.csv'
    lst_to_csv(name,label_lst,label_path)


# 构造全部的验证集
# make_all_valid_dataset()





# start_time = time.time()
# make_all_train_dataset()
# end_time = time.time()
# print('total:',end_time-start_time,'s')