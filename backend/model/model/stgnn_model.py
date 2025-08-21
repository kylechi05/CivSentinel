import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class STGNN(nn.Module):
  def __init__(self, num_nodes, window_size, horizon, hidden_dim=64):
    super(STGNN, self).__init__()
    self.num_nodes = num_nodes
    self.window_size = window_size
    self.horizon = horizon
    self.hidden_dim = hidden_dim

    self.gru = nn.GRU(input_size=1, hidden_size=hidden_dim, batch_first=True)

    self.gc1 = GCNConv(hidden_dim, hidden_dim)
    self.gc2 = GCNConv(hidden_dim, hidden_dim)


    self.fc = nn.Linear(hidden_dim, horizon)

  def forward(self, x, edge_index):
    x = x.unsqueeze(-1)

    out, _ = self.gru(x)
    out = out[:, -1, :]

    out = F.relu(self.gc1(out, edge_index))
    out = F.relu(self.gc2(out, edge_index))

    out = self.fc(out)
    return out