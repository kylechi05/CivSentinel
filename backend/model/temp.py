

model = torch.load('/content/drive/MyDrive/Colab Notebooks/CivSentinel/STGNN_Model', weights_only=False)
model.eval()

graph_ed = torch.load('/content/drive/MyDrive/Colab Notebooks/CivSentinel/STGNN_Model_Graph')


temp_test_set = torch.tensor(train_set[100][0], dtype=torch.float32)
with torch.no_grad(): 
  preds = torch.stack([model(temp_test_set, graph_ed)])

preds = torch.clamp(preds, min=0.0)

pred_probs = 1 - torch.exp(-preds[0]) 

threshold = 0.5
crime_flags = pred_probs >= threshold

id_to_hex = {v: k for k, v in hex_to_id.items()}

for day in range(pred_probs.shape[1]):
    print(f"Predicted crimes for day {day+1}:")
    for i in range(len(crime_flags)):
        if crime_flags[i, day]:
            print(id_to_hex[i])