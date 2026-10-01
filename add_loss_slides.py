import re

with open('rnn_slides.tex', 'r') as f:
    content = f.read()

new_slides = r"""% ---------------- SLIDE 19 ----------------
\begin{frame}{Bản chất Hàm mất mát (Loss Function) trong RNN}
\begin{block}{\textbf{Khái niệm}}
Hàm mất mát $L$ (Loss Function) là thước đo độ sai lệch giữa \textbf{dự đoán của mô hình} ($\hat{y}$) và \textbf{kết quả thực tế} ($y$). Mục tiêu tối thượng của quá trình huấn luyện RNN là tìm ra tập trọng số $U, W, V$ sao cho giá trị $L$ này đạt mức nhỏ nhất.
\end{block}

\vspace{0.3cm}
\begin{alertblock}{\textbf{Đặc trưng Mất mát trong Dữ liệu Chuỗi (Sequential Loss)}}
Không giống như mạng Feedforward (chỉ đưa ra 1 đầu ra ở lớp cuối), mô hình RNN có thể đưa ra dự đoán $\hat{y}_t$ tại \textbf{nhiều bước thời gian} $t$. 
\begin{itemize}
    \item Hàm mất mát toàn cục $L$ được định nghĩa là \textbf{tổng (hoặc trung bình cộng)} của tất cả các hàm mất mát cục bộ $L_t$ tại từng bước thời gian:
    \[ L = \sum_{t=1}^{T} L_t \quad \text{hoặc} \quad L = \frac{1}{T} \sum_{t=1}^{T} L_t \]
    \item \textit{Nhắc lại sơ đồ trước:} Tín hiệu sai số $L_t$ từ mọi thời điểm sẽ được thu thập và cộng dồn lại thành $L$ tổng, sau đó mới tiến hành tính đạo hàm lan truyền ngược (BPTT).
\end{itemize}
\end{alertblock}
\end{frame}

% ---------------- SLIDE 20 ----------------
\begin{frame}{Cách chọn Công thức tính Mất mát cục bộ ($L_t$)}
Việc chọn công thức tính $L_t$ hoàn toàn phụ thuộc vào \textbf{bản chất của đầu ra} bài toán:

\vspace{0.2cm}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{exampleblock}{\textbf{1. Bài toán Hồi quy (Regression)}}
\textit{Dự đoán một giá trị số thực liên tục (VD: Dự báo giá vàng ngày mai, dự báo nhiệt độ).}
\begin{itemize}
    \item \textbf{Mean Squared Error (MSE):} Phạt nặng các sai số lớn. Là Loss phổ biến nhất.
    \[ L_t = (y_t - \hat{y}_t)^2 \]
    \item \textbf{Mean Absolute Error (MAE):} Bền vững (robust) hơn với các nhiễu ngoại lai.
    \[ L_t = |y_t - \hat{y}_t| \]
\end{itemize}
\end{exampleblock}
\end{column}

\begin{column}{0.48\textwidth}
\begin{alertblock}{\textbf{2. Bài toán Phân loại (Classification)}}
\textit{Dự đoán xác suất thuộc về các nhóm (VD: Phân loại cảm xúc văn bản, Dịch máy).}
\begin{itemize}
    \item \textbf{Cross-Entropy Loss (Entropy Chéo):} Đo lường khoảng cách giữa 2 phân phối xác suất.
    \[ L_t = -\sum_{c=1}^{C} y_{t,c} \log(\hat{y}_{t,c}) \]
    \scriptsize Trong đó $y_{t,c}$ là nhãn thật (One-hot vector) và $\hat{y}_{t,c}$ là xác suất dự đoán (qua Softmax).
\end{itemize}
\end{alertblock}
\end{column}
\end{columns}
\end{frame}

"""

# Insert right before SLIDE 19
content = content.replace("% ---------------- SLIDE 19 ----------------\n\\begin{frame}{Backpropagation Through Time (BPTT)}", new_slides + "% ---------------- SLIDE 19 ----------------\n\\begin{frame}{Backpropagation Through Time (BPTT)}")

with open('rnn_slides.tex', 'w') as f:
    f.write(content)

print("Added new slides.")
