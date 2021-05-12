import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

import myModel

x1 = torch.unsqueeze(torch.linspace(-10, 10, 1000), dim=1)
x2 = torch.unsqueeze(torch.linspace(-10, 10, 1000), dim=1)

# create a singular tensor by horizontally stacking tensors x1 and x2
data = torch.column_stack((x1.clone(), x2.clone()))
torch.save(data, 'dataset2.dat')

x = torch.load('dataset2.dat')
y = torch.sin(x1.clone() + x2.clone() / np.pi).clone()
# we set up the lossFunction as the mean square error
loss_func = torch.nn.L1Loss()
# we create the ANN
ann = myModel.Net(n_feature=2, n_hidden=10, n_output=1)

print(ann)
# we use an optimizer that implements stochastic gradient descent
optimizer_batch = torch.optim.SGD(ann.parameters(), lr=.2)

# we memorize the losses for some graphics
loss_list = []
avg_loss_list = []

# we set up the environment for training in batches
batch_size = 32
n_batches = int(len(x) / batch_size)
print(n_batches)

for epoch in range(2000):

    for batch in range(n_batches):
        batch_X, batch_y = x[batch * batch_size:(batch + 1) * batch_size, ], y[batch * batch_size:(
                                                                                                              batch + 1) * batch_size, ]
        # we compute the output for this batch
        prediction = ann(torch.FloatTensor(batch_X))
        batch_y = torch.FloatTensor(batch_y)
        # we compute the loss for this batch
        loss = loss_func(prediction, batch_y)

        # we save it for graphics
        loss_list.append(loss)

        # we set up the gradients for the weights to zero (important in pytorch)
        optimizer_batch.zero_grad()

        # we compute automatically the variation for each weight (and bias) of the network
        loss.backward()

        # we compute the new values for the weights
        optimizer_batch.step()

        # we print the loss for all the dataset2 for each 10th epoch
    if epoch % 100 == 99:
        y_pred = loss_list[len(loss_list) - 1]
        loss = loss_func(y_pred, y)
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    # Specify a path
filepath = "dataset2.dat"

# save the model to file
torch.save(ann.state_dict(), filepath)
