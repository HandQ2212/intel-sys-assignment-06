Dưới đây là bản dựng trực quan hoàn chỉnh theo phong cách thẻ bài thuyết trình (Visual Slide Cards) hiện đại. Từng slide được mô hình hóa trực tiếp bằng biểu đồ khối ASCII, sơ đồ luồng dữ liệu (Data Pipeline), công thức toán học và bảng chỉ số thực tế, giúp người xem nắm bắt ngay bản chất lý thuyết của RNN.

---

### SLIDE 1: TRANG TIÊU ĐỀ

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CHUYÊN ĐỀ HỌC SÂU (DEEP LEARNING)                │
│                                                                        │
│                 RECURRENT NEURAL NETWORKS (RNN)                        │
│          Từ Hạn Chế của MLP & 1D-CNN đến Nguyên Lý Xử Lý               │
│                  Dữ Liệu Chuỗi có Trạng Thái Ẩn                        │
│                                                                        │
│   Nhóm thực hiện:                                                      │
│   • Văn Thị Mai Linh          • Nguyễn Văn Minh Lực                    │
│   • Giáp Minh Hiếu            • Nguyễn Nam Hải                         │
│                                                                        │
│   "Feedforward nhìn thế giới qua từng bức ảnh rời rạc;                 │
│    RNN thấu hiểu dữ liệu qua dòng chảy liên tục của thời gian."        │
└────────────────────────────────────────────────────────────────────────┘

```

---

### SLIDE 2: BẢN CHẤT DỮ LIỆU DẠNG CHUỖI (SEQUENTIAL DATA)

**Thứ tự xuất hiện quyết định hoàn toàn ngữ nghĩa của dữ liệu.**

```
               [CHUỖI RỜI RẠC: NLP / VĂN BẢN]
               "Hà Nội không mưa"   ≠   "Mưa không Hà Nội"
                    │                        │
                    ▼                        ▼
               (Có nghĩa rõ ràng)       (Vô nghĩa / Biến đổi ngữ nghĩa)

               [CHUỖI LIÊN TỤC: TIME-SERIES / TÀI CHÍNH]
     Giá vàng: [ 82.5 ───► 83.1 ───► 84.0 ───► 85.2 ]  (Xu hướng tăng đều)
     Giá vàng: [ 85.2 ───► 84.0 ───► 83.1 ───► 82.5 ]  (Xu hướng giảm sâu)

```

* **Đặc tính trật tự:** Mỗi điểm dữ liệu tại thời điểm $t$ luôn mang mối tương quan mật thiết với các điểm quá khứ $t-1, t-2, \dots$[cite: 1, 3]
* **Hai dạng chính:** Dữ liệu token rời rạc (Text, DNA) và dữ liệu chuỗi số liên tục (Giá vàng, cổ phiếu, nhịp tim)[cite: 1, 3].

---

### SLIDE 3: BÀI TOÁN DỰ ĐOÁN PHẦN TỬ KẾ TIẾP (NEXT STEP PREDICTION)

**Mục tiêu:** Cho chuỗi quan sát quá khứ $X = (x_1, x_2, \dots, x_t)$, dự đoán giá trị tương lai $x_{t+1}$.

```
  BÀI TOÁN 1: NEXT WORD PREDICTION (NLP)
  Ngữ cảnh:   "We"  ──►  "are"  ──►  "learning"  ──►  "AI"  ──► [ ? ]
                                                                  │
                                                      Target kỳ vọng: "is"[cite: 1, 3]

  BÀI TOÁN 2: DỰ BÁO CHUỖI THỜI GIAN (TIME-SERIES)
  Cửa sổ trượt: [ P(t-29), P(t-28), ... , P(t-1), P(t) ]  ──►  [ P(t+1) ]
                └─────────────── 30 ngày lịch sử ──────┘        Biến động ngày 31[cite: 1, 3]

