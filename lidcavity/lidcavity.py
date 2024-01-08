import numpy as np
import torch
import os
from torch.utils.data import TensorDataset




class LidCavity():
    def __init__(self, batch_size):
        from numpy.random import Generator, PCG64
        self.rg = Generator(PCG64(42))
        test_indices=self.rg.choice(600,size=100, replace=False)
        train_indices=np.setdiff1d(np.arange(600),test_indices)
        self.batch_size = batch_size
        self.data_directory = os.path.join(os.path.dirname(__file__), 'data')
        grid=torch.tensor(np.load(os.path.join(self.data_directory, 'grid.npy')),dtype=torch.float32)
        V=torch.tensor(np.load(os.path.join(self.data_directory, 'result.npy')),dtype=torch.float32)
        self.grid_train=grid[train_indices]
        self.grid_test=grid[test_indices]
        del grid
        self.V_train=V[train_indices]
        self.V_test=V[test_indices]
        del V
        self.params=np.load(os.path.join(self.data_directory, 'par.npy'))
        self.params_train=self.params[train_indices]
        self.params_test=self.params[test_indices]
        self.time=np.load(os.path.join(self.data_directory, 'times.npy'))
        self.points=np.load(os.path.join(self.data_directory, 'points.npy'))
        self.x=self.points[:,0]
        self.y=self.points[:,1]
        self.weights_space=np.load(os.path.join(self.data_directory, 'weights_space.npy'))
        self.weights_time=np.load(os.path.join(self.data_directory, 'weights_times.npy'))
        self.train_dataset=TensorDataset(self.grid_train,self.V_train)
        self.test_dataset=TensorDataset(self.grid_test,self.V_test)
        self.train_loader=torch.utils.data.DataLoader(self.train_dataset,batch_size=batch_size,shuffle=False)
        self.test_loader=torch.utils.data.DataLoader(self.test_dataset,batch_size=batch_size,shuffle=False)
        self.diff_x=np.load(os.path.join(self.data_directory, 'diff_x.npy'))
        self.diff_y=np.load(os.path.join(self.data_directory, 'diff_y.npy'))
