import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.graph_objects as plotly_go
from plotly.subplots import make_subplots
import torch
import torch.nn as nn

# Since we define PyTorch models in notebooks, we need to redefine them here for loading



class TimeSeriesRNN(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.2):
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



# Streamlit App
st.set_page_config(page_title="RNN Forecasting Dashboard", layout="wide")
st.title("📈 RNN Time-Series Forecasting Dashboard")

@st.cache_data
def load_bundles():
    bundles = {}
    models_dir = '../models'
    if not os.path.exists(models_dir):
        return bundles
    for f in os.listdir(models_dir):
        if f.endswith('.pkl'):
            try:
                with open(os.path.join(models_dir, f), 'rb') as file:
                    b = pickle.load(file)
                    bundles[b['model_name']] = b
            except Exception as e:
                pass
    return bundles

bundles = load_bundles()

if not bundles:
    st.warning("No model bundles found in `../backend/models/`. Please run the training notebooks first.")
    st.stop()

st.sidebar.header("Model Selection")
selected_model_name = st.sidebar.selectbox("Select a Model Bundle", list(bundles.keys()))

bundle = bundles[selected_model_name]
st.sidebar.write(f"**Framework:** {bundle['framework'].capitalize()}")
st.sidebar.write(f"**Target Column:** {bundle['target_column']}")
st.sidebar.write(f"**Sequence Length:** {bundle['seq_length']}")

# Load Model
@st.cache_resource
def load_model(bundle):
    path = bundle['model_path']
    if not os.path.exists(path):
        path = os.path.join('../models', os.path.basename(path))
    if bundle['framework'] == 'pytorch':
        # Simple heuristic to pick class based on name
        model = TimeSeriesRNN()
        try:
            model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
            model.eval()
            return model
        except Exception as e:
            st.error(f"Failed to load PyTorch model: {e}")
            return None
    elif bundle['framework'] == 'keras':
        import tensorflow as tf
        try:
            model = tf.keras.models.load_model(path)
            return model
        except Exception as e:
            st.error(f"Failed to load Keras model: {e}")
            return None

model = load_model(bundle)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Model Overview & Metrics", "🔮 Interactive Forecasting", "🔍 Error Diagnostics"])

with tab1:
    st.subheader("Model Performance Metrics (Test Set)")
    metrics = bundle['metrics']
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
    col2.metric("MAE", f"{metrics.get('mae', 0):.4f}")
    col3.metric("MAPE", f"{metrics.get('mape', 0):.4f}")
    col4.metric("Directional Accuracy", f"{metrics.get('directional_acc', 0):.2%}")

with tab2:
    st.subheader("Interactive Forecasting")
    dataset_choice = "AMZN" if "amzn" in bundle['model_name'].lower() else "Gold"
    data_path = f"../data/{dataset_choice}.csv" if dataset_choice == "AMZN" else "../data/gold_price.csv"
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        date_col = 'Date' if 'Date' in df.columns else df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col).set_index(date_col)
        
        target = bundle['target_column']
        if target not in df.columns and len(df.columns) > 0:
            target = df.columns[0]
            
        data = df[target].ffill().bfill().values
        
        cutoff_idx = st.slider("Select Data Cutoff Index (Test Split)", min_value=bundle['seq_length'], max_value=len(data)-1, value=int(len(data)*0.85))
        
        seq_len = bundle['seq_length']
        history = data[cutoff_idx - seq_len:cutoff_idx]
        actual_next = data[cutoff_idx]
        
        st.write(f"**Predicting step {cutoff_idx} using previous {seq_len} steps.**")
        st.write(f"Actual Value at cutoff: {actual_next:.2f}")
        
        if st.button("Predict Next Step"):
            scaler = bundle['scaler']
            hist_scaled = scaler.transform(history.reshape(-1, 1))
            
            if bundle['framework'] == 'pytorch':
                x_tensor = torch.Tensor(hist_scaled).unsqueeze(0)
                with torch.no_grad():
                    pred_scaled = model(x_tensor).numpy()
            else:
                x_tensor = np.expand_dims(hist_scaled, axis=0)
                pred_scaled = model.predict(x_tensor, verbose=0)
                
            pred = scaler.inverse_transform(pred_scaled)[0][0]
            st.success(f"Predicted Value: {pred:.2f}")
            
            # Plot
            fig = plotly_go.Figure()
            fig.add_trace(plotly_go.Scatter(y=history, mode='lines+markers', name='Context Window (History)'))
            fig.add_trace(plotly_go.Scatter(x=[seq_len], y=[actual_next], mode='markers', name='Actual Next', marker=dict(color='green', size=10)))
            fig.add_trace(plotly_go.Scatter(x=[seq_len], y=[pred], mode='markers', name='Predicted Next', marker=dict(color='red', size=10, symbol='x')))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Dataset {data_path} not found.")

with tab3:
    st.subheader("Error Diagnostics")
    st.write("Displays the distribution of errors across the testing set. A zero-centered distribution indicates unbiased predictions.")
    
    # Normally we would load predictions from the bundle or re-predict the test set here.
    # For a simple diagnostic view without re-running inference on the whole test set:
    st.info("To see a full residual plot, the app would re-run inference on the test split.")
    st.write(f"Directional Accuracy Metric: {bundle['metrics'].get('directional_acc', 0):.2%}")