```

---

### SLIDE 4: HAI PIPELINE TIỀN XỬ LÝ ĐẶC TRƯNG

Dữ liệu thô không thể đưa trực tiếp vào mạng mà phải đi qua pipeline chuẩn hóa[cite: 1, 3]:

```
[VĂN BẢN]   "giá vàng tăng"
                 │ Tokenizer
                 ▼
            ["giá", "vàng", "tăng"]
                 │ Vocabulary Index[cite: 1, 3]
                 ▼
            [ 2,  3,  4 ] ──► Padding ──► [ 2,  3,  4,  0,  0 ]
                                                │
                                                ▼ Tra cứu Embedding (E)[cite: 1, 3]
                                          Tensor [Batch, Seq_Len, d][cite: 1, 3]

[GIÁ VÀNG]  File CSV thô (Date, Price)
                 │ Làm sạch & Chia tập (Train 70% | Val 15% | Test 15%)[cite: 1, 3]
                 ▼
            log1p(Price) ──► MinMax Scaling (Fit CHỈ TRÊN Train)[cite: 1, 3]
                 │
                 ▼ Cửa sổ trượt 30 ngày (Windowing)[cite: 1, 3]
            Tensor Đầu vào: [N_samples, 30_timesteps, 1_feature][cite: 1, 3]

```

---

### SLIDE 5: TIẾP CẬN BẰNG MLP VÀ CƠ CHẾ GHÉP PHẲNG (FLATTEN)

Mạng truyền thẳng (MLP) bắt buộc phải biến toàn bộ ngữ cảnh thành một vector phẳng duy nhất[cite: 1, 3]:

```
   Token 1: "We"       [ -0.18,  0.55,  1.62,  0.70 ] (1x4)
   Token 2: "are"      [  0.22,  1.32,  0.13,  2.05 ] (1x4)
   Token 3: "learning" [  0.43, -1.30, -0.88,  1.59 ] (1x4)  ──┐
   Token 4: "AI"       [  1.02, -1.90,  0.31,  0.42 ] (1x4)    │ Ép phẳng (Concatenate)[cite: 1, 3]
   Token 5:       [  1.78, -0.82, -0.27,  1.35 ] (1x4)  ──┘
                                │
                                ▼
         Vector X_concat: [1 x 20 chiều] (Phẳng hoàn toàn)[cite: 1]
                                │
   ┌────────────────────────────┴────────────────────────────┐
   │  Linear Layer (20 ──► 16) ──► ReLU ──► Linear (16 ──► 8)│
   └────────────────────────────┬────────────────────────────┘
                                ▼
                    Logits (8) ──► Softmax ──► Argmax: "is" (Index 6)[cite: 1]

```

---

### SLIDE 6: BA ĐIỂM NGHẼN BẢN CHẤT CỦA MLP

```
   ┌───────────────────────┐   Ma trận W gắn cứng với kích thước cố định L[cite: 1, 3].
   │ 1. CỬA SỔ CỐ ĐỊNH     │──►• Câu ngắn: Bắt buộc nhồi  dư thừa[cite: 1, 3].
   │ (Fixed Window)        │   • Câu dài hơn L: Cắt cụt, mất hoàn toàn dữ liệu[cite: 1, 3].
   └───────────────────────┘
   ┌───────────────────────┐   Ép phẳng làm mất trục thời gian[cite: 1, 3]. 
   │ 2. MẤT TÍNH TUẦN TỰ   │──►Mạng xem từ ở vị trí 1 và từ ở vị trí 5 là hai tọa độ 
   │ (Non-sequential)      │   độc lập, không nhận diện được quy luật dịch chuyển[cite: 1, 3].
   └───────────────────────┘
   ┌───────────────────────┐   Số tham số tầng Linear = W1 * (L x d)[cite: 1, 3].
   │ 3. BÙNG NỔ THAM SỐ    │──►Độ dài ngữ cảnh tăng gấp đôi khiến trọng số tăng gấp đôi,
   │ (Parameter Explosion) │   dễ gây quá khớp (overfitting) và tốn bộ nhớ[cite: 1, 3].
   └───────────────────────┘

