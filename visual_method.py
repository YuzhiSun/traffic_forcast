import pandas as pd
import matplotlib.pyplot as plt
from mxnet import nd
from matplotlib.pyplot import MultipleLocator


plt.style.use('seaborn-white')
import numpy as np
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
# 记录各种可视化方法
np.set_printoptions(suppress=True)
time_label_1 = '10_04'
time_label_2 = '10_05'
time_label = time_label_1 + '-' + time_label_2
path_1 = 'D:\\mxnetLearn\\traffic_forcast\\visual_part\\data_sample\\' + time_label_1 + '.csv'
path_2 = 'D:\\mxnetLearn\\traffic_forcast\\visual_part\\data_sample\\' + time_label_2 + '.csv'
path_labels = 'D:\\mxnetLearn\\traffic_forcast\\visual_part\\data_sample\\' + time_label_2 + '.csv'
df1 = pd.read_csv(path_1)
df2 = pd.read_csv(path_2)
df3 = pd.read_csv(path_labels,index_col=[0])
y_label = df3.index.values
y_label = list(y_label)
pass


df1 = (df1 - df1.min()) / (df1.max() - df1.min())
df2 = (df2 - df2.min()) / (df2.max() - df2.min())


z1 = nd.array(df1.values[:,1:])
z2 = nd.array(df2.values[:,1:])
print(z1,z2)
z = nd.concat(z1,z2,dim=1)
print(z)
z = z.asnumpy()
c = plt.pcolor(z,cmap='cool')
x_lst = make_time_lst()

plt.title(time_label)
lst_1 = list(range(0,24,2))
lst_2 = list(range(0,24,2))
lst_1.extend(lst_2)
print(lst_1)
plt.xticks(range(0,288,12),lst_1)  #设置x轴的刻度值为每六个显示一个，值为第二个参数对应的值
plt.yticks(range(0,69,2),y_label[::2])


plt.colorbar(c)
plt.show()