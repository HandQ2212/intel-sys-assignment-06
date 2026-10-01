html_content = """<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>Mạng Nơ-ron Hồi Quy (RNN)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reset.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/dracula.min.css" id="theme">
    
    <style>
        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {
            text-transform: none;
            font-family: 'Times New Roman', Times, serif;
        }
        .reveal p, .reveal li {
            font-size: 0.8em;
            text-align: left;
        }
        .reveal ul {
            display: block;
        }
        .webgl-container { 
            width: 100%; 
            height: 500px; 
            margin: 0 auto; 
            position: relative; 
            border: 1px solid #444; 
            border-radius: 8px;
            background-color: #1E1E2E;
        }
        .instruction { font-size: 0.5em !important; color: #6272a4 !important; text-align: center !important;}
        .highlight-blue { color: #8be9fd; }
        .highlight-green { color: #50fa7b; }
        .highlight-orange { color: #ffb86c; }
        .highlight-red { color: #ff5555; }
        .code-block {
            background-color: #282a36;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.55em;
            text-align: left;
            white-space: pre;
            line-height: 1.2;
        }
        table {
            font-size: 0.55em !important;
            width: 100%;
        }
        th { background-color: #44475a !important; }
        td, th { padding: 8px !important; border: 1px solid #6272a4 !important; }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">

            <!-- SLIDE 1 -->
            <section>
                <h2>MẠNG NƠ-RON HỒI QUY (RNN)</h2>
                <h4>Từ Hạn Chế của MLP & 1D-CNN đến Nguyên Lý Xử Lý Dữ Liệu Chuỗi</h4>
                <br>
                <p style="text-align: center;"><strong>Nhóm thực hiện:</strong><br>
                Văn Thị Mai Linh • Nguyễn Văn Minh Lực<br>
                Giáp Minh Hiếu • Nguyễn Nam Hải</p>
                <br>
                <p style="text-align: center; font-style: italic; color: #f1fa8c;">
                "Feedforward nhìn thế giới qua từng bức ảnh rời rạc;<br>
                RNN thấu hiểu dữ liệu qua dòng chảy liên tục của thời gian."
                </p>
                <p class="instruction">Bấm phím Mũi tên Trái/Phải để chuyển Slide</p>
            </section>

            <!-- SLIDE 2 -->
            <section>
                <h3>Bản chất Dữ liệu dạng Chuỗi</h3>
                <p><strong>Thứ tự xuất hiện quyết định hoàn toàn ngữ nghĩa của dữ liệu.</strong></p>
                <div class="code-block">
[CHUỖI RỜI RẠC: NLP / VĂN BẢN]
"Hà Nội không mưa"   ≠   "Mưa không Hà Nội"
     (Có nghĩa)               (Vô nghĩa)

[CHUỖI LIÊN TỤC: TIME-SERIES / TÀI CHÍNH]
Giá vàng: [ 82.5 ──► 83.1 ──► 84.0 ──► 85.2 ]  (Tăng đều)
Giá vàng: [ 85.2 ──► 84.0 ──► 83.1 ──► 82.5 ]  (Giảm sâu)
                </div>
                <ul>
                    <li><strong>Đặc tính trật tự:</strong> Mỗi điểm tại $t$ tương quan mật thiết với $t-1, t-2, \dots$</li>
                </ul>
            </section>

            <!-- SLIDE 3 -->
            <section>
                <h3>Bài toán Dự đoán Phần tử Kế tiếp</h3>
                <p><strong>Mục tiêu:</strong> Cho chuỗi quan sát quá khứ $X = (x_1, x_2, \dots, x_t)$, dự đoán $x_{t+1}$.</p>
                <div class="code-block">
BÀI TOÁN 1: NEXT WORD PREDICTION (NLP)
Ngữ cảnh: "We" ──► "are" ──► "learning" ──► "AI" ──► [ ? ]
                                                     │
                                            Target kỳ vọng: "is"

BÀI TOÁN 2: DỰ BÁO CHUỖI THỜI GIAN (TIME-SERIES)
Cửa sổ trượt: [ P(t-29), P(t-28), ... , P(t-1), P(t) ]  ──►  [ P(t+1) ]
              └─────────────── 30 ngày lịch sử ──────┘        Biến động
                </div>
            </section>

            <!-- SLIDE 5 -->
            <section>
                <h3>Tiếp cận bằng MLP & Ép phẳng</h3>
                <p>MLP bắt buộc biến toàn bộ ngữ cảnh thành một vector phẳng duy nhất.</p>
                <div class="code-block" style="font-size: 0.5em;">
Token 1: "We"       [ -0.18,  0.55,  1.62,  0.70 ] (1x4)
Token 2: "are"      [  0.22,  1.32,  0.13,  2.05 ] (1x4)
Token 3: "learning" [  0.43, -1.30, -0.88,  1.59 ] (1x4)  ──┐
Token 4: "AI"       [  1.02, -1.90,  0.31,  0.42 ] (1x4)    │ Concatenate
Token 5: [PAD]      [  1.78, -0.82, -0.27,  1.35 ] (1x4)  ──┘
                             │
                             ▼
      Vector X_concat: [1 x 20 chiều] (Phẳng hoàn toàn)
                             │
                             ▼
  Linear Layer (20 ──► 16) ──► ReLU ──► Linear (16 ──► 8)
                             │
                             ▼
                 Logits ──► Softmax ──► "is"
                </div>
            </section>
            
            <!-- SLIDE 9 -->
            <section>
                <h3>Bảng So sánh: MLP vs. 1D-CNN vs. RNN</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Tiêu chí đối sánh</th>
                            <th>MLP (Feedforward)</th>
                            <th>1D-CNN</th>
                            <th class="highlight-blue">RNN</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Độ dài ngữ cảnh đầu vào</td>
                            <td>Cố định cứng</td>
                            <td>Cố định theo Kernel</td>
                            <td class="highlight-blue">Co giãn linh hoạt</td>
                        </tr>
                        <tr>
                            <td>Bảo toàn thứ tự</td>
                            <td>Bị xóa sạch (Flatten)</td>
                            <td>Giữ trật tự cục bộ</td>
                            <td class="highlight-blue">Duy trì toàn vẹn</td>
                        </tr>
                        <tr>
                            <td>Chia sẻ trọng số</td>
                            <td>Không có</td>
                            <td>Theo không gian</td>
                            <td class="highlight-blue">Xuyên suốt thời gian</td>
                        </tr>
                        <tr>
                            <td>Bộ nhớ tích lũy</td>
                            <td>Không có</td>
                            <td>Gián tiếp (Filter)</td>
                            <td class="highlight-blue">Trực tiếp ($h_t$)</td>
                        </tr>
                        <tr>
                            <td>Số lượng tham số</td>
                            <td>Tăng vọt theo $L$</td>
                            <td>Độc lập $L$</td>
                            <td class="highlight-blue">Hằng số, độc lập $L$</td>
                        </tr>
                    </tbody>
                </table>
            </section>

            <!-- SLIDE 11 -->
            <section>
                <h3>Công thức Toán học & Bộ 3 Trọng số</h3>
                <p>Hai phương trình cơ sở định nghĩa RNN:</p>
                <p style="text-align: center; font-size: 1.2em;" class="highlight-green">
                    $h_t = \tanh(W \cdot x_t + U \cdot h_{t-1} + b_h)$<br>
                    $\hat{y}_t = V \cdot h_t + b_y$
                </p>
                <ul>
                    <li><strong>$U$ (Hidden-to-Hidden):</strong> Duy trì trí nhớ cũ $h_{t-1}$</li>
                    <li><strong>$W$ (Input-to-Hidden):</strong> Tiếp nhận thông tin mới từ $x_t$</li>
                    <li><strong>$V$ (Hidden-to-Output):</strong> Đọc bộ nhớ $h_t$ để ra quyết định $y_t$</li>
                </ul>
            </section>

            <!-- SLIDE 13 (WebGL DEMO) -->
            <section>
                <h3>Đồ thị Mở cuộn theo thời gian (WebGL 3D)</h3>
                <p class="instruction">Dùng chuột kéo xoay mô hình, cuộn để Zoom. Tự động Auto-Rotate.</p>
                <div id="webgl-unfold" class="webgl-container"></div>
                <p style="text-align: center; font-size: 0.7em;">
                    <span style="color:#50fa7b">■ Input ($x_t$)</span> &nbsp;&nbsp;
                    <span style="color:#8be9fd">● Hidden ($h_t$)</span> &nbsp;&nbsp;
                    <span style="color:#ffb86c">■ Output ($y_t$)</span>
                </p>
            </section>

            <!-- SLIDE 15 -->
            <section>
                <h3>Cơ chế Huấn luyện (BPTT)</h3>
                <p>Backpropagation Through Time: Lan truyền ngược gradient ngược dòng thời gian.</p>
                <div class="code-block" style="font-size: 0.5em;">
DÒNG LAN TRUYỀN XUÔI (FORWARD PASS)
x_1 ──► [ h_1 ] ──(U)──► [ h_2 ] ──(U)──► [ h_3 ] ──► Loss L_3
           ▲                ▲                ▲
           │                │                │
DÒNG GRADIENT NGƯỢC (BPTT - BACKWARD PASS)   │
           │                │                │
           └──── dL/dh_1 ◄──┴──── dL/dh_2 ◄──┴────── dL/dh_3
                </div>
                <p style="text-align: center; font-size: 0.8em;" class="highlight-red">
                    $\frac{\partial L}{\partial U} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial L_t}{\partial h_t} \cdot \left( \prod_{j=k+1}^t \frac{\partial h_j}{\partial h_{j-1}} \right) \cdot \frac{\partial h_k}{\partial U}$
                </p>
            </section>

            <!-- SLIDE 21 -->
            <section>
                <h3>Nguyên nhân Thất bại: Distribution Shift</h3>
                <ul>
                    <li><strong>Tập Train:</strong> Giá cao nhất 850 USD</li>
                    <li><strong>Tập Test:</strong> Giá thấp nhất 1049 USD $\to$ Ngoại suy bất lực.</li>
                </ul>
                <p><strong>Khắc phục (Tiền xử lý):</strong><br> Dự đoán tỷ suất sinh lời dừng <strong>(Log-return)</strong>: <br><span class="highlight-blue">$r_t = \ln(P_t / P_{t-1})$</span></p>
            </section>

            <!-- SLIDE 24 -->
            <section>
                <h3>Tổng kết: Tiến trình Công nghệ</h3>
                <table>
                    <thead>
                        <tr>
                            <th>MLP / CNN</th>
                            <th>RNN THUẦN</th>
                            <th>LSTM / GRU</th>
                            <th>TRANSFORMER</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Ép phẳng, trượt cục bộ</td>
                            <td>Bộ nhớ ẩn $h_t$</td>
                            <td class="highlight-blue">Cơ chế cổng kiểm soát</td>
                            <td class="highlight-green">Self-Attention</td>
                        </tr>
                        <tr>
                            <td>Chỉ phù hợp chuỗi ngắn</td>
                            <td>Bị triệt tiêu gradient</td>
                            <td class="highlight-blue">Nhớ dài hạn tốt</td>
                            <td class="highlight-green">Xử lý song song</td>
                        </tr>
                    </tbody>
                </table>
            </section>

        </div>
    </div>

    <!-- Reveal JS & Plugins -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/plugin/math/math.min.js"></script>
    <!-- Three JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <script>
        // Khởi tạo Reveal.js
        Reveal.initialize({
            hash: true,
            controls: true,
            progress: true,
            center: true,
            transition: 'slide',
            plugins: [ RevealMath.KaTeX ]
        });

        // ==========================================
        // TẠO SCENE WEBGL (THREE.JS) CHO UNROLLED RNN
        // ==========================================
        const container = document.getElementById('webgl-unfold');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1E1E2E);
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
        camera.position.set(0, 0, 18);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 1.0;

        // Ánh sáng
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 15, 10);
        scene.add(pointLight);

        // Vẽ mạng RNN Unrolled
        const timesteps = 6;
        const spacing = 3.2;
        const nodes = [];
        
        for(let i = 0; i < timesteps; i++) {
            const xPos = (i - (timesteps-1)/2) * spacing;

            // Input (x_t)
            const xMat = new THREE.MeshPhongMaterial({color: 0x50fa7b});
            const xMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), xMat);
            xMesh.position.set(xPos, -3.5, 0);
            scene.add(xMesh);
            
            // Hidden (h_t)
            const hMat = new THREE.MeshPhongMaterial({color: 0x8be9fd, shininess: 80});
            const hMesh = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), hMat);
            hMesh.position.set(xPos, 0, 0);
            scene.add(hMesh);
            nodes.push(hMesh);
            
            // Output (y_t)
            const yMat = new THREE.MeshPhongMaterial({color: 0xffb86c});
            const yMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), yMat);
            yMesh.position.set(xPos, 3.5, 0);
            scene.add(yMesh);

            // W Matrix (Input -> Hidden)
            const matLine = new THREE.LineBasicMaterial({color: 0xffffff, transparent: true, opacity: 0.3});
            const geo1 = new THREE.BufferGeometry().setFromPoints([xMesh.position, hMesh.position]);
            scene.add(new THREE.Line(geo1, matLine));

            // V Matrix (Hidden -> Output)
            const geo2 = new THREE.BufferGeometry().setFromPoints([hMesh.position, yMesh.position]);
            scene.add(new THREE.Line(geo2, matLine));

            // U Matrix (Hidden(t-1) -> Hidden(t))
            if (i > 0) {
                const prevH = nodes[i-1];
                const dir = new THREE.Vector3().subVectors(hMesh.position, prevH.position).normalize();
                const length = prevH.position.distanceTo(hMesh.position);
                const arrowHelper = new THREE.ArrowHelper(dir, prevH.position, length - 1.2, 0xff79c6, 0.5, 0.5);
                scene.add(arrowHelper);
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();

        // Xử lý Resize cho chuẩn
        function resizeWebGL() {
            if (container.clientWidth > 0 && container.clientHeight > 0) {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }
        }
        window.addEventListener('resize', resizeWebGL);
        Reveal.on( 'slidechanged', resizeWebGL );
    </script>
</body>
</html>
"""

with open('rnn_webgl_slides.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
