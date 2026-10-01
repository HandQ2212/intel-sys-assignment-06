# Operational Guidelines & Coding Constraints

## Mathematical Notation Standard
Across all notebooks and markdown explanations, strictly use standard deep learning notation ($W, U, V$):
- $W$: Input-to-hidden weight matrix ($x_t \to h_t$)
- $U$: Hidden-to-hidden recurrent weight matrix ($h_{t-1} \to h_t$)
- $V$: Hidden-to-output weight matrix ($h_t \to \hat{y}_t$)
- $b_h, b_y$: Bias vectors for hidden and output states

## Notebook Constraints
- Keep code cells small, clean, runnable, and thoroughly commented.
- No truncated code blocks or `# TODO` placeholders. Everything must be complete and executable.
- Granular markdown and code cells for each notebook.

## Pipeline Lifecycle (Notebooks 03-06)
Every single model notebook MUST strictly implement the following 6-step lifecycle in granular cells:
1. **Data Preprocessing & Sequence Engineering**: Clean missing data; parse chronological timestamps. Chronological split: 70% Train, 15% Validation, 15% Test (NEVER shuffle). Fit `MinMaxScaler(-1, 1)` strictly on Train only. Transform series into sliding 3D tensors: `(batch_size, sequence_length, feature_dim)`.
2. **Model Architecture Design**: Vanilla RNN, LSTM, GRU variants. `return_sequences=False`. Include Dropout. Output linear projection layer.
3. **Training Configuration**: Loss: MSE, MAE. Optimizers: Adam/RMSprop with adaptive LR scheduling. Gradient Clipping (`clipnorm=1.0` or `max_norm=1.0`).
4. **Training Loop & Diagnostics (BPTT)**: Track Train/Val Loss per epoch. Apply EarlyStopping and ReduceLROnPlateau. Plot loss curves.
5. **Independent Evaluation & Diagnostics**: Compute RMSE, MAE, MAPE on unscaled values on Test set. Test "1-step lag fallacy" (Directional Accuracy). Plot Ground Truth vs Preds with residual distributions.
6. **Serialization & Verification**: Save weights (`.pth` or `.keras`) and export a comprehensive metadata bundle into `models/*.pkl`. Test inference with a standalone function loading the bundle.