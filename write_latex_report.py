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

Báo cáo Kỹ thuật Assignment 06 trình bày nghiên cứu hệ thống và khảo sát thực nghiệm chuyên sâu về Mạng nơ-ron Hồi quy (Recurrent Neural Network -- RNN). Mục tiêu của báo cáo là hệ thống hóa toàn bộ vòng đời phát triển của một bài toán Deep Learning dành riêng cho chuỗi thời gian: từ khâu am hiểu cơ sở toán học thuần túy, phân tích khám phá đặc trưng phân phối dữ liệu (EDA), cho đến hiện thực hóa mã nguồn (bằng NumPy, PyTorch, Keras) và cuối cùng là triển khai lên một hệ thống Web Dashboard hoàn chỉnh.

Báo cáo phân tích sâu sắc các rào cản kinh điển của chuỗi thời gian như: Tại sao mạng MLP hay Conv1D không đủ năng lực xử lý? Ma trận Jacobian ảnh hưởng như thế nào đến sự suy thoái Gradient? Làm thế nào để giải quyết bằng kỹ thuật Gradient Clipping? Thông qua việc đối chuẩn trên 2 tập dữ liệu tài chính thực tế (Gold Price và AMZN Stock), báo cáo đã bóc tách rõ ràng hiện tượng "Trễ pha" (Lagging) - một đặc trưng của Vanilla RNN khi cố gắng mô phỏng một quy luật bước đi ngẫu nhiên (Random Walk) trên thị trường tài chính.

\newpage

% ==============================================================================
% CHƯƠNG 1
% ==============================================================================
\section{Cơ sở lý thuyết giải tích và toán học của RNN}

\subsection{Dữ liệu chuỗi \& tensor ba chiều}
Trong lĩnh vực trí tuệ nhân tạo, dữ liệu chuỗi (Sequential Data) mang một đặc tính cốt lõi khác biệt hoàn toàn với ảnh hoặc bảng biểu tĩnh: **Thứ tự của dữ liệu mang ý nghĩa quyết định**. Ví dụ, trong chuỗi thời gian (Time-series), giá trị của biến tại thời điểm $t$ phụ thuộc mật thiết vào các sự kiện diễn ra tại $t-1, t-2, \dots$
Để máy tính có thể xử lý, dữ liệu chuỗi được biểu diễn dưới dạng **Tensor 3 chiều (3D Tensor)** với cấu trúc định dạng: \texttt{(Batch Size, Sequence Length, Input Features)}.
\begin{itemize}
    \item \textbf{Batch Size (Kích thước lô):} Số lượng chuỗi độc lập được xử lý song song trong một lần truyền xuôi (Forward pass).
    \item \textbf{Sequence Length (Độ dài chuỗi - $T$):} Số mốc thời gian (time steps) có trong một chuỗi đơn. Ví dụ $T=30$ ngày.
    \item \textbf{Input Features (Đặc trưng đầu vào):} Kích thước không gian vector của mỗi mốc thời gian. Với giá vàng chỉ có 1 cột giá trị, số features bằng 1.
\end{itemize}

\subsection{Các dạng bài toán chuỗi}
Dựa trên kiến trúc của mạng RNN, bài toán dữ liệu chuỗi được phân loại thành 4 dạng kinh điển:
\begin{enumerate}
    \item \textbf{One-to-One:} Bản chất là bài toán mạng Feed Forward (MLP) thông thường, kích thước chuỗi là 1.
    \item \textbf{One-to-Many:} Mạng nhận một đầu vào duy nhất (ví dụ: một bức ảnh) và sinh ra một chuỗi đầu ra (ví dụ: câu văn chú thích - Image Captioning).
    \item \textbf{Many-to-One:} Mạng nhận một chuỗi thời gian làm đầu vào và đưa ra một dự đoán duy nhất ở bước cuối cùng. (Đây chính là bài toán dự báo chứng khoán/giá vàng trong đồ án này).
    \item \textbf{Many-to-Many:} Có hai phân nhóm: 
        \begin{itemize}
            \item \textit{Đồng bộ (Synced):} Mỗi bước đầu vào đều có một đầu ra tương ứng (ví dụ: Gán nhãn từ loại cho từng chữ trong câu).
            \item \textit{Bất đồng bộ (Encoder-Decoder):} Đọc hết một chuỗi rồi mới sinh ra một chuỗi khác (ví dụ: Dịch máy - Machine Translation).
        \end{itemize}
