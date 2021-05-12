import torch

import myModel

# we load the model
if __name__ == "__main__":
    filepath = "dataset.dat"
    ann = myModel.Net(2, 10, 1)

    ann.load_state_dict(torch.load(filepath))
    ann.eval()

    # visualise the parameters for the ann (aka weights and biases)
    for name, param in ann.named_parameters():
        if param.requires_grad:
            print(name, param.data)

    x1 = float(input("x1 = "))
    x2 = float(input("x2 = "))
    x1 = torch.tensor([x1, x2])
    print(ann(x1).tolist())