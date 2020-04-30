# 处理各种数据的方法
import pandas as pd
from os import listdir
#统计各条道路的tti的最值
def obtain_max_min_tti(path='D:\\mxnetLearn\\traffic_forcast\\data\\chengdushi.txt'):
    max_min_DF = pd.DataFrame(columns=['road_id','max_tti','min_tti'])
    data_reader = pd.read_csv(path, dtype='str',sep=',',chunksize=240000,
                              names=['road_id','date','tti','speed','max_tti','min_tti','max-min'])
    i = 100
    for data in data_reader:
        for index,row in data.iterrows():
            #判断在max_min_DF中是否已经存了当前的road_id
            bool_res = max_min_DF[max_min_DF['road_id'].isin([row['road_id']])].empty
            if bool_res == False:
                road_id_tmp = row['road_id']
                tti_new_tmp = row['tti']
                tti_max = max_min_DF[(max_min_DF['road_id'] == road_id_tmp)]['max_tti'].values[0]
                tti_min = max_min_DF[(max_min_DF['road_id'] == road_id_tmp)]['min_tti'].values[0]
                tti_max = float(tti_max)
                tti_min = float(tti_min)
                tti_new_tmp = float(tti_new_tmp)
                if tti_new_tmp < tti_min:
                    line_index = max_min_DF[(max_min_DF['road_id'] == road_id_tmp)]['min_tti'].index
                    max_min_DF.loc[line_index, 'min_tti'] = tti_new_tmp
                elif tti_new_tmp > tti_max:
                    line_index = max_min_DF[(max_min_DF['road_id'] == road_id_tmp)]['max_tti'].index
                    max_min_DF.loc[line_index, 'max_tti'] = tti_new_tmp


            else :
                road_id_tmp = row['road_id']
                max_tmp = row['tti']
                min_tmp = row['tti']
                tmp_df = pd.DataFrame({'road_id': road_id_tmp,
                                       'max_tti': max_tmp,
                                       'min_tti': min_tmp}, index=[0])
                max_min_DF = max_min_DF.append(tmp_df, ignore_index=True)
        for index, line in max_min_DF.iterrows():
            max_min_DF.loc[index,'max-min']=float(line['max_tti']) - float(line['min_tti'])
        print(max_min_DF)
        i = i+1
        csv_str = 'max_min_tti' + str(i) + '.csv'

        max_min_DF.to_csv(csv_str)
    max_min_DF.to_csv('all_max_min_tti.csv')

# obtain_max_min_tti()
def parse_date():
# 解析日期格式   将日期列转化为多个列 例如  2018-01-01 00:23:33  解析为六列 分别为 年月日 时分秒

    # 存所有道路信息的文件路径
    root_path = 'D:\\mxnetLearn\\traffic_forcast\\selected_road_info'

    dir_list = listdir(root_path)
    for path_ in dir_list:
        path_piece = root_path + '\\'+ path_
        print(path_)
        data_origin = pd.read_csv(path_piece,
                                  dtype='str', sep=',',
                                  names=['idx','road_id', 'date', 'tti', 'speed','year','month','day','hour','minutes'])
        data = data_origin.iloc[1:,1:]

        for i in range(1,len(data)+1):
            try:
                line = data.loc[i,'date']
            except:
                print('第',i,'行，date 列 异常')
                continue

            date, time = line.split(' ')
            year, month, day = date.split('-')
            hr, mints, sec = time.split(':')
            data.loc[i, 'year'] = year
            data.loc[i, 'month'] = month
            data.loc[i, 'day'] = day
            data.loc[i, 'hour'] = hr
            data.loc[i, 'minutes'] = mints
        aim_path = 'D:\\mxnetLearn\\traffic_forcast\\selected_road_parse_info\\' + path_
        data.to_csv(aim_path, index=False)
# parse_date()
def make_time_lst():
    #  生成小时和时间list  构造时间索引
    hour_ = ''
    minutes_ = ''
    hour_lst = []
    minutes_lst = []
    time_lst = []
    for i in range(0, 24):
        if i < 10:
            hour_temp = '0' + str(i)
            hour_ = hour_temp
            hour_lst.append(hour_)
            if i < 6:
                minutes_ = str(i) + '0'
                minutes_lst.append(minutes_)
            continue
        hour_ = str(i)
        hour_lst.append(hour_)
    # print(hour_lst, '\n', minutes_lst)
    for hr in hour_lst:
        for mints in minutes_lst:
            time_temp = hr + '-' +mints
            time_lst.append(time_temp)
    # print(time_lst)
    return time_lst