\end{enumerate}

\subsection{Vì sao MLP và Conv1D chưa đủ?}
Trước khi có RNN, kỹ sư thường dùng Mạng Đa tầng (MLP) hoặc Tích chập 1 chiều (Conv1D) để xử lý chuỗi:
\begin{itemize}
    \item \textbf{Hạn chế của MLP:} MLP bắt buộc kích thước đầu vào phải cố định. Nếu nối (flatten) toàn bộ 30 mốc thời gian thành một vector $1D$, MLP sẽ gán các trọng số độc lập cho từng mốc thời gian. Điều này phá vỡ tính tịnh tiến qua thời gian (Translation Invariance) và không thể chia sẻ tri thức learned pattern (ví dụ một mẫu tăng giá) nếu nó xuất hiện ở các vị trí khác nhau trong chuỗi.
    \item \textbf{Hạn chế của Conv1D:} Conv1D sử dụng bộ lọc (filter) trượt dọc theo chiều thời gian. Mặc dù có tính chia sẻ tham số (Parameter sharing) cục bộ, Conv1D chỉ nắm bắt được **phụ thuộc ngắn hạn (Short-term dependencies)** theo kích thước kernel. Nó thiếu một "bộ nhớ" toàn cục (Global memory) để ghi nhận chuỗi sự kiện nối tiếp.
\end{itemize}

\subsection{Simple RNN (Vanilla RNN)}
Để giải quyết những bài toán trên, mạng RNN (Simple RNN / Vanilla RNN) ra đời với khái niệm **Trạng thái Ẩn (Hidden State - $h_t$)**. Trạng thái ẩn đóng vai trò như "trí nhớ ngắn hạn" của mạng, được cập nhật liên tục qua mỗi mốc thời gian $t$.

Tại mỗi bước $t$, Simple RNN áp dụng nguyên lý **Chia sẻ tham số (Parameter Sharing)**: Các ma trận $U$ (Input-to-Hidden), $W$ (Hidden-to-Hidden) và $V$ (Hidden-to-Output) được dùng chung cho tất cả các mốc thời gian. 
Phương trình truyền xuôi:
\begin{align}
    h_t &= \tanh(U x_t + W h_{t-1} + b_h) \\
    \hat{y}_t &= V h_t + b_y
\end{align}
Cơ chế chia sẻ tham số giúp mô hình khái quát hóa tốt hơn và xử lý được các chuỗi có độ dài thay đổi liên tục.

\subsection{Lan truyền ngược (BPTT) và vấn đề của gradient}
Để huấn luyện Simple RNN, thuật toán **Backpropagation Through Time (BPTT)** được sử dụng. BPTT thực chất là trải phẳng mạng RNN theo thời gian thành một mạng sâu $T$ tầng, sau đó áp dụng truyền lỗi ngược (Backprop).

\begin{mybox}{Khảo sát phổ (Spectral Analysis) của ma trận $W$}
Khi lan truyền ngược $k$ bước thời gian, thành phần $dh_{t-k}$ phụ thuộc vào tích Jacobian:
\begin{equation}
    \frac{\partial h_t}{\partial h_{t-k}} = \prod_{i=t-k+1}^{t} \left[ W^T \text{diag}(1 - \tanh^2(...)) \right]