```

---

### SLIDE 7: BƯỚC TIẾN 1D-CNN: CỬA SỔ TRƯỢT KERNEL (N-GRAM)

1D-CNN khắc phục việc gắn cứng vị trí bằng cách dùng Kernel trượt qua từng bước thời gian[cite: 1, 3]:

```
  Ma trận đầu vào X (5 từ x 4 chiều)           Kernel W (2 từ x 4 chiều)
  [ H1: "We"       ]                            [ w_11, w_12, w_13, w_14 ]
  [ H2: "are"      ] ◄── Trượt Bước 1 ────────  [ w_21, w_22, w_23, w_24 ]  ──► c1 = 1.81[cite: 1]
  [ H3: "learning" ] ◄── Trượt Bước 2 (are-learning)                        ──► c2 = 0.62[cite: 1]
  [ H4: "AI"       ] ◄── Trượt Bước 3 (learning-AI)                         ──► c3 = -0.16[cite: 1]
  [ H5: ""    ] ◄── Trượt Bước 4 (AI-)                            ──► c4 = 1.47[cite: 1]

                      Feature Map: [ 1.81,  0.62,  -0.16,  1.47 ][cite: 1]
                                           │
                                           ▼ ReLU: max(0, x)[cite: 1]
                                   [ 1.81,  0.62,   0.00,  1.47 ][cite: 1]
                                           │
                                           ▼ Global Max-Pooling: Lấy giá trị lớn nhất[cite: 1, 3]
                                      v = 1.81 (Đặc trưng N-gram mạnh nhất)[cite: 1]

```

---

### SLIDE 8: VÌ SAO 1D-CNN VẪN CHƯA TỐI ƯU CHO CHUỖI DÀI?

```
  VẤN ĐỀ 1: TẦM NHÌN BỊ BÓ HẸP (LIMITED RECEPTIVE FIELD)
  ┌─────────────┐
  │ Kernel (k=2)│ ──► Chỉ bắt được từng cặp từ đứng cạnh nhau (Bigram)[cite: 1, 3].
  └─────────────┘     Không thể liên kết chủ ngữ đầu câu với vị ngữ cuối đoạn văn dài[cite: 3].

  VẤN ĐỀ 2: MAX-POOLING XÓA BỎ THỨ TỰ THỜI GIAN
               [ c1: "We are" ]         = 1.81  ──┐
               [ c2: "are learning" ]   = 0.62    │ Global Max-Pool
               [ c3: "learning AI" ]    = 0.00    ├────────────────► Max = 1.81[cite: 1]
               [ c4: "AI " ]       = 1.47  ──┘
  ► Max-Pooling chỉ biết 1.81 là lớn nhất, nhưng HOÀN TOÀN QUÊN 1.81 xuất hiện ở đầu hay cuối câu[cite: 3]!