# make_time_lst()

def obtain_roadfile_list():
    #生成想要的道路排列顺序
    root_path = 'D:\\mxnetLearn\\traffic_forcast\\selected_road_parse_info'
    dir_list = listdir(root_path)
    road_id_lst = []
    path_lst = []
    for path_ in dir_list:
        road_id = path_.split('.')[0]
        road_id_lst.append(road_id)
        path_piece = root_path + '\\' + path_
        path_lst.append(path_piece)
    return road_id_lst, path_lst
def make_info_table(month='01',day='01',road_id_lst = [],path_lst = []):
    # 将选取的道路信息汇总到一个表中，一天为一个文件
    # 获取时间索引
    time_cols = make_time_lst()
    error_list = []
    # 获取文件内容
    # root_path = 'D:\\mxnetLearn\\traffic_forcast\\selected_road_parse_info'
    # dir_list = listdir(root_path)
    # road_id_lst = []
    # path_lst = []

    # 生成 道路id列表和道路信息文件路径列表
    # for path_ in dir_list:
    #     road_id = path_.split('.')[0]
    #     road_id_lst.append(road_id)
    #     path_piece = root_path + '\\' + path_
    #     path_lst.append(path_piece)
    # print(road_id_lst ,'\n' , path_lst)
    df = pd.DataFrame(columns=time_cols,index=road_id_lst)
    for road_file_path in path_lst:
        # 开始试验
        data_origin = pd.read_csv(road_file_path, dtype='str')
        # print(data_origin)
        for time_ in time_cols:
            hr_tmp , min_tmp = time_.split('-')
            col_tmp = time_ #时间索引
            road_id_tmp = data_origin.at[0,'road_id']
            # print(road_id_tmp,':',time_)
            try:
                tti_tmp = data_origin[(data_origin['hour']==hr_tmp)
                                 & (data_origin['minutes']==min_tmp)
                                 & (data_origin['month']==month)
                                 & (data_origin['day']==day)]['tti'].values[0]

            except:
                error_info = 'error:'+ road_id_tmp + '['+ month + '-' + \
                             day + '-' + hr_tmp + '-' + min_tmp + ']' + '\n'
                error_list.append(error_info)
                # print(error_info)
                df.at[road_id_tmp, col_tmp] = '1.000'
                continue
            df.at[road_id_tmp, col_tmp] = tti_tmp
    print(df)
        #结束试验
    error_df = pd.DataFrame(error_list)


    error_path = 'D:\\mxnetLearn\\traffic_forcast\\tti_table\\error\\' + month +'_' + day + '.csv'
    error_df.to_csv(error_path)
    tti_table_path = 'D:\\mxnetLearn\\traffic_forcast\\tti_table\\table\\' + month +'_' + day + '.csv'
    df.to_csv(tti_table_path)
    # print(df)

    pass
# make_info_table()

def produce_month_days():
    #该函数用来生成一年中的月和日
    data_df = pd.read_csv('D:\\mxnetLearn\\traffic_forcast\\test_data\\281897.csv',dtype='str')
    # print(data_df)
    df_tmp = pd.DataFrame(columns=['month-day'])
    df_tmp = data_df['month'] +'-' + data_df['day']   # 合并两列
    df_tmp.drop_duplicates(inplace=True)  # 去重
    mon_day = df_tmp.values   #得到想要的日期
    return mon_day
# produce_month_days()
def make_whole_year_road_info():
    #生成全年的选中道路的tti表
    road_id_lst, path_lst = obtain_roadfile_list()    #获取到道路罗列顺序列表
    month_days = produce_month_days()    #获取月日列表
    month_, day_ = '' ,''
    # 开始进行遍历所有日期下的所有道路的各个时段tti信息
    for month_day in month_days:
        month_, day_ = month_day.split('-')
        print(month_day)
        make_info_table(month=month_,day=day_,road_id_lst=road_id_lst,path_lst=path_lst)

make_whole_year_road_info()

#


pass

