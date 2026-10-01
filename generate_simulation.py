html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Mô phỏng RNN & BPTT bằng WebGL</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #1e1e2e; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #canvas-container { width: 100vw; height: 100vh; }
        #ui { position: absolute; top: 20px; left: 20px; z-index: 10; background: rgba(30,30,46,0.85); padding: 20px; border-radius: 12px; border: 1px solid #44475a; box-shadow: 0 4px 6px rgba(0,0,0,0.3); width: 300px; }
        h1 { margin: 0 0 15px 0; font-size: 22px; color: #8be9fd; text-align: center; }
        button { background: #6272a4; color: white; border: none; padding: 12px 15px; margin: 8px 0; cursor: pointer; border-radius: 6px; font-weight: bold; width: 100%; transition: 0.3s; font-size: 14px; }
        button:hover { background: #50fa7b; color: #282a36; transform: translateY(-2px); }
        .legend { margin-top: 20px; font-size: 14px; border-top: 1px solid #44475a; padding-top: 15px; }
        .legend-item { display: flex; align-items: center; margin-bottom: 8px; }
        .color-box { width: 16px; height: 16px; margin-right: 12px; border-radius: 3px; }
        #status-text { margin-top: 20px; font-size: 15px; color: #f1fa8c; font-weight: bold; text-align: center; min-height: 45px;}
        .instruction { font-size: 12px; color: #a9a9b3; text-align: center; margin-top: 10px;}
    </style>
</head>
<body>
    <div id="ui">
        <h1>Mô phỏng WebGL</h1>
        <button id="btn-forward">▶ 1. Forward Pass (Mô hình RNN)</button>
        <button id="btn-backward">◀ 2. Backward Pass (BPTT)</button>
        <button id="btn-reset">↺ Đặt lại (Reset)</button>
        
        <div class="legend">
            <div class="legend-item"><div class="color-box" style="background: #50fa7b;"></div> Input ($x_t$)</div>
            <div class="legend-item"><div class="color-box" style="background: #8be9fd;"></div> Hidden State ($h_t$)</div>
            <div class="legend-item"><div class="color-box" style="background: #ffb86c;"></div> Output / Loss ($y_t$)</div>
            <div class="legend-item"><div class="color-box" style="background: #ffffff;"></div> Luồng Forward</div>
            <div class="legend-item"><div class="color-box" style="background: #ff5555;"></div> Luồng Backward (Gradient)</div>
        </div>
        <div id="status-text">Sẵn sàng.<br>Bấm nút bên trên để bắt đầu.</div>
        <div class="instruction">Dùng chuột trái để xoay không gian 3D.<br>Cuộn chuột để thu phóng.</div>
    </div>
    <div id="canvas-container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // ======= KHỞI TẠO THREE.JS =======
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x1e1e2e, 0.015);
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 30);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Ánh sáng
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 20, 20);
        scene.add(pointLight);

        // ======= DỮ LIỆU & KIẾN TRÚC RNN =======
        const timesteps = 5;
        const spacing = 5;
        const nodes = [];
        const edges = [];
        
        // Vật liệu
        const matX = new THREE.MeshPhongMaterial({color: 0x50fa7b, shininess: 100}); // Xanh lá
        const matH = new THREE.MeshPhongMaterial({color: 0x8be9fd, shininess: 100}); // Xanh dương
        const matY = new THREE.MeshPhongMaterial({color: 0xffb86c, shininess: 100}); // Cam
        
        const matEdgeNormal = new THREE.LineBasicMaterial({color: 0x44475a, transparent: true, opacity: 0.5});
        
        // Tạo các node
        for(let i=0; i<timesteps; i++) {
            const xPos = (i - (timesteps-1)/2) * spacing;
            
            // X Node
            const xMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 1.5), matX);
            xMesh.position.set(xPos, -5, 0);
            scene.add(xMesh);
            
            // H Node
            const hMesh = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), matH);
            hMesh.position.set(xPos, 0, 0);
            scene.add(hMesh);
            
            // Y Node
            const yMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 1.5), matY);
            yMesh.position.set(xPos, 5, 0);
            scene.add(yMesh);
            
            nodes.push({ x: xMesh, h: hMesh, y: yMesh });
            
            // Edges X -> H (W)
            const edgeW = new THREE.Line(
                new THREE.BufferGeometry().setFromPoints([xMesh.position, hMesh.position]),
                matEdgeNormal
            );
            scene.add(edgeW);
            edges.push({from: xMesh.position, to: hMesh.position, type: 'W'});
            
            // Edges H -> Y (V)
            const edgeV = new THREE.Line(
                new THREE.BufferGeometry().setFromPoints([hMesh.position, yMesh.position]),
                matEdgeNormal
            );
            scene.add(edgeV);
            edges.push({from: hMesh.position, to: yMesh.position, type: 'V'});
            
            // Edges H(t-1) -> H(t) (U)
            if (i > 0) {
                const edgeU = new THREE.Line(
                    new THREE.BufferGeometry().setFromPoints([nodes[i-1].h.position, hMesh.position]),
                    matEdgeNormal
                );
                scene.add(edgeU);
                edges.push({from: nodes[i-1].h.position, to: hMesh.position, type: 'U', index: i});
            }
        }

        // ======= HỆ THỐNG ANIMATION (PARTICLES) =======
        let particles = [];
        const particleGeo = new THREE.SphereGeometry(0.3, 16, 16);
        
        function spawnParticle(startPos, endPos, color, duration, delay=0, callback=null) {
            const mat = new THREE.MeshBasicMaterial({color: color});
            const mesh = new THREE.Mesh(particleGeo, mat);
            mesh.position.copy(startPos);
            mesh.visible = false;
            scene.add(mesh);
            
            particles.push({
                mesh: mesh,
                start: startPos.clone(),
                end: endPos.clone(),
                startTime: Date.now() + delay,
                duration: duration,
                callback: callback,
                active: true
            });
        }

        // ======= LOGIC MÔ PHỎNG =======
        let animationMode = "IDLE";
        const statusText = document.getElementById('status-text');

        function clearParticles() {
            particles.forEach(p => scene.remove(p.mesh));
            particles = [];
        }

        function playForward() {
            clearParticles();
            animationMode = "FORWARD";
            statusText.innerHTML = "FORWARD PASS<br><span style='color:#ffffff; font-size:12px;'>Tính toán luồng dữ liệu $X \\to H \\to Y$</span>";
            
            const duration = 800; // ms per jump
            const color = 0xffffff;
            
            for(let i=0; i<timesteps; i++) {
                const delay = i * duration;
                
                // X -> H
                spawnParticle(nodes[i].x.position, nodes[i].h.position, color, duration, delay, () => {
                    // Khi đến H, scale to lên một chút tạo hiệu ứng "nhận tín hiệu"
                    nodes[i].h.scale.set(1.3, 1.3, 1.3);
                    setTimeout(() => nodes[i].h.scale.set(1, 1, 1), 200);
                    
                    // Từ H đi lên Y
                    spawnParticle(nodes[i].h.position, nodes[i].y.position, color, duration, 0);
                    
                    // Từ H đi sang H tiếp theo (nếu có)
                    if (i < timesteps - 1) {
                        spawnParticle(nodes[i].h.position, nodes[i+1].h.position, color, duration, 0);
                    }
                });
            }
        }

        function playBackward() {
            clearParticles();
            animationMode = "BACKWARD";
            statusText.innerHTML = "BACKWARD PASS (BPTT)<br><span style='color:#ff5555; font-size:12px;'>Lan truyền ngược Gradient từ $T$ về $1$</span>";
            
            const duration = 1000;
            const color = 0xff5555; // Đỏ báo hiệu Gradient
            
            // Giả sử lỗi xuất phát từ các Output (Y), chảy ngược về H
            // Thực tế BPTT thường chạy giật lùi từ T về 1
            for(let i = timesteps - 1; i >= 0; i--) {
                const stepFromEnd = (timesteps - 1) - i;
                const delay = stepFromEnd * (duration * 0.8);
                
                // Y -> H (Gradient dL/dy -> dL/dh)
                spawnParticle(nodes[i].y.position, nodes[i].h.position, color, duration, delay, () => {
                    nodes[i].h.material.color.setHex(0xff5555);
                    setTimeout(() => nodes[i].h.material.color.setHex(0x8be9fd), 400);
                    
                    // H -> X (Gradient dL/dW)
                    spawnParticle(nodes[i].h.position, nodes[i].x.position, color, duration, 0);
                    
                    // H(t) -> H(t-1) (BPTT qua ma trận U)
                    if (i > 0) {
                        spawnParticle(nodes[i].h.position, nodes[i-1].h.position, color, duration, 0);
                    }
                });
            }
        }

        // ======= SỰ KIỆN NÚT BẤM =======
        document.getElementById('btn-forward').addEventListener('click', playForward);
        document.getElementById('btn-backward').addEventListener('click', playBackward);
        document.getElementById('btn-reset').addEventListener('click', () => {
            clearParticles();
            animationMode = "IDLE";
            statusText.innerHTML = "Đã đặt lại.<br>Sẵn sàng mô phỏng.";
            camera.position.set(0, 5, 30);
            controls.target.set(0, 0, 0);
        });

        // ======= RENDER LOOP =======
        function animate() {
            requestAnimationFrame(animate);
            controls.update();

            // Cập nhật Particles
            const now = Date.now();
            for(let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                if (!p.active) continue;
                
                if (now >= p.startTime) {
                    p.mesh.visible = true;
                    const progress = (now - p.startTime) / p.duration;
                    
                    if (progress >= 1) {
                        // Tới đích
                        p.mesh.position.copy(p.end);
                        p.active = false;
                        p.mesh.visible = false;
                        if (p.callback) p.callback();
                    } else {
                        // Đang di chuyển (Lerp)
                        p.mesh.position.lerpVectors(p.start, p.end, progress);
                    }
                }
            }
            
            renderer.render(scene, camera);
        }
        animate();

        // Responsive
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""
with open("rnn_bptt_simulation.html", "w", encoding="utf-8") as f:
    f.write(html_content)
