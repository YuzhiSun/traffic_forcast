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


get_all_year_info()