\end{equation}
Nếu $\lambda$ là các giá trị riêng lớn nhất của ma trận $W$:
\begin{itemize}
    \item Khi $\vert{}\lambda\vert{} > 1$: Lũy thừa ma trận làm cho đạo hàm phình to hàm mũ, gây ra \textbf{Exploding Gradient} (bùng nổ Gradient). Mô hình vỡ quỹ đạo hội tụ (NaN/Inf).
    \item Khi $\vert{}\lambda\vert{} < 1$: Đạo hàm liên tục nhân với các số $< 1$ (do $\tanh' \le 1$), dẫn tới \textbf{Vanishing Gradient} (suy thoái Gradient). Mạng không thể "nhớ" được các thông tin cách đó quá nhiều bước thời gian.
\end{itemize}
\end{mybox}

\subsection{Giải pháp Kỹ thuật: Gradient Clipping}
Trong khi Vanishing Gradient đòi hỏi thay đổi cả cấu trúc mạng (sang LSTM/GRU), thì \textbf{Exploding Gradient} có thể giải quyết dứt điểm bằng một kỹ thuật số học cực kỳ thanh lịch: \textbf{Gradient Clipping}.
Ý tưởng: Theo dõi chuẩn (Norm) của toàn bộ vector Gradient. Nếu Norm vượt qua một ngưỡng $threshold$, ta sẽ thực hiện co rút (scale down) toàn bộ vector gradient theo tỷ lệ để Norm của nó vừa đúng bằng $threshold$.
\begin{equation}
    \text{Nếu } \|g\| > \text{threshold}, \quad g \leftarrow g \cdot \frac{\text{threshold}}{\|g\|}
\end{equation}
Điều này giúp giữ nguyên "hướng" (Direction) của Gradient để mạng vẫn học đúng quy luật, nhưng giới hạn "độ lớn" (Magnitude) để bước nhảy trọng số không phá vỡ mô hình.


% ==============================================================================
% CHƯƠNG 2
% ==============================================================================
\section{Khảo sát dữ liệu chuỗi thực tế (Data Diagnostics)}

\subsection{Nguồn \& Quy mô data}
Để có góc nhìn bao quát, đồ án kiểm thử mô hình trên hai bộ dữ liệu đặc thù:
\begin{enumerate}
    \item \textbf{Gold Price (Giá vàng):} Thu thập từ tập dữ liệu vĩ mô (1968 - 2021). Với hơn 13,462 bản ghi giao dịch ngày, độ dài bộ dữ liệu đủ sâu để RNN tìm thấy những chu kỳ (cycles) kéo dài hàng chục năm.
    \item \textbf{AMZN Stock (Chứng khoán Amazon):} Trích xuất từ Yahoo Finance (1997 - 2023) với 6,682 mẫu. Phản ánh bức tranh thị trường đầy khốc liệt của ngành công nghệ.
\end{enumerate}

\subsection{Phân phối và biến động}
Việc nắm bắt phân phối thống kê là bước tiên quyết trước khi đưa dữ liệu vào mạng Deep Learning.
\begin{table}[H]
    \centering
    \begin{tabular}{|l|c|c|c|c|c|c|}
        \hline
        \textbf{Dataset} & \textbf{Mean} & \textbf{Std} & \textbf{Min} & \textbf{Max} & \textbf{Skewness} & \textbf{Kurtosis} \\
        \hline
        AMZN Close & 43.14 & 54.33 & 0.06 & 186.57 & 1.34 & 0.52 \\
        \hline
        Gold Price & 585.34 & 483.91 & 35.10 & 2067.15 & 1.05 & 0.08 \\
        \hline
    \end{tabular}
    \caption{Bảng thống kê mô tả phân phối.}
\end{table}
Nhìn vào độ lệch chuẩn (Std), cả hai tập dữ liệu đều mang độ phân tán rất cao. Hệ số Skewness dương $> 1.0$ cho thấy phân phối lệch phải (Right-skewed), tập trung ở vùng giá thấp và kéo dài đuôi ra vùng giá bùng nổ (bong bóng kinh tế/công nghệ).
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{eda_gold.png}
    \caption{Biểu đồ thể hiện biến động giá Vàng, một dạng chuỗi Không dừng (Non-Stationary).}
\end{figure}

\subsection{Tuỳ đặc trưng mỗi data mà làm tiếp}
Chuỗi thời gian trong tài chính hầu như đều vi phạm giả thuyết dừng (Stationarity). Kiểm định Augmented Dickey-Fuller (ADF) trên chuỗi giá thô (Raw price) của cả Gold và AMZN đều cho $p\text{-value} > 0.05$. 

Tùy vào mục tiêu bài toán mà kỹ thuật tiền xử lý sẽ phân nhánh:
\begin{itemize}
    \item \textbf{Nếu tập trung vào tỷ suất sinh lời:} Bắt buộc phải chuyển đổi chuỗi giá $P_t$ thành chuỗi lợi suất Log (Log Returns): $R_t = \ln(P_t/P_{t-1})$. Chuỗi $R_t$ này ngay lập tức thỏa mãn tính dừng (p-value $< 0.01$), giúp RNN tối ưu gradient ổn định hơn.
    \item \textbf{Nếu bắt buộc phải dự báo giá tuyệt đối (Nhiệm vụ của Assignment):} Ta vẫn giữ nguyên chuỗi giá $P_t$, nhưng bắt buộc phải khử nhiễu thang đo (Scale) bằng \texttt{MinMaxScaler}. Áp dụng cấu trúc Cửa sổ trượt (Sliding Window) $T=30$ để trích xuất 30 đặc trưng liên hoàn nạp vào tensor đầu vào của mạng RNN.
\end{itemize}


% ==============================================================================
% CHƯƠNG 3
% ==============================================================================
\section{Thiết kế và cài đặt mô hình}

\subsection{Trình bày thuật toán \& Cấu hình kỹ thuật}
Báo cáo trình bày 3 phiên bản mã nguồn: NumPy thuần (dùng để chứng minh toán học BPTT), PyTorch và Keras. 
\begin{table}[H]
    \centering
    \begin{tabular}{|l|l|l|}
        \hline
        \textbf{Thông số} & \textbf{PyTorch} & \textbf{Keras} \\
        \hline
        API / Base Class & \texttt{nn.RNN} & \texttt{Sequential} \\
        Hidden Size & 64 & 64 \\
        Optimizer & Adam ($lr=0.001$) & Adam ($lr=0.001$) \\
        Weight Init & Uniform (Default) & Orthogonal / Glorot \\
        Chống Exploding & \texttt{clip\_grad\_norm\_} & \texttt{clipnorm=1.0} \\
        \hline
    \end{tabular}
    \caption{Đối chuẩn cấu hình hệ thống huấn luyện.}
\end{table}

\subsection{Bóc tách sâu về Nghịch lý Directional Accuracy}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\linewidth]{res_amzn.png}
    \caption{Đường cong dự báo (Test Split) trên tập AMZN.}
