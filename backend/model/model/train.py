import os

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from stgnn_model import STGNN

def create_rolling_windows(crime_freq, window_size=30, horizon=2, start_day=None, end_day=None):
  if start_day is not None:
    crime_freq = crime_freq.loc[:, start_day:]
  if end_day is not None:
    crime_freq = crime_freq.loc[:, :end_day]

  windows = []
  crime_array = crime_freq.values
  num_days = crime_freq.shape[1]

  for i in range(num_days - window_size - horizon + 1):
    past_window = crime_array[:, i:i+window_size]
    future_window = crime_array[:, i+window_size:i+window_size+horizon]
    windows.append((past_window, future_window))

  return windows

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

crime_freq_path = os.path.join(BASE_DIR, '../datasets/processed/crime_freq.csv')
graph_edges_path = os.path.join(BASE_DIR, '../datasets/processed/graph_edges.pt')
saved_model_path = os.path.join(BASE_DIR, '../saved_models/STGNN_Model.pt')

crime_freq = pd.read_csv(crime_freq_path, index_col=0, parse_dates=True)
graph_edges = torch.load(graph_edges_path)

train_set = create_rolling_windows(crime_freq, window_size=30, horizon=2, start_day='2023-01-01', end_day='2025-01-04')
val_set = create_rolling_windows(crime_freq, window_size=30, horizon=2, start_day='2025-01-05', end_day='2025-04-02')
test_set = create_rolling_windows(crime_freq, window_size=30, horizon=2, start_day='2025-04-03', end_day='2025-06-29')

window_size = 30
hidden_dim = 32
horizon = 2
lr = 0.001
epochs = 50
batch_size = 32

X_train = torch.stack([torch.tensor(pw, dtype=torch.float) for pw, _ in train_set])
y_train = torch.stack([torch.tensor(fw, dtype=torch.float) for _, fw in train_set])

X_val = torch.stack([torch.tensor(pw, dtype=torch.float) for pw, _ in val_set])
y_val = torch.stack([torch.tensor(fw, dtype=torch.float) for _, fw in val_set])

X_test = torch.stack([torch.tensor(pw, dtype=torch.float) for pw, _ in test_set])
y_test = torch.stack([torch.tensor(fw, dtype=torch.float) for _, fw in test_set])

train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

val_dataset = TensorDataset(X_val, y_val)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)

test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

model = STGNN(window_size, hidden_dim, horizon)
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

for epoch in range(epochs):
    total_loss = 0
    for x_batch, y_batch in train_loader:
        optimizer.zero_grad()
        preds = torch.stack([model(x, graph_edges) for x in x_batch])
        loss = loss_fn(preds, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_train_loss = total_loss / len(train_loader)

    model.eval()
    val_loss = 0
    with torch.no_grad():
        for x_batch, y_batch in val_loader:
            preds = torch.stack([model(x, graph_edges) for x in x_batch])
            loss = loss_fn(preds, y_batch)
            val_loss += loss.item()
    avg_val_loss = val_loss / len(val_loader)
    
    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

X_test = torch.stack([torch.tensor(pw, dtype=torch.float) for pw, _ in test_set])
y_test = torch.stack([torch.tensor(fw, dtype=torch.float) for _, fw in test_set])

test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

model.eval()
test_loss = 0
with torch.no_grad():
    for x_batch, y_batch in test_loader:
        preds = torch.stack([model(x, graph_edges) for x in x_batch])
        loss = loss_fn(preds, y_batch)
        test_loss += loss.item()
test_loss /= len(test_loader)

print(f'Test Lost: {test_loss}')

torch.save(model, saved_model_path)

print(f'STGNN model saved to {saved_model_path}')