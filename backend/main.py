from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import pickle
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import tensorflow as tf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TimeSeriesRNN(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=1, dropout=0.2):
        super(TimeSeriesRNN, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.rnn(x)
        last_hidden = out[:, -1, :]
        last_hidden = self.dropout(last_hidden)
        y_hat = self.fc(last_hidden)
        return y_hat

bundles = {}
models = {}
datasets = {}

def load_all_models():
    models_dir = '../models'
    if not os.path.exists(models_dir):
        return
    for f in os.listdir(models_dir):
        if f.endswith('.pkl'):
            with open(os.path.join(models_dir, f), 'rb') as file:
                bundle = pickle.load(file)
                name = bundle['model_name']
                bundles[name] = bundle
                
                # load model
                path = bundle['model_path']
                if not os.path.exists(path):
                    path = os.path.join('../models', os.path.basename(path))
                
                if bundle['framework'] == 'pytorch':
                    model = TimeSeriesRNN()
                    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
                    model.eval()
                    models[name] = model
                elif bundle['framework'] == 'keras':
                    model = tf.keras.models.load_model(path)
                    models[name] = model

                # Load dataset for convenience
                dataset_choice = "AMZN" if "amzn" in name.lower() else "Gold"
                data_path = f"../data/{dataset_choice}.csv" if dataset_choice == "AMZN" else "../data/gold_price.csv"
                if dataset_choice not in datasets and os.path.exists(data_path):
                    df = pd.read_csv(data_path)
                    date_col = 'Date' if 'Date' in df.columns else df.columns[0]
                    df[date_col] = pd.to_datetime(df[date_col])
                    df = df.sort_values(date_col).set_index(date_col)
                    
                    target = bundle['target_column']
                    if target not in df.columns and len(df.columns) > 0:
                        target = df.columns[0]
                    
                    data = df[target].ffill().bfill().values
                    datasets[dataset_choice] = data

load_all_models()

class PredictRequest(BaseModel):
    model_name: str
    cutoff_idx: int

@app.get("/api/models")
def get_models():
    return [{"name": name, "framework": b['framework'], "target": b['target_column'], "seq_length": b['seq_length'], "metrics": b['metrics']} for name, b in bundles.items()]

@app.post("/api/predict")
def predict(req: PredictRequest):
    if req.model_name not in bundles or req.model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    bundle = bundles[req.model_name]
    model = models[req.model_name]
    
    dataset_choice = "AMZN" if "amzn" in req.model_name.lower() else "Gold"
    data = datasets.get(dataset_choice)
    if data is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    seq_len = bundle['seq_length']
    cutoff = req.cutoff_idx
    if cutoff < seq_len or cutoff >= len(data):
        cutoff = len(data) - 1
        
    history = data[cutoff - seq_len:cutoff]
    actual_next = float(data[cutoff])
    
    scaler = bundle['scaler']
    hist_scaled = scaler.transform(history.reshape(-1, 1))
    
    if bundle['framework'] == 'pytorch':
        x_tensor = torch.Tensor(hist_scaled).unsqueeze(0)
        with torch.no_grad():
            pred_scaled = model(x_tensor).numpy()
    else:
        x_tensor = np.expand_dims(hist_scaled, axis=0)
        pred_scaled = model.predict(x_tensor, verbose=0)
        
    pred = float(scaler.inverse_transform(pred_scaled)[0][0])
    
    return {
        "history": history.tolist(),
        "actual_next": actual_next,
        "predicted_next": pred,
        "seq_length": seq_len,
        "cutoff_idx": cutoff
    }

# Ensure static dir exists
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
