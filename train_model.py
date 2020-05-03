import d2lzh as d2l
from mxnet import autograd, gluon, init
from mxnet.gluon import data as gdata, loss as gloss, nn
import os
import pandas as pd
import shutil
import time
from mxnet import nd

from traffic_forcast.datasetUtil import MyDataset

train_dir, test_dir, batch_size = 'train', 'test', 5

transform_train = gdata.vision.transforms.Compose([
    gdata.vision.transforms.Resize(size=(35,75)),
    gdata.vision.transforms.RandomResizedCrop(size=(30,69), scale=(0.64, 1.0),
                                              ratio=(1.0, 1.0)),
    gdata.vision.transforms.RandomFlipLeftRight(),
    gdata.vision.transforms.ToTensor(),
    gdata.vision.transforms.Normalize([0.4914, 0.4822, 0.4456],
                                      [0.2032, 0.1994, 0.2010])])



transform_test = gdata.vision.transforms.Compose([
    gdata.vision.transforms.ToTensor(),
    gdata.vision.transforms.Normalize([0.4914, 0.4822, 0.4456],
                                      [0.2032, 0.1994, 0.2010])])

train_root = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\train_data'
valid_root = 'D:\\mxnetLearn\\traffic_forcast\\test_data\\valid_data'
train_ds = MyDataset(train_root, flag=1)
valid_ds = MyDataset(valid_root, flag=1)

train_iter = gdata.DataLoader(train_ds.transform_first(transform_train),
                              batch_size, shuffle=True, last_batch='keep')
valid_iter = gdata.DataLoader(valid_ds.transform_first(transform_train),
                              batch_size, shuffle=True, last_batch='keep')
class Residual(nn.HybridBlock):
    def __init__(self, num_channels, use_1x1conv=False, strides=1, **kwargs):
        super(Residual, self).__init__(**kwargs)
        self.conv1 = nn.Conv2D(num_channels, kernel_size=3, padding=1,
                               strides=strides)
        self.conv2 = nn.Conv2D(num_channels, kernel_size=3, padding=1)
        if use_1x1conv:
            self.conv3 = nn.Conv2D(num_channels, kernel_size=1,
                                   strides=strides)
        else:
            self.conv3 = None
        self.bn1 = nn.BatchNorm()
        self.bn2 = nn.BatchNorm()

    def hybrid_forward(self, F, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.conv3:
            X = self.conv3(X)
        return F.relu(Y + X)



def resnet18(num_classes):
    net = nn.HybridSequential()
    net.add(nn.Conv2D(64, kernel_size=3, strides=1, padding=1),
            nn.BatchNorm(), nn.Activation('relu'))

    def resnet_block(num_channels, num_residuals, first_block=False):
        blk = nn.HybridSequential()
        for i in range(num_residuals):
            if i == 0 and not first_block:
                blk.add(Residual(num_channels, use_1x1conv=True, strides=2))
            else:
                blk.add(Residual(num_channels))
        return blk

    net.add(resnet_block(64, 2, first_block=True),
            resnet_block(128, 2),
            resnet_block(256, 2),
            resnet_block(512, 2))
    net.add(nn.GlobalAvgPool2D(), nn.Dense(num_classes))
    return net



def get_net(ctx):
    num_classes = 22
    net = resnet18(num_classes)
    net.initialize(ctx=ctx, init=init.Xavier())
    return net

def log_rmse(net,features,labels):
    clipped_pred = nd.clip(net(features),1,float('inf'))
    rmse = nd.sqrt(2*loss(clipped_pred.log(),labels.log()).mean())
    return rmse.asscalar()

loss = gloss.L2Loss()

def train(net, train_iter, valid_iter, num_epochs, lr, wd, ctx, lr_period,
          lr_decay):
    trainer = gluon.Trainer(net.collect_params(), 'sgd',
                            {'learning_rate': lr, 'momentum': 0.9, 'wd': wd})
    for epoch in range(num_epochs):
        train_rmse, train_n, start = 0.0, 0, time.time()
        valid_rmse, valid_n = 0.0, 0
        if epoch > 0 and epoch % lr_period == 0:
            trainer.set_learning_rate(trainer.learning_rate * lr_decay)
        for X, y in train_iter:
            y = y.astype('float32').as_in_context(ctx)
            with autograd.record():
                y_hat = net(X.as_in_context(ctx))
                l = loss(y_hat, y)
            l.backward()
            trainer.step(batch_size)
            train_rmse += log_rmse(net,X.as_in_context(ctx),y)
            train_n += y.size
        time_s = "time %.2f sec" % (time.time() - start)
        if valid_iter is not None:
            for X, y in valid_iter:
                y = y.astype('float32').as_in_context(ctx)
                valid_rmse += log_rmse(net, X.as_in_context(ctx), y)
                valid_n += y.size
            epoch_s = ("epoch: %d, train rmse: %f, valid rmse: %f,"
                       % (epoch + 1, train_rmse / train_n, valid_rmse / valid_n))
        else:
            epoch_s = ("epoch: %d, train rmse: %f" % (epoch + 1, train_rmse / train_n))
        print(epoch_s + time_s + ', lr:' + str(trainer.learning_rate))




ctx, num_epochs, lr, wd = d2l.try_gpu(), 10, 0.1, 5e-4
lr_period, lr_decay, net = 80, 0.1, get_net(ctx)
net.hybridize()
train(net, train_iter,valid_iter, num_epochs, lr, wd, ctx, lr_period,
      lr_decay)





# for X, _ in test_iter:
#     y_hat = net(X.as_in_context(ctx))
#     preds.extend(y_hat.argmax(axis=1).astype(int).asnumpy())
# sorted_ids = list(range(1, len(test_ds) + 1))
# sorted_ids.sort(key=lambda x: str(x))
# df = pd.DataFrame({'id': sorted_ids, 'label': preds})
# df['label'] = df['label'].apply(lambda x: train_valid_ds.synsets[x])
# df.to_csv('submission.csv', index=False)


