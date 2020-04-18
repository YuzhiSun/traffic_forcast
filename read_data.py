import pandas as pd

data_reader = pd.read_csv('D:\\mxnetLearn\\traffic_forcast\\data\\chengdushi_road.txt',
                          dtype='str', nrows=100)
print(data_reader)
# for data in data_reader:
#     print(data)