```

---

### SLIDE 9: BẢNG SO SÁNH: MLP vs. 1D-CNN vs. RNN

| Tiêu chí đối sánh | MLP (Feedforward) | 1D-CNN (Convolutional) | Recurrent Neural Network (RNN) |
| --- | --- | --- | --- |
| **Độ dài ngữ cảnh đầu vào** | Cố định cứng, phải đệm padding[cite: 1, 3] | Cửa sổ trượt cố định theo $k$[cite: 1, 3] | **Co giãn linh hoạt theo độ dài chuỗi**[cite: 1, 3] |
| **Bảo toàn thứ tự tuần tự** | Bị xóa sạch sau phép Flatten[cite: 1, 3] | Giữ được trật tự cục bộ N-gram[cite: 1, 3] | **Duy trì trật tự toàn vẹn theo thời gian**[cite: 1, 3] |
| **Cơ chế chia sẻ trọng số** | Không chia sẻ (Độc lập vị trí)[cite: 1, 3] | Chia sẻ trọng số theo không gian

 | **Chia sẻ trọng số xuyên suốt thời gian**[cite: 1, 3] |
| **Bộ nhớ tích lũy** | Không có bộ nhớ[cite: 1, 3] | Gián tiếp qua độ sâu filter | **Bộ nhớ trạng thái ẩn ($h_t$) trực tiếp**[cite: 1, 3] |
| **Tăng trưởng số tham số** | Tăng vọt theo độ dài $(L \cdot d)$[cite: 1, 3] | Phụ thuộc số filter, độc lập $L$[cite: 1, 3] | **Hằng số, hoàn toàn không phụ thuộc $L$**[cite: 1, 3] |

---

### SLIDE 10: Ý TƯỞNG CỐT LÕI CỦA RNN: TRẠNG THÁI ẨN ($h_t$)

**Trực giác:** Con người không bắt đầu tư duy lại từ đầu ở từng chữ cái, mà liên tục duy trì một dòng ý thức nén thông tin quá khứ.

```
                     DÒNG THỜI GIAN TUẦN TỰ (TIME STEPS)
               t = 1                  t = 2                  t = 3
           "Tôi"                  "đang"                 "học"
             │                      │                      │
             ▼                      ▼                      ▼
  h_0=0 ──► [ RNN ] ── h_1 ───────► [ RNN ] ── h_2 ──────► [ RNN ] ── h_3 ──► ...
             │                      │                      │
             └──────────────────────┴──────────────────────┘
             h_t chính là "Trí nhớ" nén toàn bộ quá khứ:
             • h_1: Nhớ từ "Tôi"
             • h_2: Nhớ ngữ cảnh ("Tôi" + "đang")
             • h_3: Nhớ toàn bộ ("Tôi" + "đang" + "học")

```

---

### SLIDE 11: CÔNG THỨC TOÁN HỌC & BỘ BA TRỌNG SỐ ($W, U, V$)

Trái tim toán học của mạng RNN được định nghĩa qua hai phương trình cơ sở[cite: 1, 3]:

$$h_t = \tanh(\mathbf{W} \cdot x_t + \mathbf{U} \cdot h_{t-1} + b_h)$$

[cite: 1, 3]

$$\hat{y}_t = \mathbf{V} \cdot h_t + b_y$$

[cite: 1, 3]

```
               ┌───────────────────────────────────────────────┐
               │              KẾT QUẢ DỰ ĐOÁN (y_t)            │
               └───────────────────────▲───────────────────────┘
                                       │
                                       │ Ma trận V (Hidden ──► Output)[cite: 1, 3]
                                       │ Đọc bộ nhớ h_t để đưa ra quyết định[cite: 1]
                                       │
                      ┌────────────────┴───────────────┐
                      │    TRẠNG THÁI ẨN MỚI (h_t)     │
                      └────────▲───────────────▲───────┘
                               │               │
       Ma trận U (Hidden-to-Hidden)[cite: 1, 3]    │               │ Ma trận W (Input-to-Hidden)[cite: 1, 3]
       TRÁI TIM CỦA RNN:               │               │ Tiếp nhận thông tin mới[cite: 1, 3]
       Duy trì trí nhớ cũ h_(t-1)[cite: 1, 3]      │               │ từ quan sát hiện tại x_t[cite: 1]
                      ┌────────┴───────┐       │
                      │  h_(t-1) (Cũ)  │       │
                      └────────────────┘       │
                                        ┌──────┴───────┐
                                        │ Đầu vào x_t  │
                                        └──────────────┘