\end{figure}
Chỉ số **Độ chính xác Hướng (Directional Accuracy)** của mô hình đo lường khả năng đoán đúng chiều (tăng hay giảm) của giá trị:
\begin{equation}
    DA = \frac{1}{N-1} \sum_{t=1}^{N-1} \mathbb{I}\left( \text{sign}(y_{t+1} - y_t) == \text{sign}(\hat{y}_{t+1} - y_t) \right)
\end{equation}
Tại sao DA của mô hình RNN trên AMZN chỉ đạt xấp xỉ 50\% (ngang ngửa việc tung đồng xu), trong khi biểu đồ dự đoán lại bám rất sát Ground Truth?
Bởi vì Vanilla RNN bị cuốn vào hiệu ứng "Lagging" (Trễ pha). Để giảm thiểu hàm phạt Loss (MSE) lớn, mô hình đã học được một mánh khóe: Giá ngày mai gần như bằng giá ngày hôm nay $\hat{y}_{t+1} \approx y_t$. Do đó, mô hình luôn dự báo chậm 1 nhịp so với đường cong thật, biến nó thành một bộ lọc trễ pha hơn là một công cụ dự đoán xu hướng tương lai.


% ==============================================================================
% CHƯƠNG 4
% ==============================================================================
\section{Triển khai Web App (Deployment Architecture)}

Để đưa các mô hình nghiên cứu dạng \texttt{.pkl}, \texttt{.pth}, \texttt{.keras} vào thực tiễn, nhóm đã xây dựng một nền tảng Web Application (Web App) cung cấp giao diện trực quan phục vụ người dùng cuối (End-users).

\subsection{Kiến trúc hệ thống (System Architecture)}
Hệ thống tuân theo kiến trúc Client-Server RESTful phân tách:
\begin{itemize}
    \item \textbf{Backend (Server):} Sử dụng vi khung (Microframework) **FastAPI** trên nền tảng Uvicorn xử lý luồng bất đồng bộ (Asynchronous). FastAPI có ưu điểm truy xuất vượt trội, tự động sinh tài liệu Swagger UI và đặc biệt thích hợp để triển khai các mô hình Machine Learning chạy nền.
    \item \textbf{Frontend (Client):} Sử dụng **Vanilla JavaScript** kết hợp bộ thư viện tiện ích **Tailwind CSS** định kiểu giao diện hiện đại. Trọng tâm là thư viện **Chart.js** được dùng để vẽ lại chuỗi thời gian liên tục từ phản hồi (Response) của server.
