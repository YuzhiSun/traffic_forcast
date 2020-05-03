import os
import warnings
from mxnet import image
from mxnet.gluon.data import dataset
import pandas as pd


class MyDataset(dataset.Dataset):
    """从一个结构化的文件夹中读取图片和标签数据.

    like::

        root/img/0001.jpg
        root/label/0001.csv


    Parameters
    ----------
    root : str
        Path to root directory.
    flag : {0, 1}, default 1
        If 0, always convert loaded images to greyscale (1 channel).
        If 1, always convert loaded images to colored (3 channels).
    transform : callable, default None
        A function that takes data and label and transforms them::

            transform = lambda data, label: (data.astype(np.float32)/255, label)

    Attributes
    ----------
    items : list of tuples
        List of all images in (img_path, label_path) pairs.
    """
    def __init__(self, root, flag=1, transform=None):
        self._root = os.path.expanduser(root)
        self._flag = flag
        self._transform = transform
        self._exts = ['.jpg', '.jpeg', '.png']
        self._list_image_label(self._root)

    def _list_image_label(self, root):
        self.items = []  # 存储图片和标签的地址元组列表
        label_path = self._root + '\\label_lst.csv'
        with open(label_path, 'r') as f:
            lines = f.readlines()[1:]
            tokens = [l.rstrip() for l in lines]
        for path_pie in tokens:
            img_path = self._root + '\\img\\' + path_pie + '.png'
            label_path = self._root + '\\label\\' + path_pie + '.csv'
            self.items.append((img_path,label_path))

    def __getitem__(self, idx):
        img = image.imread(self.items[idx][0], self._flag)
        label_df = pd.read_csv(self.items[idx][1],index_col=[0])
        label = label_df.values.reshape((1,22)).tolist()[0]
        if self._transform is not None:
            return self._transform(img, label)
        return img, label

    def __len__(self):
        return len(self.items)
# root = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\train_data'
#
# dataset_ = MyDataset(root)
# print(dataset_[1])