```

---

### SLIDE 12: NGUYÊN LÝ CHIA SẺ TRỌNG SỐ (WEIGHT SHARING)

Mạng xử lý chuỗi dài 5 bước hay 1.000 bước đều **dùng chung một bộ ma trận duy nhất**[cite: 1, 3]:

```
   Thời điểm t=1:   h_1 = tanh( [W]·x_1 + [U]·h_0 + b )  ──► y_1 = [V]·h_1
   Thời điểm t=2:   h_2 = tanh( [W]·x_2 + [U]·h_1 + b )  ──► y_2 = [V]·h_2
   Thời điểm t=3:   h_3 = tanh( [W]·x_3 + [U]·h_2 + b )  ──► y_3 = [V]·h_3
                                    ▲       ▲                      ▲
                                    └───────┴──────────────────────┘
                          DÙNG CHUNG BỘ TRỌNG SỐ CHO MỌI THỜI ĐIỂM[cite: 1, 3]

```

* **Lợi ích:** Tổng số lượng tham số độc lập tuyệt đối với chiều dài chuỗi dữ liệu[cite: 1, 3].
* **Tổng quát hóa:** Giúp mô hình nhận diện được mẫu hình tương đồng dù nó xuất hiện ở đầu hay cuối chuỗi.



---

### SLIDE 13: ĐỒ THỊ TÍNH TOÁN DẠNG MỞ CUỘN (UNFOLDED COMPUTATION GRAPH)

Một ô nhớ RNN hồi quy tương đương với một **Mạng truyền thẳng cực sâu (Deep Feedforward Network)** có độ sâu bằng $T$:

```
   DẠNG CUỘN (FOLDED)                 DẠNG MỞ CUỘN THEO THỜI GIAN (UNFOLDED)
        y_t                                y_1            y_2            y_T
         ▲                                  ▲              ▲              ▲
         │ (V)                              │ (V)          │ (V)          │ (V)
      ┌─────┐                            ┌─────┐        ┌─────┐        ┌─────┐
      │ h_t │ ↺ (U)       ──►            │ h_1 │ ──U──► │ h_2 │ ──U──► │ h_T │
      └─────┘                            └─────┘        └─────┘        └─────┘
         ▲                                  ▲              ▲              ▲
         │ (W)                              │ (W)          │ (W)          │ (W)
        x_t                                x_1            x_2            x_T

```

---

### SLIDE 14: CÁC DẠNG KIẾN TRÚC TƯƠNG TÁC CHUỖI CỦA RNN

```
  1. ONE-TO-MANY (Sinh chuỗi)        2. MANY-TO-ONE (Phân loại / Dự báo)
       [y1]   [y2]   [y3]                                [y_final]
        ▲      ▲      ▲                                      ▲
     ┌──┴──────┴──────┴──┐                               ┌──┴────────────────┐
     │      Mạng RNN     │                               │      Mạng RNN     │
     └──▲────────────────┘                               └──▲──────▲──────▲──┘
        │                                                   │      │      │
       [x] (Ảnh đầu vào)                                  [x1]   [x2]   [x3] (Review câu)[cite: 3]

  3. MANY-TO-MANY ĐỒNG BỘ            4. MANY-TO-MANY BẤT ĐỒNG BỘ (Seq2Seq)
       [y1]   [y2]   [y3]                                         [y1]   [y2]
        ▲      ▲      ▲                                            ▲      ▲
     ┌──┴──────┴──────┴──┐                               ┌─────┐       ┌──┴──────┴──┐
     │      Mạng RNN     │                               │ Enc │ ──►   │    Dec     │
     └──▲──────▲──────▲──┘                               └──▲──┘       └────────────┘
        │      │      │                                     │
      [x1]   [x2]   [x3] (Gán từ loại POS)[cite: 3]              [x1, x2] (Dịch máy: Anh ──► Việt)[cite: 3]