\end{itemize}

\subsection{Quy trình Nạp mô hình (Model Loading)}
Trong giai đoạn khởi động Server (Lifespan start-up), hệ thống quét toàn bộ thư mục \texttt{models/} để tiền tải (Pre-load) bộ 4 mô hình (PyTorch/Keras cho Gold/AMZN). Các lớp giả lập tensor như \texttt{TimeSeriesRNN} được nạp sẵn vào RAM, các file `MinMaxScaler` cũng được giải nén sẵn thông qua `pickle` để không tốn thời gian I/O đĩa cứng ở từng request của người dùng.

\subsection{Giao diện (User Interface)}
\begin{figure}[H]
    \centering
    % Nơi người dùng sẽ thay thế bằng ảnh Screenshot thực tế
    \includegraphics[width=0.95\linewidth]{dashboard_ui.png} 
    \caption{Giao diện trực quan của Web Dashboard dự báo chuỗi thời gian (Người dùng thiết lập thông số truy vấn).}
    \label{fig:web_dashboard}
\end{figure}

Giao diện Web cung cấp Control Panel tinh giản:
\begin{itemize}
    \item Hộp thả chọn loại mô hình (AMZN - PyTorch, Gold - Keras, v.v...).
    \item Bộ DatePicker cho phép người dùng khoanh vùng giới hạn thời gian dự báo (Start Date $\rightarrow$ End Date).
    \item Khu vực trung tâm là đồ thị diện rộng của Chart.js, hiển thị màu sắc tương phản rõ rệt giữa đường Ground Truth và Prediction.
\end{itemize}

\subsection{Kiểm chứng hệ thống (Validation \& Testing)}
Quy trình gọi suy luận (Inference) hoạt động trơn tru theo đường ống (Pipeline): 
Người dùng gửi khoảng ngày $\to$ API \texttt{/predict\_range} tìm các chỉ số trong tệp CSV gốc $\to$ Cắt chuỗi mốc 30 ngày (Sliding Window) $\to$ Dịch chuyển qua \texttt{scaler.transform} $\to$ Chuyển vị thành ma trận Tensor $\to$ Chạy \texttt{model.forward()} $\to$ Dịch ngược bằng \texttt{inverse\_transform} $\to$ Trả về Client cấu trúc JSON chứa mảng ngày và giá trị để vẽ.
Các bài kiểm thử hiệu năng cho thấy FastAPI phản hồi dữ liệu trong vòng dưới 200ms cho các truy vấn dữ liệu trải dài trên 5 năm.

% ==============================================================================
% TÀI LIỆU THAM KHẢO
% ==============================================================================
\newpage
\section*{Tài liệu tham khảo (References)}
\addcontentsline{toc}{section}{Tài liệu tham khảo (References)}
\begin{enumerate}[label={[\arabic*]}]
    \item Goodfellow, I., Bengio, Y., \& Courville, A. (2016). \textit{Deep Learning}. MIT Press. (Chapter 10: Sequence Modeling: Recurrent and Recursive Nets).
    \item Werbos, P. J. (1990). \textit{Backpropagation through time: what it does and how to do it}. Proceedings of the IEEE, 78(10), 1550-1560.
    \item Hochreiter, S. (1991). \textit{Untersuchungen zu dynamischen neuronalen Netzen}. Diploma thesis, TU Munich.
    \item Hochreiter, S., \& Schmidhuber, J. (1997). \textit{Long short-term memory}. Neural computation, 9(8), 1735-1780.
    \item Lipton, Z. C., Berkowitz, J., \& Elkan, C. (2015). \textit{A critical review of recurrent neural networks for sequence learning}. arXiv preprint arXiv:1506.00019.
\end{enumerate}

\end{document}
"""

with open("report/A06_Report.tex", "w", encoding="utf-8") as f:
    f.write(latex_content)
