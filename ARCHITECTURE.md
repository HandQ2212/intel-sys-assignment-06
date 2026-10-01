# Architecture

## Data Schemas
- `data/AMZN.csv` and `data/gold_price.csv` are expected to have a chronological temporal column (e.g., `Date`) and target value column (e.g., `Close` or `Price`).
- Data must be chronological, missing values forward-filled or interpolated appropriately.

## Tensor Shapes
- Inputs to models: `(batch_size, sequence_length, feature_dim)`
- Outputs from models: `(batch_size, 1)` corresponding to many-to-one architecture.

## Model Serialization Standard (`models/*.pkl`)
Each pipeline must export a `.pkl` dictionary formatted as follows:

```python
{
    "model_name": "pytorch_lstm_amzn", # Unique identifier
    "framework": "pytorch",             # "pytorch" or "keras"
    "target_column": "Close",           # Name of the column being predicted
    "seq_length": 30,                   # Sequence length used during training
    "scaler": fitted_scaler_instance,   # Fitted MinMaxScaler object (scikit-learn)
    "metrics": {
        "rmse": float(test_rmse),
        "mae": float(test_mae),
        "mape": float(test_mape),
        "directional_acc": float(dir_acc)
    },
    "model_path": "models/pytorch_lstm_amzn.pth" # Path to weight file (.pth or .keras)
}
```

The app dashboard `app.py` will auto-discover all `.pkl` bundles in the `models/` directory.