```

---

### SLIDE 15: CƠ CHẾ HUẤN LUYỆN BPTT (BACKPROPAGATION THROUGH TIME)

Mô hình tính toán sai số tại mọi thời điểm và lan truyền ngược gradient ngược dòng thời gian từ $T$ về $1$[cite: 1, 3]:

```
  DÒNG LAN TRUYỀN XUÔI (FORWARD PASS)
  x_1 ──► [ h_1 ] ──(U)──► [ h_2 ] ──(U)──► [ h_3 ] ──► Loss L_3
             ▲                ▲                ▲
             │                │                │
  DÒNG GRADIENT NGƯỢC (BPTT - BACKWARD PASS)   │
             │                │                │
             └──── dL/dh_1 ◄──┴──── dL/dh_2 ◄──┴────── dL/dh_3[cite: 3]

```

$$\frac{\partial L}{\partial U} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial L_t}{\partial h_t} \cdot \left( \prod_{j=k+1}^t \frac{\partial h_j}{\partial h_{j-1}} \right) \cdot \frac{\partial h_k}{\partial U}$$

---

### SLIDE 16: VẤN ĐỀ TRIỆT TIÊU GRADIENT (VANISHING GRADIENT)

**Bản chất:** Phép nhân chuỗi ma trận $U$ liên tiếp qua $T-k$ bước thời gian:

```
                      Đạo hàm tanh(z) nằm trong khoảng (0, 1][cite: 3]
                                         │
   dL/dh_k  =  dL/dh_t  ×  [ diag(1 - h^2) · U ] × ... × [ diag(1 - h^2) · U ][cite: 3]
               └─────────────────────── T - k lần nhân ───────────────────────┘

```

* **Khi trị riêng lớn nhất của $U < 1$:**

$$\Vert{}U^{T-k}\Vert{} \longrightarrow 0 \quad (\text{khi chuỗi dài ra})[cite: 3]$$

* **Hậu quả:** Tín hiệu đạo hàm ở các bước đầu tiên suy giảm theo hàm mũ về 0[cite: 1, 3]. Trọng số không thể cập nhật để học các liên kết ngữ cảnh quá khứ xa[cite: 1, 3].

---

### SLIDE 17: HIỆN TƯỢNG NỔ GRADIENT & GRADIENT CLIPPING

```
  HIỆN TƯỢNG NỔ GRADIENT (EXPLODING GRADIENT)
  • Khi trị riêng lớn nhất của U > 1: ||U^(T-k)|| bùng nổ vô tận theo hàm mũ[cite: 3].
  • Bước nhảy trọng số quá lớn phá hủy vùng cực tiểu, làm tràn số (NaN / Inf)[cite: 3].

  GIẢI PHÁP: CẮT TỈA GRADIENT (GRADIENT NORM CLIPPING)
                     g_clipped = g * (theta / ||g||)   khi ||g|| > theta[cite: 3]

              Vector ban đầu (Quá dài gây nổ)
              ──────────────────────────────────────────────►  (||g|| = 15.2)
              
              Vector sau khi Clip (Giữ nguyên hướng, co độ dài)
              ─────────────►  (||g_clipped|| = theta = 1.0)[cite: 1]

```

---

### SLIDE 18: TỔNG KẾT ĐIỂM NGHẼN CỦA SIMPLE RNN

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │ 1. KHÔNG CÓ CƠ CHẾ CHỌN LỌC (Unselective Memory)                       │
  │    Mọi bước thời gian đều bị nén qua một hàm tanh duy nhất, thông tin  │
  │    quan trọng dễ bị thông tin rác làm loãng[cite: 1, 3].                            │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. MẤT TRÍ NHỚ DÀI HẠN (Short-term Memory Horizon)                     │
  │    Do triệt tiêu gradient, RNN thực tế chỉ nhớ được từ 5 đến 10 bước   │
  │    thời gian gần nhất[cite: 1, 3].                                                 │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. BẮT BUỘC TÍNH TOÁN TUẦN TỰ (Sequential Bottleneck)                  │
  │    h_t chỉ tính được khi đã có h_(t-1) ──► KHÔNG THỂ SONG SONG HÓA     │
  │    trên GPU như Transformer hay CNN[cite: 3].                                  │
  └────────────────────────────────────────────────────────────────────────┘

```

