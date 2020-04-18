from math import radians, sin, cos, asin, sqrt

import pandas as pd
import re

# 计算坐标间距离
def geo_distance(geo_1,geo2):  #地理距离
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """

    lon1, lat1, lon2, lat2 = map(radians, map(float, [lon1, lat1, lon2, lat2]))  #根据提供的函数对指定序列做映，radians:将角度转换为弧度。
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r
print(geo_distance(111.5,36.08,121.47,31.23))  #我老家到上海的距离

#获取道路经纬度的列表
def obtain_lat_lon_list(txt_path='D:\\mxnetLearn\\traffic_forcast\\data\\boundary.txt'):
    txt_path = 'D:\\mxnetLearn\\traffic_forcast\\data\\boundary.txt'
    data = pd.read_csv(txt_path,dtype='str',engine='python',sep='\\t',encoding='utf-8')
    geom = data.iloc[68,2]  #提取出经纬度信息 data.loc[:0]['geom']是一个series 需要用下标将value取出
    # print(geom)
    # geom='MULTILINESTRING((108.93904 34.21174,108.93905 34.21152),(108.93905 34.21152,108.93906 34.21082),(108.93906 34.21082,108.93906 34.21074,108.93906 34.2106),'
    res = re.findall('[0-9]+\\.[0-9]+ [0-9]+\\.[0-9]+',geom)
    # res_count = re.split('[0-9]+\\.[0-9]+ [0-9]+\\.[0-9]+',geom)
    return res

# 将每条道路的长度分为50份 在这五十份中取重复度前十的aoi作为该道路的代表aoi
def cut_list(lat_lon_list):
    lst_len = len(lat_lon_list)
    interval_lst = lst_len//50
    if interval_lst <2:
        interval_lst=2
    # print(interval_lst)
    lst_cut = lat_lon_list[::interval_lst]
    # lst_cut_len = len(lst_cut)
    # print(lst_cut)
    return lst_cut

# 获取经纬度对应的aoi  参数为一个经纬度列表
def obtain_aoi_info(lat_lon_list):
    lst_res = []
    for lat_lon in lat_lon_list:
        lat_lon = re.sub(' ',',',lat_lon) #用‘,’替换空格
        lst_res.append(lat_lon)








# lat_lon_list = obtain_lat_lon_list()
# cut_list_res = cut_list(lat_lon_list)
# obtain_aoi_info(cut_list_res)

