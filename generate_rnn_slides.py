import os

preamble = r"""\documentclass[aspectratio=169, 10pt]{beamer}
\usepackage{fontspec}
\usefonttheme{professionalfonts}
\setmainfont{Times New Roman}
\setsansfont{Times New Roman}

\usepackage{amsmath, amssymb}
\usepackage{booktabs, colortbl, multirow}
\usepackage{tikz}
\usetikzlibrary{shapes, arrows.meta, positioning, calc, matrix, fit, backgrounds, decorations.pathreplacing}
\usepackage{graphicx}

\usetheme{Madrid}
\usecolortheme{whale}
\setbeamertemplate{navigation symbols}{}

% Custom Professional Color Palette
\definecolor{mainnavy}{RGB}{26, 54, 93}
\definecolor{accentteal}{RGB}{13, 92, 117}
\definecolor{teal}{RGB}{13, 92, 117}
\definecolor{warmorange}{RGB}{217, 119, 6}
\definecolor{crimsonred}{RGB}{220, 38, 38}
\definecolor{emeraldgreen}{RGB}{5, 150, 105}
\definecolor{slate}{RGB}{51, 65, 85}
\definecolor{lightbg}{RGB}{248, 250, 252}
\definecolor{boxblue}{RGB}{239, 246, 255}
\definecolor{boxgreen}{RGB}{240, 253, 244}
\definecolor{boxorange}{RGB}{255, 251, 235}
\definecolor{boxred}{RGB}{254, 242, 242}

\setbeamercolor{structure}{fg=mainnavy}
\setbeamercolor{title}{bg=mainnavy, fg=white}
\setbeamercolor{frametitle}{bg=mainnavy, fg=white}
\setbeamercolor{block title}{bg=mainnavy, fg=white}
\setbeamercolor{block body}{bg=lightbg, fg=slate}
\setbeamercolor{block title example}{bg=accentteal, fg=white}
\setbeamercolor{block body example}{bg=lightbg, fg=slate}
\setbeamercolor{block title alerted}{bg=crimsonred, fg=white}
\setbeamercolor{block body alerted}{bg=boxred, fg=slate}

% Custom Footline ensuring exact x / 24 numbering
\setbeamertemplate{footline}{%
  \leavevmode%
  \hbox{%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.5ex,dp=1.1ex,center]{author in head/foot}%
    \usebeamerfont{author in head/foot}Chuyên đề Học Sâu
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.5ex,dp=1.1ex,center]{title in head/foot}%
    \usebeamerfont{title in head/foot}Mạng Nơ-ron Hồi quy (RNN)
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.5ex,dp=1.1ex,right]{date in head/foot}%
    \usebeamerfont{date in head/foot}\insertframenumber{} / 24\hspace*{2.5ex}
  \end{beamercolorbox}}%
  \vskip0pt%
}

% Standardized Arrow & TikZ Styles
\tikzset{
  >=Stealth,
  flowarrow/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, mainnavy},
  flowarrow_teal/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, accentteal},
  flowarrow_red/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, crimsonred},
  flowarrow_green/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, emeraldgreen},
  flowarrow_orange/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, warmorange},
  axisarrow/.style={-{Stealth[length=2.2mm, width=1.5mm]}, thick, mainnavy}
}

\title[Chuyên đề RNN]{MẠNG NƠ-RON HỒI QUY (RNN)}
\subtitle{Từ Hạn Chế của MLP \& 1D-CNN đến Nguyên Lý Xử Lý Dữ Liệu Chuỗi có Trạng Thái Ẩn}
\author{Nhóm thực hiện:\\Văn Thị Mai Linh \and Nguyễn Văn Minh Lực \and Giáp Minh Hiếu \and Nguyễn Nam Hải}
\institute{Chuyên đề Học Sâu (Deep Learning)}
\date{}

\begin{document}

\begin{frame}[plain]
\titlepage
\vspace{-1cm}
\begin{center}
\textit{\footnotesize "Feedforward nhìn thế giới qua từng bức ảnh rời rạc;\\RNN thấu hiểu dữ liệu qua dòng chảy liên tục của thời gian."}
\end{center}
\end{frame}

\begin{frame}{Bản chất Dữ liệu dạng Chuỗi (Sequential Data)}
\begin{block}{\textbf{Thứ tự xuất hiện quyết định hoàn toàn ngữ nghĩa của dữ liệu}}
\begin{itemize}
    \item \textbf{Đặc tính trật tự:} Mỗi điểm dữ liệu tại thời điểm $t$ luôn mang mối tương quan mật thiết với các điểm quá khứ $t-1, t-2, \dots$
    \item \textbf{Hai dạng chính:} Dữ liệu token rời rạc (Text, DNA) và dữ liệu chuỗi số liên tục (Giá vàng, cổ phiếu, nhịp tim).
\end{itemize}
\end{block}

\vspace{0.3cm}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{exampleblock}{\textbf{Chuỗi Rời rạc (NLP / Văn bản)}}
"Hà Nội không mưa" $\neq$ "Mưa không Hà Nội"\\
\vspace{0.2cm}
$\rightarrow$ \textit{Câu đầu có nghĩa, câu sau vô nghĩa hoặc biến đổi ngữ nghĩa.}
\end{exampleblock}
\end{column}
\begin{column}{0.48\textwidth}
\begin{alertblock}{\textbf{Chuỗi Liên tục (Time-Series)}}
Giá vàng: $[ 82.5 \rightarrow 83.1 \rightarrow 84.0 \rightarrow 85.2 ]$ (Tăng)\\
Giá vàng: $[ 85.2 \rightarrow 84.0 \rightarrow 83.1 \rightarrow 82.5 ]$ (Giảm)
\end{alertblock}
\end{column}
\end{columns}
\end{frame}

\begin{frame}{Bài toán Dự đoán Phần tử Kế tiếp (Next Step Prediction)}
\textbf{Mục tiêu:} Cho chuỗi quan sát quá khứ $X = (x_1, x_2, \dots, x_t)$, dự đoán giá trị tương lai $x_{t+1}$.
\vspace{0.4cm}

\begin{block}{\textbf{Bài toán 1: Next Word Prediction (NLP)}}
Ngữ cảnh: \texttt{"We"} $\rightarrow$ \texttt{"are"} $\rightarrow$ \texttt{"learning"} $\rightarrow$ \texttt{"AI"} $\rightarrow$ \textbf{[ ? ]}\\
$\rightarrow$ Target kỳ vọng: \textbf{"is"}
\end{block}

\begin{exampleblock}{\textbf{Bài toán 2: Dự báo Chuỗi thời gian (Time-Series)}}
Cửa sổ trượt (30 ngày lịch sử):\\
$[ P(t-29), P(t-28), \dots , P(t-1), P(t) ] \rightarrow \textbf{[ P(t+1) ]}$\\
$\rightarrow$ Dự báo biến động ngày 31.
\end{exampleblock}
\end{frame}

\begin{frame}{Hai Pipeline Tiền xử lý Đặc trưng}
\textit{Dữ liệu thô không thể đưa trực tiếp vào mạng mà phải đi qua pipeline chuẩn hóa:}
\vspace{0.2cm}

\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{block}{\textbf{Văn bản (Text Pipeline)}}
\small
\begin{enumerate}
    \item \textbf{Văn bản thô:} "giá vàng tăng"
    \item \textbf{Tokenizer:} ["giá", "vàng", "tăng"]
    \item \textbf{Vocab Index:} $[2, 3, 4]$
    \item \textbf{Padding:} $[2, 3, 4, 0, 0]$
    \item \textbf{Embedding:} Tensor $[\text{Batch}, \text{Seq\_Len}, d]$
\end{enumerate}
\end{block}
\end{column}

\begin{column}{0.48\textwidth}
\begin{exampleblock}{\textbf{Chuỗi số (Time-Series Pipeline)}}
\small
\begin{enumerate}
    \item \textbf{File CSV thô:} Date, Price
    \item \textbf{Làm sạch \& Chia tập:} Train 70\%, Val 15\%, Test 15\%
    \item \textbf{Scaling:} log1p(Price) $\rightarrow$ MinMax (chỉ fit trên Train)
    \item \textbf{Windowing:} Cửa sổ trượt 30 ngày
    \item \textbf{Đầu vào:} Tensor $[\text{N}, 30, 1]$
\end{enumerate}
\end{exampleblock}
\end{column}
\end{columns}
\end{frame}

\begin{frame}{Tiếp cận bằng MLP \& Cơ chế Ghép phẳng (Flatten)}
\textit{Mạng truyền thẳng (MLP) bắt buộc phải biến toàn bộ ngữ cảnh thành một vector phẳng duy nhất.}
\vspace{0.2cm}

\begin{center}
\begin{tikzpicture}[node distance=0.3cm, scale=0.8, every node/.style={scale=0.8}]
    \node[draw, rounded corners, fill=blue!10] (t1) {Token 1: $[ -0.18, 0.55, \dots ]$};
    \node[draw, rounded corners, fill=blue!10, below=of t1] (t2) {Token 2: $[ 0.22, 1.32, \dots ]$};
    \node[draw, rounded corners, fill=blue!10, below=of t2] (t3) {Token 3: $[ 0.43, -1.30, \dots ]$};
    \node[draw, rounded corners, fill=blue!10, below=of t3] (t4) {Token 4: $[ 1.02, -1.90, \dots ]$};
    \node[draw, rounded corners, fill=blue!10, below=of t4] (t5) {Token 5: $[ 1.78, -0.82, \dots ]$};
    
    \node[draw, right=1.5cm of t3, fill=orange!20, minimum height=3cm, align=center] (concat) {Ép phẳng\\(Concatenate)\\ $\rightarrow 1 \times 20$};
    
    \draw[->, thick] (t1.east) -- (concat.west);
    \draw[->, thick] (t2.east) -- (concat.west);
    \draw[->, thick] (t3.east) -- (concat.west);
    \draw[->, thick] (t4.east) -- (concat.west);
    \draw[->, thick] (t5.east) -- (concat.west);
    
    \node[draw, right=1.5cm of concat, fill=green!20, align=center] (mlp) {Linear (20 $\rightarrow$ 16)\\ ReLU \\ Linear (16 $\rightarrow$ 8)};
    \draw[->, thick] (concat.east) -- (mlp.west);
    
    \node[draw, right=1.5cm of mlp, fill=red!20] (out) {Softmax $\rightarrow$ "is"};
    \draw[->, thick] (mlp.east) -- (out.west);
\end{tikzpicture}
\end{center}
\end{frame}

\begin{frame}{Ba Điểm nghẽn Bản chất của MLP}
\begin{alertblock}{\textbf{1. Cửa sổ cố định (Fixed Window)}}
Ma trận W gắn cứng với kích thước cố định L.
\begin{itemize}
    \item Câu ngắn: Bắt buộc nhồi padding dư thừa.
    \item Câu dài hơn L: Cắt cụt, mất hoàn toàn dữ liệu.
\end{itemize}
\end{alertblock}

\begin{alertblock}{\textbf{2. Mất tính tuần tự (Non-sequential)}}
Ép phẳng làm mất trục thời gian. Mạng xem từ ở vị trí 1 và từ ở vị trí 5 là hai tọa độ độc lập, không nhận diện được quy luật dịch chuyển.
\end{alertblock}

\begin{alertblock}{\textbf{3. Bùng nổ tham số (Parameter Explosion)}}
Số tham số tầng Linear = $W_1 \times (L \times d)$. Độ dài ngữ cảnh tăng gấp đôi khiến trọng số tăng gấp đôi, dễ gây quá khớp (overfitting) và tốn bộ nhớ.
\end{alertblock}
\end{frame}


\begin{frame}{Bước tiến 1D-CNN: Cửa sổ Trượt Kernel (N-gram)}
\textit{1D-CNN khắc phục việc gắn cứng vị trí bằng cách dùng Kernel trượt qua từng bước thời gian:}

\begin{center}
\begin{tikzpicture}[scale=0.85, every node/.style={scale=0.85}]
    % Input Matrix
    \matrix[matrix of nodes, nodes={draw, minimum width=2.5cm, minimum height=0.6cm, fill=blue!10}, row sep=0.1cm] (input) {
        "We" \\
        "are" \\
        "learning" \\
        "AI" \\
        "[PAD]" \\
    };
    
    % Kernel
    \node[draw, right=3cm of input-1-1, fill=orange!20, minimum width=3cm, minimum height=1.3cm, align=center, yshift=-0.35cm] (kernel) {Kernel $k=2$\\ Trượt từng bước};
    
    % Connections
    \draw[->, dashed, thick, color=gray] (input-1-1.east) -- (kernel.west);
    \draw[->, dashed, thick, color=gray] (input-2-1.east) -- (kernel.west);
    
    % Output
    \node[right=2.5cm of kernel] (out) {
        \begin{tabular}{c}
        Feature Map \\
        $c_1 = 1.81$ \\
        $c_2 = 0.62$ \\
        $c_3 = -0.16$ \\
        $c_4 = 1.47$ 
        \end{tabular}
    };
    \draw[->, thick] (kernel.east) -- (out.west);
    
    \node[below=1cm of out, draw, fill=green!20] (pool) {Max-Pooling $\rightarrow v = 1.81$};
    \draw[->, thick] (out.south) -- (pool.north);
\end{tikzpicture}
\end{center}
\end{frame}

\begin{frame}{Vì sao 1D-CNN vẫn chưa tối ưu cho chuỗi dài?}
\begin{alertblock}{\textbf{Vấn đề 1: Tầm nhìn bị bó hẹp (Limited Receptive Field)}}
Kernel ($k=2$) chỉ bắt được từng cặp từ đứng cạnh nhau (Bigram). Không thể liên kết chủ ngữ ở đầu câu với vị ngữ ở cuối một đoạn văn dài.
\end{alertblock}

\vspace{0.5cm}
\begin{alertblock}{\textbf{Vấn đề 2: Max-Pooling xóa bỏ thứ tự thời gian}}
\begin{itemize}
    \item $c_1$ ("We are") = $1.81$
    \item $c_2$ ("are learning") = $0.62$
    \item $c_3$ ("learning AI") = $0.00$
    \item $c_4$ ("AI [PAD]") = $1.47$
\end{itemize}
Max-Pooling lấy giá trị lớn nhất là $1.81$, nhưng \textbf{hoàn toàn quên} $1.81$ xuất hiện ở đầu hay cuối câu!
\end{alertblock}
\end{frame}


\begin{frame}{Bảng So sánh: MLP vs. 1D-CNN vs. RNN}
\begin{table}
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{>{\bfseries}l p{4cm} p{4cm} p{4.5cm}}
\toprule
Tiêu chí đối sánh & MLP (Feedforward) & 1D-CNN (Convolutional) & Recurrent Neural Network (RNN) \\
\midrule
Độ dài ngữ cảnh & Cố định cứng, phải đệm padding & Cửa sổ trượt cố định theo $k$ & \textcolor{accentteal}{\textbf{Co giãn linh hoạt theo độ dài chuỗi}} \\
\addlinespace
Bảo toàn thứ tự & Bị xóa sạch sau phép Flatten & Giữ được trật tự cục bộ N-gram & \textcolor{accentteal}{\textbf{Duy trì trật tự toàn vẹn theo thời gian}} \\
\addlinespace
Chia sẻ trọng số & Không chia sẻ (Độc lập vị trí) & Chia sẻ trọng số theo không gian & \textcolor{accentteal}{\textbf{Chia sẻ trọng số xuyên suốt thời gian}} \\
\addlinespace
Bộ nhớ tích lũy & Không có bộ nhớ & Gián tiếp qua độ sâu filter & \textcolor{accentteal}{\textbf{Bộ nhớ trạng thái ẩn ($h_t$) trực tiếp}} \\
\addlinespace
Tăng trưởng tham số & Tăng vọt theo độ dài $(L \cdot d)$ & Phụ thuộc số filter, độc lập $L$ & \textcolor{accentteal}{\textbf{Hằng số, hoàn toàn không phụ thuộc $L$}} \\
\bottomrule
\end{tabular}%
}
\end{table}
\end{frame}

\begin{frame}{Ý tưởng Cốt lõi của RNN: Trạng thái Ẩn ($h_t$)}
\textbf{Trực giác:} Con người không bắt đầu tư duy lại từ đầu ở từng chữ cái, mà liên tục duy trì một dòng ý thức nén thông tin quá khứ.

\vspace{0.6cm}
\begin{center}
\begin{tikzpicture}[node distance=1.5cm, auto, thick]
    % Nodes
    \node (x1) [align=center] {$t=1$ \\ "Tôi"};
    \node (x2) [right=2cm of x1, align=center] {$t=2$ \\ "đang"};
    \node (x3) [right=2cm of x2, align=center] {$t=3$ \\ "học"};
    
    \node (h0) [below left=1cm and 0.5cm of x1] {$h_0=0$};
    
    \node (rnn1) [draw, fill=blue!10, rounded corners, below=1cm of x1, minimum width=1.5cm, minimum height=1cm] {RNN};
    \node (rnn2) [draw, fill=blue!10, rounded corners, below=1cm of x2, minimum width=1.5cm, minimum height=1cm] {RNN};
    \node (rnn3) [draw, fill=blue!10, rounded corners, below=1cm of x3, minimum width=1.5cm, minimum height=1cm] {RNN};
    
    % Arrows
    \draw[->] (x1) -- (rnn1);
    \draw[->] (x2) -- (rnn2);
    \draw[->] (x3) -- (rnn3);
    
    \draw[->] (h0) -- (rnn1) node[midway, above] {};
    \draw[->] (rnn1) -- (rnn2) node[midway, above] {$h_1$};
    \draw[->] (rnn2) -- (rnn3) node[midway, above] {$h_2$};
    \draw[->] (rnn3) -- ++(2,0) node[midway, above] {$h_3$};
\end{tikzpicture}
\end{center}
\vspace{0.2cm}
\textbf{$h_t$ chính là "Trí nhớ" nén toàn bộ quá khứ:}
\begin{itemize}
    \item $h_1$: Nhớ từ "Tôi"
    \item $h_2$: Nhớ ngữ cảnh ("Tôi" + "đang")
    \item $h_3$: Nhớ toàn bộ ("Tôi" + "đang" + "học")
\end{itemize}
\end{frame}

\begin{frame}{Công thức Toán học \& Bộ ba Trọng số ($W, U, V$)}
Trái tim toán học của mạng RNN được định nghĩa qua hai phương trình cơ sở:
\begin{align*}
    h_t &= \tanh(\mathbf{W} \cdot x_t + \mathbf{U} \cdot h_{t-1} + b_h) \\
    \hat{y}_t &= \mathbf{V} \cdot h_t + b_y
\end{align*}

\begin{columns}[T]
\begin{column}{0.6\textwidth}
\begin{center}
\begin{tikzpicture}[node distance=1.5cm, thick]
    \node (h_prev) [draw, fill=gray!20] {$h_{t-1}$ (Cũ)};
    \node (x_t) [draw, fill=green!20, right=2cm of h_prev] {Đầu vào $x_t$};
    
    \node (h_t) [draw, fill=blue!20, rounded corners, minimum width=4cm, minimum height=1cm, above right=1cm and -1.5cm of h_prev] {TRẠNG THÁI ẨN ($h_t$)};
    
    \node (y_t) [draw, fill=orange!20, rounded corners, minimum width=4cm, minimum height=1cm, above=1.5cm of h_t] {KẾT QUẢ DỰ ĐOÁN ($y_t$)};
    
    \draw[->] (h_prev) -- (h_t.south west) node[midway, left, align=right] {Ma trận $U$\\ \scriptsize(Hidden-to-Hidden)};
    \draw[->] (x_t) -- (h_t.south east) node[midway, right, align=left] {Ma trận $W$\\ \scriptsize(Input-to-Hidden)};
    \draw[->] (h_t) -- (y_t) node[midway, right] {Ma trận $V$ \scriptsize(Hidden-to-Output)};
\end{tikzpicture}
\end{center}
\end{column}
\begin{column}{0.38\textwidth}
\begin{block}{\textbf{Vai trò}}
\begin{itemize}
    \item \textbf{U:} Duy trì trí nhớ cũ $h_{t-1}$.
    \item \textbf{W:} Tiếp nhận thông tin mới từ quan sát $x_t$.
    \item \textbf{V:} Đọc bộ nhớ $h_t$ để đưa ra quyết định.
\end{itemize}
\end{block}
\end{column}
\end{columns}
\end{frame}

\begin{frame}{Nguyên lý Chia sẻ Trọng số (Weight Sharing)}
\textit{Mạng xử lý chuỗi dài 5 bước hay 1.000 bước đều \textbf{dùng chung một bộ ma trận duy nhất}:}

\vspace{0.4cm}
\begin{center}
\begin{tabular}{ll}
Thời điểm $t=1$: & $h_1 = \tanh( \mathbf{W} \cdot x_1 + \mathbf{U} \cdot h_0 + b ) \rightarrow y_1 = \mathbf{V} \cdot h_1$ \\
Thời điểm $t=2$: & $h_2 = \tanh( \mathbf{W} \cdot x_2 + \mathbf{U} \cdot h_1 + b ) \rightarrow y_2 = \mathbf{V} \cdot h_2$ \\
Thời điểm $t=3$: & $h_3 = \tanh( \mathbf{W} \cdot x_3 + \mathbf{U} \cdot h_2 + b ) \rightarrow y_3 = \mathbf{V} \cdot h_3$ \\
\end{tabular}
\end{center}

\vspace{0.2cm}
\begin{exampleblock}{\textbf{Lợi ích Cốt lõi}}
\begin{itemize}
    \item \textbf{Tổng số lượng tham số} độc lập tuyệt đối với chiều dài chuỗi dữ liệu.
    \item \textbf{Tổng quát hóa:} Giúp mô hình nhận diện được mẫu hình tương đồng dù nó xuất hiện ở đầu hay cuối chuỗi.
\end{itemize}
\end{exampleblock}
\end{frame}

\begin{frame}{Đồ thị Tính toán dạng Mở cuộn (Unfolded Computation Graph)}
Một ô nhớ RNN hồi quy tương đương với một \textbf{Mạng truyền thẳng cực sâu} có độ sâu bằng $T$:

\vspace{0.5cm}
\begin{columns}[c]
\begin{column}{0.25\textwidth}
\centering
\textbf{DẠNG CUỘN}\\ (Folded)\\
\vspace{0.4cm}
\begin{tikzpicture}[thick]
    \node (x) {$x_t$};
    \node (h) [draw, fill=blue!10, rounded corners, minimum size=1cm, above=1cm of x] {$h_t$};
    \node (y) [above=1cm of h] {$y_t$};
    
    \draw[->] (x) -- (h) node[midway, right] {$W$};
    \draw[->] (h) -- (y) node[midway, right] {$V$};
    \draw[->] (h.east) arc(-90:200:0.4cm) node[above right] {$U$};
\end{tikzpicture}
\end{column}

\begin{column}{0.1\textwidth}
\centering
$\longrightarrow$
\end{column}

\begin{column}{0.6\textwidth}
\centering
\textbf{DẠNG MỞ CUỘN}\\ (Unfolded)\\
\vspace{0.4cm}
\begin{tikzpicture}[node distance=1.5cm, thick]
    \node (x1) {$x_1$};
    \node (x2) [right=of x1] {$x_2$};
    \node (xT) [right=of x2] {$x_T$};
    
    \node (h1) [draw, fill=blue!10, rounded corners, minimum size=0.8cm, above=0.8cm of x1] {$h_1$};
    \node (h2) [draw, fill=blue!10, rounded corners, minimum size=0.8cm, above=0.8cm of x2] {$h_2$};
    \node (hT) [draw, fill=blue!10, rounded corners, minimum size=0.8cm, above=0.8cm of xT] {$h_T$};
    
    \node (y1) [above=0.8cm of h1] {$y_1$};
    \node (y2) [above=0.8cm of h2] {$y_2$};
    \node (yT) [above=0.8cm of hT] {$y_T$};
    
    \draw[->] (x1) -- (h1) node[midway, right] {$W$};
    \draw[->] (x2) -- (h2) node[midway, right] {$W$};
    \draw[->] (xT) -- (hT) node[midway, right] {$W$};
    
    \draw[->] (h1) -- (h2) node[midway, above] {$U$};
    \draw[->] (h2) -- (hT) node[midway, above, dashed] {$U$};
    
    \draw[->] (h1) -- (y1) node[midway, right] {$V$};
    \draw[->] (h2) -- (y2) node[midway, right] {$V$};
    \draw[->] (hT) -- (yT) node[midway, right] {$V$};
\end{tikzpicture}
\end{column}
\end{columns}
\end{frame}

\begin{frame}{Các Dạng Kiến trúc Tương tác Chuỗi của RNN}
\begin{itemize}
    \item \textbf{One-to-Many:} Ảnh $\rightarrow$ RNN $\rightarrow$ $[y_1, y_2, y_3]$ (Sinh chú thích ảnh)
    \item \textbf{Many-to-One:} $[x_1, x_2, x_3]$ $\rightarrow$ RNN $\rightarrow$ $y$ (Phân loại cảm xúc review)
    \item \textbf{Many-to-Many (Đồng bộ):} $[x_1, x_2, x_3]$ $\rightarrow$ RNN $\rightarrow$ $[y_1, y_2, y_3]$ (Gán nhãn từ loại)
    \item \textbf{Many-to-Many (Seq2Seq):} $[x_1, x_2]$ $\rightarrow$ Encoder $\rightarrow$ Decoder $\rightarrow$ $[y_1, y_2]$ (Dịch máy)
\end{itemize}
\end{frame}

\begin{frame}{Cơ chế Huấn luyện BPTT (Backpropagation Through Time)}
Mô hình tính toán sai số tại mọi thời điểm và lan truyền ngược gradient ngược dòng thời gian từ $T$ về $1$:

\vspace{0.5cm}
\begin{center}
\begin{tikzpicture}[node distance=1.5cm, thick]
    \node (x1) {$x_1$};
    \node (h1) [draw, fill=blue!10, right=1cm of x1] {$h_1$};
    \node (h2) [draw, fill=blue!10, right=1.5cm of h1] {$h_2$};
    \node (h3) [draw, fill=blue!10, right=1.5cm of h2] {$h_3$};
    \node (L3) [right=1.5cm of h3, text=red] {Loss $L_3$};
    
    \draw[->] (x1) -- (h1);
    \draw[->] (h1) -- (h2) node[midway, above] {Forward};
    \draw[->] (h2) -- (h3);
    \draw[->] (h3) -- (L3);
    
    \draw[->, red, dashed, bend left=45] (L3) to node[midway, below] {$\frac{\partial L}{\partial h_3}$} (h3);
    \draw[->, red, dashed, bend left=45] (h3) to node[midway, below] {$\frac{\partial L}{\partial h_2}$} (h2);
    \draw[->, red, dashed, bend left=45] (h2) to node[midway, below] {$\frac{\partial L}{\partial h_1}$} (h1);
\end{tikzpicture}
\end{center}

\vspace{0.4cm}
Công thức Gradient cho $U$:
$$\frac{\partial L}{\partial U} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial L_t}{\partial h_t} \cdot \left( \prod_{j=k+1}^t \frac{\partial h_j}{\partial h_{j-1}} \right) \cdot \frac{\partial h_k}{\partial U}$$
\end{frame}

\begin{frame}{Vấn đề Triệt tiêu Gradient (Vanishing Gradient)}
\textbf{Bản chất:} Phép nhân chuỗi ma trận $U$ liên tiếp qua $T-k$ bước thời gian:

$$ \frac{\partial L}{\partial h_k} = \frac{\partial L}{\partial h_t} \times [ \text{diag}(1 - h^2) \cdot U ] \times \dots \times [ \text{diag}(1 - h^2) \cdot U ] $$
(nhân $T-k$ lần, đạo hàm $\tanh(z)$ nằm trong $(0, 1]$)

\vspace{0.4cm}
\begin{alertblock}{\textbf{Hậu quả khi Trị riêng lớn nhất của $U < 1$}}
$$ \Vert U^{T-k} \Vert \longrightarrow 0 \quad (\text{khi chuỗi dài ra}) $$
Tín hiệu đạo hàm ở các bước đầu tiên suy giảm theo hàm mũ về 0. Trọng số không thể cập nhật để học các liên kết ngữ cảnh quá khứ xa.
\end{alertblock}
\end{frame}


\begin{frame}{Hiện tượng Nổ Gradient \& Gradient Clipping}
\begin{alertblock}{\textbf{Hiện tượng Nổ Gradient (Exploding Gradient)}}
\begin{itemize}
    \item Khi trị riêng lớn nhất của $U > 1$: $\Vert U^{T-k} \Vert$ bùng nổ vô tận theo hàm mũ.
    \item Bước nhảy trọng số quá lớn phá hủy vùng cực tiểu, làm tràn số (NaN / Inf).
\end{itemize}
\end{alertblock}

\vspace{0.4cm}
\begin{exampleblock}{\textbf{Giải pháp: Cắt tỉa Gradient (Gradient Norm Clipping)}}
$$ g_{\text{clipped}} = g \cdot \frac{\theta}{\Vert g \Vert} \quad \text{khi} \Vert g \Vert > \theta $$
\textit{Vector ban đầu quá dài sẽ bị co ngắn lại cho bằng $\theta$, nhưng vẫn giữ nguyên hướng (hướng Gradient).}
\end{exampleblock}
\end{frame}

\begin{frame}{Tổng kết Điểm nghẽn của Simple RNN}
\begin{alertblock}{\textbf{1. Không có Cơ chế Chọn lọc (Unselective Memory)}}
Mọi bước thời gian đều bị nén qua một hàm $\tanh$ duy nhất, thông tin quan trọng dễ bị thông tin rác làm loãng.
\end{alertblock}

\begin{alertblock}{\textbf{2. Mất Trí nhớ Dài hạn (Short-term Memory Horizon)}}
Do triệt tiêu gradient, RNN thực tế chỉ nhớ được từ 5 đến 10 bước thời gian gần nhất.
\end{alertblock}

\begin{alertblock}{\textbf{3. Bắt buộc Tính toán Tuần tự (Sequential Bottleneck)}}
$h_t$ chỉ tính được khi đã có $h_{t-1} \rightarrow$ KHÔNG THỂ SONG SONG HÓA trên GPU như Transformer hay CNN.
\end{alertblock}
\end{frame}

\begin{frame}{Thiết lập Thực nghiệm Chuỗi Tài chính}
\textit{Kiểm chứng hiệu năng của RNN trên 2 tập dữ liệu thực tế lớn từ Kaggle:}
\vspace{0.4cm}

\begin{itemize}
    \item \textbf{Tập 1:} Chuỗi giá vàng \& bạc hàng ngày (Gold \& Silver daily prices, 1968–2021).
    \item \textbf{Tập 2:} Chuỗi biến động giá \& khối lượng cổ phiếu Amazon (AMZN, 1997–2023).
\end{itemize}
\vspace{0.4cm}
\begin{block}{\textbf{Cấu hình Thực nghiệm}}
\begin{itemize}
    \item \textbf{Cửa sổ trượt:} 30 ngày lịch sử ($L=30$) để dự đoán bước tiếp theo ($t+1$).
    \item \textbf{Baseline đối chứng:} Phương pháp Naive / Persistence ($\hat{y}_{t+1} = y_t$ — Lấy giá hôm nay đoán cho ngày mai).
\end{itemize}
\end{block}
\end{frame}

\begin{frame}{Kết quả Thực nghiệm \& Hiện tượng Nghịch lý}
Bảng so sánh độ lệch sai số căn quân phương (RMSE trên tập Test):

\vspace{0.4cm}
\begin{table}
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{l c c c p{4.5cm}}
\toprule
\textbf{Tập dữ liệu} & \textbf{Naive Baseline} & \textbf{PyTorch RNN} & \textbf{Keras RNN} & \textbf{Đánh giá} \\
\midrule
Giá Vàng (Gold) & 15.48 & \textbf{15.45} & 16.42 & \textcolor{red}{\textit{Keras RNN chạy tệ hơn cả Naive}} \\
Cổ phiếu AMZN & 3.14 & \textbf{3.13} & 3.18 & \textcolor{gray}{\textit{Xấp xỉ phương pháp Naive}} \\
\bottomrule
\end{tabular}%
}
\end{table}

\vspace{0.4cm}
\begin{alertblock}{\textbf{Nghịch lý Quan sát}}
Một mạng nơ-ron học sâu phức tạp huấn luyện hàng chục epoch kết quả lại chỉ tương đương, thậm chí kém hơn cả một thuật toán "lười biếng" lấy giá hôm trước làm dự đoán!
\end{alertblock}
\end{frame}

\begin{frame}{Bản chất Thất bại: Dịch chuyển Phân phối (Distribution Shift)}
Tại sao Simple RNN lại thất bại ở bài toán dự báo giá kim loại?

\vspace{0.4cm}
\begin{alertblock}{\textbf{Phân phối Dữ liệu Train vs Test}}
\begin{itemize}
    \item \textbf{Tập Train:} Giá cao nhất = $850.00$ USD (ĐÃ ĐƯỢC HỌC - Nội suy tốt)
    \item \textbf{Tập Test:} Giá thấp nhất = $1,049.40$ USD (CHƯA GẶP BAO GIỜ - Ngoại suy bất lực)
    \item $\rightarrow$ 100\% dữ liệu Test > Train Max!
\end{itemize}
\end{alertblock}

\vspace{0.2cm}
\begin{exampleblock}{\textbf{Bài học \& Giải pháp khắc phục}}
\begin{itemize}
    \item Mạng nơ-ron không thể ngoại suy trên vùng số liệu mới.
    \item \textbf{Giải pháp:} Không dự đoán mức giá tuyệt đối, phải chuyển thành tỷ suất sinh lời dừng (\textbf{Log-return}): $r_t = \ln(P_t / P_{t-1})$.
\end{itemize}
\end{exampleblock}
\end{frame}


\begin{frame}{Bước Tiến hóa LSTM: Đường dẫn Trí nhớ Dài hạn}
Long Short-Term Memory bổ sung đường truyền thẳng \textbf{Cell State ($C_t$)} không bị cản trở bởi phép nhân ma trận lặp lại:

\vspace{0.4cm}
\begin{center}
\begin{tikzpicture}[thick, node distance=1.5cm, scale=0.8, every node/.style={scale=0.8}]
    % Nodes
    \node (ct_prev) {$C_{t-1}$};
    \node[circle, draw, right=2cm of ct_prev] (mul1) {$\times$};
    \node[circle, draw, right=3cm of mul1] (add) {$+$};
    \node[right=2cm of add] (ct) {$C_t$};
    
    \draw[->] (ct_prev) -- (mul1);
    \draw[->] (mul1) -- (add);
    \draw[->] (add) -- (ct);
    
    \node[below=1.5cm of mul1, draw, fill=red!20] (forget) {Forget Gate ($f_t$)};
    \node[below=1.5cm of add, draw, fill=green!20] (input) {Input Gate ($i_t$)};
    \node[right=1cm of input, draw, fill=orange!20] (output) {Output Gate ($o_t$)};
    
    \draw[->] (forget) -- (mul1) node[midway, right] {Bỏ cái cũ};
    \draw[->] (input) -- (add) node[midway, right] {Ghi cái mới};
\end{tikzpicture}
\end{center}

\vspace{0.2cm}
\begin{itemize}
    \item \textbf{Cổng Quên ($f_t$):} Xóa bỏ các ký ức không còn phù hợp.
    \item \textbf{Cổng Ghi ($i_t$):} Chọn lọc thông tin mới đáng chú ý nạp vào.
    \item \textbf{Cổng Xuất ($o_t$):} Quyết định trích xuất thông tin gì ra ngoài trạng thái ẩn.
\end{itemize}
\end{frame}

\begin{frame}{Tinh giản với GRU (Gated Recurrent Unit)}
GRU rút gọn cấu trúc của LSTM, gộp Cell State và Hidden State thành một trạng thái duy nhất:

\vspace{0.5cm}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{block}{\textbf{Cổng Cập nhật (Update Gate $z_t$)}}
Cân bằng giữa việc giữ lại trí nhớ cũ và ghi đè trạng thái mới. (Gộp vai trò của Forget và Input gate).
\end{block}
\end{column}

\begin{column}{0.48\textwidth}
\begin{block}{\textbf{Cổng Đặt lại (Reset Gate $r_t$)}}
Quyết định xem trạng thái quá khứ sẽ kết hợp bao nhiêu với đầu vào hiện tại.
\end{block}
\end{column}
\end{columns}

\vspace{0.5cm}
\begin{exampleblock}{\textbf{Tối ưu hiệu suất}}
Giảm bớt 25\% số lượng tham số so với LSTM, tốc độ huấn luyện nhanh hơn rõ rệt mà hiệu quả thực nghiệm tương đương.
\end{exampleblock}
\end{frame}


\begin{frame}{Tổng kết \& Bức tranh Toàn cảnh}
\begin{center}
\textbf{TIẾN TRÌNH CÔNG NGHỆ MÔ HÌNH HÓA DỮ LIỆU CHUỖI}
\end{center}
\vspace{0.2cm}
\begin{table}
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{p{3.5cm} p{3.5cm} p{3.5cm} p{3.5cm}}
\toprule
\textbf{MLP / 1D-CNN} (2012) & \textbf{RNN THUẦN} (1986-1990) & \textbf{LSTM / GRU} (1997-2014) & \textbf{TRANSFORMER} (2017+) \\
\midrule
$\bullet$ Ép phẳng, trượt cục bộ & $\bullet$ Bộ nhớ ẩn $h_t$ & $\bullet$ Cơ chế cổng kiểm soát & $\bullet$ Cơ chế Self-Attention \\
$\bullet$ Mất tính tuần tự dài & $\bullet$ Bị triệt tiêu gradient & $\bullet$ Nhớ dài hạn rất tốt & $\bullet$ Xử lý song song tuyệt đối \\
$\bullet$ Chỉ phù hợp chuỗi ngắn & $\bullet$ Dễ nổ đạo hàm & $\bullet$ Chuẩn mực Time-series & $\bullet$ Thống trị lĩnh vực LLM \\
\bottomrule
\end{tabular}%
}
\end{table}

\vspace{0.4cm}
\begin{block}{\textbf{Thông điệp kết luận}}
Simple RNN đã đặt nền móng lý thuyết mang tính lịch sử về việc chia sẻ trọng số thời gian và trạng thái ẩn. Hiểu rõ các điểm nghẽn toán học của RNN chính là chìa khóa để làm chủ toàn bộ các mô hình học sâu chuỗi hiện đại.
\end{block}
\end{frame}

\end{document}
"""

with open("rnn_slides.tex", "w", encoding="utf-8") as f:
    f.write(preamble)

print("Generated rnn_slides.tex")
