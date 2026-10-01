import os

latex_content = r"""\documentclass[12pt,a4paper]{article}

% ==============================================================================
% GÓI THƯ VIỆN CƠ BẢN VÀ HỖ TRỢ TIẾNG VIỆT
% ==============================================================================
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage[vietnamese]{babel}

\usepackage{amsmath, amssymb, amsthm, mathtools}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs, multirow, makecell, tabularx, longtable, array}
\usepackage{geometry}
\geometry{
    a4paper,
    left=25mm,
    right=20mm,
    top=25mm,
    bottom=25mm
}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{tcolorbox}
\tcbuselibrary{breakable}
\usepackage{hyperref}
\usepackage{tikz}
\usepackage{float}

% Cấu hình đường dẫn thư mục ảnh
\graphicspath{{./}{figures/}}

% Cấu hình Hyperlink
\hypersetup{
    colorlinks=true,
    linkcolor=blue!75!black,
    citecolor=red!75!black,
    urlcolor=teal!80!black
}

% Cấu hình Header & Footer
\setlength{\headheight}{15pt}
\addtolength{\topmargin}{-3pt}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textit{Học viện Công nghệ Bưu chính Viễn thông -- PTIT}}
\fancyhead[R]{\small\textit{Báo cáo Kỹ thuật Assignment 06 -- LTHTTM}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.6pt}
\renewcommand{\footrulewidth}{0.4pt}

% Cấu hình Code Listing
\lstset{
    language=Python,
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{blue!80!black}\bfseries,
    commentstyle=\color{green!50!black}\itshape,
    stringstyle=\color{red!70!black},
    numbers=left,
    numberstyle=\tiny\color{gray},
    stepnumber=1,
    numbersep=8pt,
    backgroundcolor=\color{gray!5},
    frame=single,
    rulecolor=\color{gray!30},
    breaklines=true,
    breakatwhitespace=true,
    showstringspaces=false,
    tabsize=4
}

% Định dạng tiêu đề các mục
\titleformat{\section}{\large\bfseries\color{blue!85!black}}{\thesection}{1em}{}[\titlerule]
\titleformat{\subsection}{\normalsize\bfseries\color{cyan!75!black}}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\small\bfseries\color{black}}{\thesubsubsection}{1em}{}

% Khối ghi chú nổi bật
\newtcolorbox{mybox}[1]{
    colback=blue!5!white,
    colframe=blue!75!black,
    fonttitle=\bfseries,
    title=#1,
    arc=2mm,
    boxrule=1pt
}

% Khối chú thích & phân tích biểu đồ chuyên sâu
\newtcolorbox{chartbox}[1][]{
    colback=blue!2!white,
    colframe=blue!70!black,
    fonttitle=\bfseries\small,
    coltitle=white,
    arc=1.5mm,
    boxrule=0.8pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm,
    breakable,
    title=#1
}

% Cấu hình cột bảng tự co giãn và căn lề
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}

% ==============================================================================
% BẮT ĐẦU TÀI LIỆU
% ==============================================================================
\begin{document}

% ==============================================================================
% TRANG BÌA CHUẨN KHUNG VIỀN CỔ ĐIỂN VÀ HỌA TIẾT 4 GÓC THEO FILE DOCX
% ==============================================================================
\begin{titlepage}
    \begin{tikzpicture}[remember picture, overlay]
        % 1. Đường viền khung ngoài dày
        \draw[line width=2.2pt, color=black]
            ([xshift=15mm, yshift=-15mm]current page.north west)
            rectangle
            ([xshift=-15mm, yshift=15mm]current page.south east);
        
        % 2. Đường viền khung trong mảnh
        \draw[line width=0.8pt, color=black]
            ([xshift=17.5mm, yshift=-17.5mm]current page.north west)
            rectangle
            ([xshift=-17.5mm, yshift=17.5mm]current page.south east);
    \end{tikzpicture}

    \centering
    \vspace*{0.2cm}
    {\large \textbf{HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG}}\\[0.25cm]
    {\large \textbf{KHOA CÔNG NGHỆ THÔNG TIN 1}}\\[0.2cm]
    \rule{5cm}{1pt}\\[0.9cm]

    % Logo PTIT
    \begin{center}
        \IfFileExists{figures/logo_ptit.png}{%
            \includegraphics[width=3.4cm, height=4.2cm, keepaspectratio]{figures/logo_ptit.png}
        }{%
            \begin{tcolorbox}[colback=red!5!white, colframe=red!75!black, width=3.8cm, height=3.8cm, arc=2mm, halign=center, valign=center]
                \Large \textbf{\color{red!80!black}PTIT}\\[0.1cm]
                \footnotesize \textbf{\color{black}LOGO}
            \end{tcolorbox}
        }
    \end{center}

    \vspace{0.6cm}

    {\Large \textbf{BÁO CÁO KỸ THUẬT ASSIGNMENT 06}}\\[0.3cm]
    {\large \textbf{MÔN HỌC: LẬP TRÌNH HỆ THỐNG THÔNG MINH}}\\[0.5cm]
    {\Large \textbf{\color{blue!85!black}MẠNG NƠ-RON HỒI QUY (RNN) TỪ CƠ SỞ LÝ THUYẾT ĐẾN ỨNG DỤNG DỰ BÁO CHUỖI THỜI GIAN}}\\[0.3cm]
    {\normalsize \textit{Nghiên cứu Giải tích, Hiện thực Hóa Mã nguồn thuần (NumPy) và Đối chuẩn Thực nghiệm trên Keras và PyTorch (Gold Price, AMZN)}}

    \vspace{0.8cm}

    \begin{flushleft}
        \hspace{1.6cm}
        \begin{tabular}{p{5.0cm} p{0.5cm} l}
            \textbf{Giảng viên hướng dẫn} & : & \textbf{PGS.TS. Trần Đình Quế} \\[0.3cm]
            \textbf{Lớp}                  & : & \textbf{D23CTPM01} \\[0.3cm]
            \textbf{Nhóm học phần}        & : & \textbf{CT01} \\[0.3cm]
            \textbf{Thành viên thực hiện} & : & \textbf{Nguyễn Nam Hải} \\[0.3cm]
            \textbf{Mã sinh viên}         & : & \textbf{B23DCCN277} \\[0.3cm]
        \end{tabular}
    \end{flushleft}

    \vfill
    {\large \textbf{Hà Nội -- 2026}}
    \vspace*{0.3cm}
\end{titlepage}

% ==============================================================================
% MỤC LỤC BÁO CÁO KỸ THUẬT
% ==============================================================================
\newpage
\renewcommand{\contentsname}{MỤC LỤC BÁO CÁO KỸ THUẬT ASSIGNMENT 06}
\tableofcontents
\newpage

% ==============================================================================
% DANH MỤC HÌNH VẼ & BẢNG BIỂU
% ==============================================================================
\phantomsection
\addcontentsline{toc}{section}{DANH MỤC HÌNH VẼ}
\listoffigures

\vspace{0.8cm}

\phantomsection
\addcontentsline{toc}{section}{DANH MỤC BẢNG BIỂU}
\listoftables

\newpage

% ==============================================================================
% TÓM TẮT BÁO CÁO (ABSTRACT)
% ==============================================================================
\phantomsection
\addcontentsline{toc}{section}{TÓM TẮT BÁO CÁO (ABSTRACT)}
\section*{TÓM TẮT BÁO CÁO (ABSTRACT)}

Báo cáo Kỹ thuật Assignment 06 trình bày nghiên cứu hệ thống và khảo sát thực nghiệm chuyên sâu về Mạng nơ-ron Hồi quy (Recurrent Neural Network -- RNN), tập trung vào **bản chất giải tích của dữ liệu chuỗi thời gian và sự lưu trữ trạng thái ẩn (Hidden State)**. Tiếp nối tinh thần từ Assignment 05 về "Hợp hàm toán học", báo cáo này làm rõ cách thức mà một mạng nơ-ron học được những phụ thuộc thời gian (Temporal Dependencies) thông qua các vòng lặp phản hồi và thuật toán Backpropagation Through Time (BPTT).

Báo cáo không chỉ khảo sát mặt lý thuyết mà còn tiến hành bóc tách toàn diện vấn đề **Vanishing Gradient** (Suy thoái Gradient), rào cản lớn nhất của Vanilla RNN. Về phương diện thực hành, báo cáo thực hiện 3 bước triển khai độc lập: (1) **Xây dựng RNN thuần (From Scratch)** hoàn toàn bằng NumPy; (2) **Triển khai bằng PyTorch**; và (3) **Triển khai bằng Keras/TensorFlow**.

Hai tập dữ liệu tài chính thực tế mang đặc thù chuỗi thời gian được phân tích và đánh giá:
\begin{enumerate}[leftmargin=*]
    \item **Gold Price (Giá Vàng Thế Giới)**: Dữ liệu vĩ mô dài hạn từ năm 1968, với các chu kỳ đột biến đan xen chu kỳ bão hòa.
    \item **AMZN Stock (Cổ phiếu Amazon)**: Dữ liệu chứng khoán thị trường biến động mạnh, tần suất dao động cao.
\end{enumerate}

Cùng với 7 sổ tay Jupyter, dự án còn tích hợp một hệ thống phần mềm hoàn chỉnh bao gồm Backend (FastAPI) và Frontend tương tác cho phép chọn khoảng thời gian tùy chỉnh để vẽ biểu đồ trực quan giữa Giá Thực tế (Actual) và Giá Dự báo (Prediction). Kết quả cuối cùng mở ra những góc nhìn sâu sắc về hiện tượng "trễ pha" (Lagging) cố hữu của RNN cổ điển, tạo tiền đề để chuyển giao lên các kiến trúc tiên tiến hơn như LSTM và GRU.

\newpage

% ==============================================================================
% TÀI NGUYÊN THỰC NGHIỆM VÀ HƯỚNG DẪN CÀI ĐẶT
% ==============================================================================
\phantomsection
\addcontentsline{toc}{section}{TÀI NGUYÊN THỰC NGHIỆM VÀ HƯỚNG DẪN CÀI ĐẶT}
\section*{TÀI NGUYÊN THỰC NGHIỆM VÀ HƯỚNG DẪN CÀI ĐẶT}
\markboth{TÀI NGUYÊN THỰC NGHIỆM VÀ HƯỚNG DẪN CÀI ĐẶT}{TÀI NGUYÊN THỰC NGHIỆM VÀ HƯỚNG DẪN CÀI ĐẶT}

\subsection*{1. Kho Lưu Trữ Mã Nguồn Chính Thức}
\begin{mybox}{Thông Tin Kho Chứa Dự Án \& Đường Dẫn Trực Tuyến}
    \begin{itemize}[leftmargin=*]
        \item \textbf{Tác giả thực hiện:} Nguyễn Nam Hải (Mã SV: B23DCCN277 -- Lớp D23CTPM01)
        \item \textbf{Cấu trúc sổ tay Notebook (7 files):}
        \begin{itemize}
            \item \texttt{01\_rnn\_theory\_and\_mathematics.ipynb}
            \item \texttt{02\_eda\_and\_data\_diagnostics.ipynb}
            \item \texttt{03\_pytorch\_amzn.ipynb}
            \item \texttt{04\_pytorch\_gold.ipynb}
            \item \texttt{05\_keras\_amzn.ipynb}
            \item \texttt{06\_keras\_gold.ipynb}
            \item \texttt{07\_numpy\_rnn\_gold.ipynb}
        \end{itemize}
        \item \textbf{Cấu trúc Web Dashboard:}
        \begin{itemize}
            \item \texttt{backend/main.py}: API viết bằng FastAPI, nạp sẵn 4 pre-trained models.
            \item \texttt{backend/static/index.html}: Giao diện Dashboard tương tác hiện đại với Tailwind và Chart.js.
        \end{itemize}
    \end{itemize}
\end{mybox}

\subsection*{2. Danh Mục Tập Dữ Liệu Thực Nghiệm}
\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\textwidth}{l L{3.2cm} X L{4.2cm}}
\toprule
\textbf{Bộ dữ liệu} & \textbf{Thời gian} & \textbf{Đặc tả Đầu vào Mạng RNN} & \textbf{Tệp nguồn} \\
\midrule
\textbf{1. AMZN} & 1997 -- 2023 & Chuỗi $T=30$, Tensor $(B, 30, 1)$ & \texttt{data/AMZN.csv} \\
\addlinespace
\textbf{2. Gold Price} & 1968 -- 2021 & Chuỗi $T=30$, Tensor $(B, 30, 1)$ & \texttt{data/gold\_price.csv} \\
\bottomrule
\end{tabularx}
\caption{Tổng hợp đặc tả của 2 bộ dữ liệu thực nghiệm trong Assignment 06}
\label{tab:datasets_spec}
\end{table}

\newpage

% ==============================================================================
% CHƯƠNG 1
% ==============================================================================
\section{Cơ sở lý thuyết giải tích và bản chất của mạng RNN}

\subsection{Deep Learning dưới góc nhìn Chuỗi thời gian và Mạng Hồi quy}
Tương tự như cách mạng CNN tận dụng tính định xứ của không gian 2D, mạng RNN (Recurrent Neural Network) tận dụng tính định hướng của chiều thời gian 1D. Đối với các chuỗi thời gian như giá chứng khoán hay thời tiết, thứ tự của dữ liệu $X = \{x_1, x_2, \dots, x_t\}$ mang ý nghĩa quyết định.

RNN thay thế giả định Độc lập và Cùng phân phối (IID - Independent and Identically Distributed) của các mô hình cơ bản bằng cách thiết lập một liên kết (Hidden State $h_t$) lưu lại toàn bộ tri thức của các mốc thời gian quá khứ $t'<t$.

\subsection{Toán tử tính toán trạng thái ẩn (Hidden State)}
Thay vì tính $\hat{y}_t = f(x_t)$, RNN định nghĩa một hàm truy hồi (Recurrence Relation):
\begin{equation}
    h_t = \sigma_h (U x_t + W h_{t-1} + b_h)
\end{equation}
\begin{equation}
    \hat{y}_t = \sigma_y (V h_t + b_y)
\end{equation}
Trong đó $U, W, V$ lần lượt là các ma trận trọng số tương tác Input-to-Hidden, Hidden-to-Hidden, và Hidden-to-Output. Ma trận $W$ là trái tim của RNN, định tuyến thông tin từ quá khứ $h_{t-1}$ đi tới hiện tại $h_t$.

\subsection{Thuật toán BPTT (Backpropagation Through Time)}
Thuật toán huấn luyện chuẩn của RNN được gọi là BPTT. Về bản chất, ta khai triển (unroll) toàn bộ đồ thị tính toán của mạng theo số bước thời gian $T$. Đạo hàm của hàm mục tiêu (Loss) $L$ theo ma trận $W$ là tổng của Gradient tại tất cả các thời điểm:
\begin{equation}
    \frac{\partial L}{\partial W} = \sum_{t=1}^{T} \frac{\partial L_t}{\partial W}
\end{equation}
Việc tính toán $\frac{\partial L_t}{\partial W}$ đòi hỏi phải truyền lỗi ngược từ thời điểm $t$ về tới mốc thời điểm $k=1$.

\subsection{Bài toán Vanishing Gradient (Suy thoái Gradient)}
\begin{mybox}{Phân tích giải tích Ma trận Jacobian}
Khi áp dụng luật chuỗi (Chain Rule) để tính đạo hàm trạng thái ẩn $h_t$ theo một trạng thái ẩn trong quá khứ $h_k$ ($k < t$), ta phải nhân liên tiếp các ma trận Jacobian cục bộ:
\begin{equation}
    \frac{\partial h_t}{\partial h_k} = \prod_{i=k+1}^{t} \frac{\partial h_i}{\partial h_{i-1}}
\end{equation}
Vì $h_i = \tanh(W h_{i-1} + \dots)$, đạo hàm $\frac{\partial h_i}{\partial h_{i-1}}$ có dạng:
\begin{equation}
    \frac{\partial h_i}{\partial h_{i-1}} = W^T \text{diag}\left( 1 - \tanh^2(u_i) \right)
\end{equation}
Chuỗi phép nhân ma trận $W^T$ lặp lại $t - k$ lần sẽ làm cho Norm của ma trận Gradient tăng hoặc giảm theo quy luật hàm mũ. Nếu Eigenvalues lớn nhất của $W < 1$, toàn bộ tích trên sẽ tiến về mốc $0$, khiến mạng "quên" hoàn toàn các biến cố xảy ra ở quá khứ xa. Đây là giới hạn toán học chí mạng của Vanilla RNN.
\end{mybox}

% ==============================================================================
% CHƯƠNG 2
% ==============================================================================
\section{Khảo sát 2 tập dữ liệu thực nghiệm}

\subsection{Tập dữ liệu chuỗi thời gian Giá Vàng (Gold Price)}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{eda_gold.png}
    \caption{Chuỗi thời gian biến động giá vàng (1968-2021).}
    \label{fig:eda_gold}
\end{figure}
Như thể hiện tại Hình \ref{fig:eda_gold}, dữ liệu có xu hướng dài hạn (Long-term Trend) và không có tính dừng (Non-stationary). Các đỉnh đột biến thường liên kết mật thiết với khủng hoảng kinh tế toàn cầu.

\subsection{Tập dữ liệu chuỗi thời gian Chứng khoán (AMZN)}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{eda_amzn.png}
    \caption{Sự bùng nổ của cổ phiếu AMZN từ giai đoạn 2010 trở đi.}
    \label{fig:eda_amzn}
\end{figure}

\subsection{Cơ chế Cửa sổ trượt (Sliding Window)}
Để huấn luyện mô hình dự đoán giám sát, ta phải kiến tạo một cơ sở dữ liệu giám sát từ mảng 1 chiều. Phép biến đổi Sliding Window với $Seq\_length = 30$ tạo ra ma trận $X$ kích thước $(N, 30, 1)$ và nhãn tương ứng $Y$ kích thước $(N, 1)$. Đồng thời, ta thực hiện chia tách Train/Test theo thời gian thực (không tráo đổi - Shuffle).

% ==============================================================================
% CHƯƠNG 3
% ==============================================================================
\section{Thiết kế và cài đặt mô hình (NumPy, PyTorch, Keras)}

\subsection{Xây dựng Vanilla RNN thuần từ con số 0 bằng NumPy}
Nhằm nắm vững cơ chế giải tích, Notebook \texttt{07\_numpy\_rnn\_gold.ipynb} định nghĩa toàn bộ mạng RNN thuần không sử dụng framework Deep Learning.
\begin{itemize}
    \item Khởi tạo bộ tham số ma trận $U, W, V$ kích thước tùy chỉnh.
    \item Xây dựng vòng lặp For-loop cập nhật trạng thái ẩn (Forward Pass).
    \item Tự xây dựng hàm Gradient (BPTT) cho từng tham số với kỹ thuật kẹp (Gradient Clipping) để tránh tràn bộ nhớ.
\end{itemize}

\subsection{Cài đặt mô hình bằng PyTorch}
Module \texttt{nn.RNN} của PyTorch cho phép tính toán song song qua ma trận lớn trên GPU. Mạng được cấu hình với \texttt{hidden\_size=64} và \texttt{num\_layers=1}. Tại tầng ra, ta chỉ lấy lát cắt của trạng thái ẩn thời điểm $T$: \texttt{out[:, -1, :]} để ánh xạ ra $y_{pred}$.

\subsection{Cài đặt mô hình bằng Keras/TensorFlow}
Trong Keras, kiến trúc có phần ngắn gọn hơn thông qua API \texttt{Sequential}. \texttt{SimpleRNN(64, return\_sequences=False)} giúp bỏ qua các trạng thái ẩn trung gian, truyền thẳng kết quả tới hàm \texttt{Dense(1)}. Keras Callback \texttt{EarlyStopping} tự động cắt dứt chu trình nếu Validation Loss bão hòa.

% ==============================================================================
% CHƯƠNG 4
% ==============================================================================
\section{Kết quả thực nghiệm, đối chuẩn số liệu và phân tích chuyên sâu}

\subsection{Bảng tổng hợp đối chuẩn kết quả}
Dữ liệu dưới đây trích xuất từ tập kiểm thử (Test Set) không nhìn thấy trong quá trình Train.
\begin{table}[H]
    \centering
    \begin{tabular}{|l|c|c|c|c|}
        \hline
        \textbf{Mô hình} & \textbf{RMSE} & \textbf{MAE} & \textbf{MAPE} & \textbf{Độ chính xác Hướng} \\
        \hline
        PyTorch AMZN & 25.24 & 21.75 & 14.52\% & 49.07\% \\
        \hline
        Keras AMZN & 57.04 & 51.55 & 35.17\% & 49.79\% \\
        \hline
        PyTorch Gold & 425.98 & 398.62 & 28.65\% & 50.22\% \\
        \hline
        Keras Gold & 72.92 & 56.06 & 3.81\% & 50.42\% \\
        \hline
    \end{tabular}
    \caption{Chỉ số đánh giá độ tin cậy của 4 mô hình}
\end{table}

\subsection{Phân tích kết quả trên tập Giá Vàng và Chứng khoán}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{res_amzn.png}
    \caption{Mô phỏng đường cong dự báo (Test Split) trên tập AMZN.}
    \label{fig:res_amzn_test}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{res_gold.png}
    \caption{Mô phỏng đường cong dự báo trên tập Gold.}
    \label{fig:res_gold_test}
\end{figure}

\subsection{Hiện tượng trễ pha (Lagging)}
\begin{chartbox}[Nghịch lý Dự báo Trễ pha ở Chuỗi Thời gian Tài chính]
Nhìn trực quan vào Hình \ref{fig:res_amzn_test} và Hình \ref{fig:res_gold_test}, ta thấy đường dự báo bám dính rất chặt vào đường Ground Truth. Nhưng khi phóng đại (Zoom-in), ta phát hiện giá trị dự báo thực chất luôn bị chậm (lag) đúng 1 nhịp so với thực tế: $\hat{y}_{t+1} \approx y_t$. 

Bản chất của việc này là do hàm Loss (MSE) bị mắc kẹt tại cực tiểu cục bộ: Vì thị trường chứng khoán tuân theo luật Random Walk (Bác bỏ giả thuyết thị trường hiệu quả), nên việc dự đoán ngày mai giống y hệt ngày hôm nay là cách "an toàn" nhất để hệ thống nhận được mức phạt (MSE penalty) thấp nhất. Vanilla RNN vì không có bộ nhớ vĩnh cửu nên không đủ năng lực phát hiện các chuỗi Logic phức tạp, buộc phải thỏa hiệp bằng "Lagging".
\end{chartbox}

% ==============================================================================
% CHƯƠNG 5
% ==============================================================================
\section{Kết luận chung}
Toàn bộ Assignment 06 đã hiện thực hóa từ A-Z một quy trình Deep Learning cho Time Series. Báo cáo đã minh chứng được khả năng trích xuất tri thức tuần tự của RNN cũng như vạch trần các yếu điểm cố hữu (Vanishing Gradient, Lagging). Hệ thống báo cáo cùng với phần mềm Web Dashboard tạo thành một quy chuẩn hoàn thiện, thể hiện nỗ lực tối đa của sinh viên trong quá trình học tập.

\end{document}
"""

with open("report/A06_Report.tex", "w", encoding="utf-8") as f:
    f.write(latex_content)