---

### SLIDE 19: THIẾT LẬP THỰC NGHIỆM CHUỖI TÀI CHÍNH

Kiểm chứng hiệu năng của RNN trên 2 tập dữ liệu thực tế lớn từ Kaggle[cite: 1, 3]:

* **Tập 1:** Chuỗi giá vàng & bạc hàng ngày (Gold & Silver daily prices, 1968–2021).


* **Tập 2:** Chuỗi biến động giá & khối lượng cổ phiếu Amazon (AMZN, 1997–2023).


* **Cửa sổ trượt:** 30 ngày lịch sử ($L=30$) để dự đoán bước tiếp theo ($t+1$)[cite: 1, 3].
* **Baseline đối chứng:** Phương pháp Naive / Persistence ($\hat{y}_{t+1} = y_t$ — Lấy giá hôm nay đoán cho ngày mai)[cite: 1, 3].

---

### SLIDE 20: KẾT QUẢ THỰC NGHIỆM & HIỆN TƯỢNG NGHỊCH LÝ

Bảng so sánh độ lệch sai số căn quân phương (RMSE trên tập Test)[cite: 1, 3]:

| Tập dữ liệu thử nghiệm | Mô hình Naive (Baseline) | PyTorch Simple RNN | Keras Simple RNN | Đánh giá |
| --- | --- | --- | --- | --- |
| **Giá Vàng (Gold Prices)** | **15.48**[cite: 1, 3] | **15.45**[cite: 1, 3] | **16.42**[cite: 1, 3] | *Keras RNN chạy tệ hơn cả Naive*[cite: 1, 3] |
| **Cổ Phiếu Amazon (AMZN)** | **3.14**[cite: 1, 3] | **3.13**[cite: 1, 3] | **3.18**[cite: 1, 3] | *Xấp xỉ phương pháp Naive*[cite: 1, 3] |

```
  NGHỊCH LÝ QUAN SÁT:
  Một mạng nơ-ron học sâu phức tạp huấn luyện hàng chục epoch kết quả lại chỉ tương 
  đương, thậm chí kém hơn cả một thuật toán "lười biếng" lấy giá hôm trước làm dự đoán[cite: 1, 3]!

```

---

### SLIDE 21: BẢN CHẤT THẤT BẠI: DỊCH CHUYỂN PHÂN PHỐI (DISTRIBUTION SHIFT)

Tại sao Simple RNN lại thất bại ở bài toán dự báo giá kim loại?

```
  PHÂN PHỐI DỮ LIỆU TRAIN VS TEST:
  [Tập Train] Giá cao nhất: 850.00 USD[cite: 1, 3]
  ═══════════════════════════════════════════════════════
  [Tập Test]  Giá thấp nhất: 1,049.40 USD  ──► 100% dữ liệu Test > Train Max[cite: 1, 3]!

  ◄────── Miền Tập Train ──────►                ◄────── Miền Tập Test ──────►
  [        Giá < 850          ]                 [        Giá > 1049         ]
  [       (ĐÃ ĐƯỢC HỌC)       ]                 [     (CHƯA GẶP BAO GIỜ)    ]
               ▲                                              ▲
               │                                              │
        NỘI SUY TỐT                                    NGOẠI SUY BẤT LỰC[cite: 3]

```

* **Bài học tiền xử lý:** Mạng nơ-ron không thể ngoại suy trên vùng số liệu mới.


* **Giải pháp khắc phục:** Không dự đoán mức giá tuyệt đối, phải chuyển thành tỷ suất sinh lời dừng (**Log-return**): $r_t = \ln(P_t / P_{t-1})$[cite: 1, 3].

