import pandas as pd


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

def make_train_dataset():
    # 首先列出选中要预测的22条道路
    select_road_id = [281897,281898,281899,282175,282176,282181,282182,
                      282183,282184,282185,282186,282697,282699,282701,
                      282791,282871,283055,283251,283260,283268,283269,283271]

    df = pd.read_csv('D:\\mxnetLearn\\traffic_forcast\\test_data\\01_01.csv', dtype='str', index_col=[0])
    filename_ = '01_01.csv'
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
        print('time_stack:',time_stack,'\n',df_slice,'\n','label:','\n',df_label,'\n')

    pass
make_train_dataset()
