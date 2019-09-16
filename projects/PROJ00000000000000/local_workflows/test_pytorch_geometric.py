import torch
from torch_geometric.data import Data

# ==== from connectivity matrix to edges ====
edge_index_tmp = [[], []]
edge_attr_tmp = []

for idx, itm in enumerate(connect_mat):
    edge_index_tmp[0].extend([idx for i in range(len(itm)])
    edge_index_tmp[1].extend([i for i in range(len(itm)])
    for jdx, jtm in enumerate(itm):
        edge_attr_tmp.append([jtm])

edge_index = torch.tensor(edge_index_tmp, dtype=torch.long)
# where 0, 1 are the node indeces
# the shape of edge_index is [2, num_edges]

edge_attr = torch.tensor(edge_attr_tmp, dtype=torch.float)
# where the list items are the edge feature vectors
# the shape of edge_attr is [num_edges, num_edge_features]

x = torch.tensor([[-1], [0], [1]], dtype=torch.float)
# where the list items are the node feature vectors
# the shape of x is [num_nodes, num_node_features]

y = torch.tensor([[0]], dtype=torch.float)

data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

# ==== Create dataset with multiple data
from torch_geometric.data import DataLoader

data_list = [data, ..., data]
loader = DataLoader(data_list, batch_size=32, shuffle=true)

for batch in loader:
    pass # do operations on batches

import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = GCNConv(dataset.num_node_features, 16)
        self.conv2 = GCNConv(16, dataset.num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Net().to(device)
data = dataset[0].to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[train_mask])
    loss.backward()
    optimizer.step()

model.eval()
_, pred = model(data).max(dim=1)
correct = float(pred[data.test_mask].eq(data.y[data.test_mask]).sum().item())
acc = correct / data.test_mask.sum().item()
print('Accuracy: {:.4f}.format(acc)')