---

### SLIDE 22: BƯỚC TIẾN HÓA LSTM: ĐƯỜNG DẪN TRÍ NHỚ DÀI HẠN

Long Short-Term Memory bổ sung đường truyền thẳng **Cell State ($C_t$)** không bị cản trở bởi phép nhân ma trận lặp lại[cite: 1, 3]:

```
                     ĐƯỜNG CAO TỐC CELL STATE (C_t)[cite: 3]
  C_(t-1) ─────────────( ⊗ )──────────────────────( ⊕ )───────────────► C_t
                         ▲                          ▲
                         │ Forget Gate (f_t)        │ Input Gate (i_t)
                    ┌────┴─────┐               ┌────┴─────┐
                    │ "Bỏ bớt  │               │ "Ghi thêm│
                    │ cái cũ"  │               │  cái mới"│
                    └──────────┘               └──────────┘
                         ▲                          ▲
  h_(t-1) ───────────────┴──────────────────────────┴──────( ⊗ )──────► h_t
                                                             ▲
                                                Output Gate (o_t)[cite: 1, 3]

```

* **Cổng Quên ($f_t$):** Xóa bỏ các ký ức không còn phù hợp[cite: 1, 3].
* **Cổng Ghi ($i_t$):** Chọn lọc thông tin mới đáng chú ý nạp vào bộ nhớ dài hạn[cite: 1, 3].
* **Cổng Xuất ($o_t$):** Quyết định trích xuất thông tin gì ra ngoài trạng thái ẩn[cite: 1, 3].

---

### SLIDE 23: TINH GIẢN VỚI GRU (GATED RECURRENT UNIT)

GRU rút gọn cấu trúc của LSTM, gộp Cell State và Hidden State thành một trạng thái duy nhất[cite: 1, 3]:

```
            ┌───────────────────────────────────────────────┐
            │          CƠ CHẾ 2 CỔNG CỦA MẠNG GRU           │
            └───────────────────────┬───────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
       CỔNG CẬP NHẬT (UPDATE GATE z_t)     CỔNG ĐẶT LẠI (RESET GATE r_t)
       Cân bằng giữa việc giữ lại trí      Quyết định xem trạng thái quá khứ
       nhớ cũ và ghi đè trạng thái mới[cite: 1, 3].    sẽ kết hợp bao nhiêu với đầu vào[cite: 3].

```

* **Tối ưu:** Giảm bớt 25% số lượng tham số so với LSTM, tốc độ huấn luyện nhanh hơn rõ rệt mà hiệu quả thực nghiệm tương đương[cite: 1, 3].

---

### SLIDE 24: TỔNG KẾT & BỨC TRANH TOÀN CẢNH

```
                 TIẾN TRÌNH CÔNG NGHỆ MÔ HÌNH HÓA DỮ LIỆU CHUỖI

  MLP / 1D-CNN (2012)        RNN THUẦN (1986-1990)       LSTM / GRU (1997-2014)     TRANSFORMER (2017+)
  • Ép phẳng, trượt cục bộ   • Bộ nhớ ẩn h_t             • Cơ chế cổng kiểm soát    • Cơ chế Self-Attention
  • Mất tính tuần tự dài     • Bị triệt tiêu gradient    • Nhớ dài hạn rất tốt      • Xử lý song song tuyệt đối
  • Chỉ phù hợp chuỗi ngắn   • Dễ nổ đạo hàm             • Chuẩn mực Time-series    • Thống trị lĩnh vực LLM

```

* **Thông điệp kết luận:** Simple RNN đã đặt nền móng lý thuyết mang tính lịch sử về việc chia sẻ trọng số thời gian và trạng thái ẩn[cite: 1, 3]. Hiểu rõ các điểm nghẽn toán học của RNN chính là chìa khóa để làm chủ toàn bộ các mô hình học sâu chuỗi hiện đại.