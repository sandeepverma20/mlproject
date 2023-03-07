# -*- coding: utf-8 -*-
"""Simple_Classification_Pytorch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FlwzKL8w0ooSo641tDAgTZoDcT5xfzs8
"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import pandas as pd
import numpy as np
import torch.nn as nn
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler

#Set the random seed

torch.manual_seed(2022)

bankrupt = pd.read_csv("/content/Bankruptcy.csv")

bankrupt.head()

X = bankrupt.drop(['NO','YR','D'],axis=1).values
y = bankrupt['D'].values
scaler = MinMaxScaler()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, 
                                                    random_state=42,stratify=y)
X_scl_trn = scaler.fit_transform(X_train) 
X_scl_tst = scaler.transform(X_test)

X_torch = torch.from_numpy(X_scl_trn)
y_torch = torch.from_numpy(y_train)
print(X_torch.size())
print(y_torch.size())

type(X_torch)

# Create a model
model = nn.Sequential(nn.Linear(in_features=X_scl_trn.shape[1], out_features=5),
                      nn.ReLU(),
                      nn.Linear(5, 3),
                      nn.ReLU(),
                      nn.Linear(3,1),
                      nn.Sigmoid())

criterion = torch.nn.BCELoss()
# Construct the optimizer (Adam in this case)
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)
optimizer

y_pred = model(X_torch.float())
y_torch = y_torch.unsqueeze(1)
print(y_torch.shape)
print(y_pred.shape)

# Gradient Descent

for epoch in np.arange(0,1000):
   # Forward pass: Compute predicted y by passing x to the model
   y_pred_prob = model(X_torch.float())

   # Compute and print loss
   loss = criterion(y_pred_prob, y_torch.float())
   print('epoch: ', epoch+1,' loss: ', loss.item())

   # Zero gradients, perform a backward pass, and update the weights.
   optimizer.zero_grad()

   # perform a backward pass (backpropagation)
   loss.backward()

   # Update the parameters
   optimizer.step()
#print('epoch: ', epoch+1,' loss: ', loss.item())

X_torch_test = torch.from_numpy(X_scl_tst)
y_pred_prob = model(X_torch_test.float()) # Equivalent predict_proba / predict
y_pred_prob = y_pred_prob.detach().numpy()
y_pred_prob = y_pred_prob.reshape(y_test.shape[0],)
y_pred_prob[:5]

y_pred = np.where(y_pred_prob >= 0.5,1,0)

y_pred[:5]

print(accuracy_score(y_test,y_pred))

"""accuracy_score

0.825

"""

