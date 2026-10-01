    <script>
        // 1. SETUP SCENE
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050510, 0.02);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 35);

        const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const labelRenderer = new THREE.CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none';
        document.body.appendChild(labelRenderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxPolarAngle = Math.PI / 2 - 0.1;

        // 2. GRID / ENVIRONMENT
        const gridHelper = new THREE.GridHelper(100, 100, 0x00ffff, 0x003333);
        gridHelper.position.y = -8;
        scene.add(gridHelper);

        // 3. POST-PROCESSING (BLOOM - GLOW EFFECT)
        const renderScene = new THREE.RenderPass(scene, camera);
        const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85);
        bloomPass.threshold = 0.2;
        bloomPass.strength = 1.2;
        bloomPass.radius = 0.5;

        const composer = new THREE.EffectComposer(renderer);
        composer.addPass(renderScene);
        composer.addPass(bloomPass);

        // 4. NETWORK CREATION
        const timesteps = 4;
        const spacing = 7;
        const nodes = [];
        
        const matX = new THREE.MeshBasicMaterial({color: 0x00ff00, wireframe: true});
        const matH = new THREE.MeshBasicMaterial({color: 0x00ffff, wireframe: true});
        const matY = new THREE.MeshBasicMaterial({color: 0xff9900, wireframe: true});
        const matCore = new THREE.MeshBasicMaterial({color: 0xffffff});

        function createNode(type, position, labelHtml, cssClass) {
            const group = new THREE.Group();
            group.position.copy(position);
            
            let outerGeo;
            if(type === 'x') outerGeo = new THREE.BoxGeometry(2, 2, 2);
            else if(type === 'h') outerGeo = new THREE.IcosahedronGeometry(1.5, 1);
            else outerGeo = new THREE.CylinderGeometry(1.5, 1.5, 2, 6);

            const outerMat = type === 'x' ? matX : (type === 'h' ? matH : matY);
            const outerMesh = new THREE.Mesh(outerGeo, outerMat);
            group.add(outerMesh);

            const coreMesh = new THREE.Mesh(new THREE.IcosahedronGeometry(0.4, 0), matCore);
            group.add(coreMesh);
            
            const div = document.createElement('div');
            div.className = 'node-label ' + cssClass;
            div.innerHTML = labelHtml;
            const label = new THREE.CSS2DObject(div);
            label.position.set(0, 2.5, 0);
            group.add(label);

            scene.add(group);
            return { group, outerMesh, coreMesh, label };
        }

        for(let i=0; i<timesteps; i++) {
            const xPos = (i - (timesteps-1)/2) * spacing;
            const xNode = createNode('x', new THREE.Vector3(xPos, -5, 0), `Input x<sub>${i+1}</sub>`, 'label-input');
            const hNode = createNode('h', new THREE.Vector3(xPos, 0, 0), `Hidden h<sub>${i+1}</sub>`, 'label-hidden');
            const yNode = createNode('y', new THREE.Vector3(xPos, 5, 0), `Output y<sub>${i+1}</sub>`, 'label-output');
            
            nodes.push({x: xNode, h: hNode, y: yNode});

            const matLine = new THREE.LineBasicMaterial({color: 0x444444});
            scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([xNode.group.position, hNode.group.position]), matLine));
            scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([hNode.group.position, yNode.group.position]), matLine));
            if(i > 0) {
                scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([nodes[i-1].h.group.position, hNode.group.position]), matLine));
            }
            
            xNode.group.visible = false;
            hNode.group.visible = false;
            yNode.group.visible = false;
        }

        // 5. ANIMATION SYSTEM
        let particles = [];
        const particleGeo = new THREE.SphereGeometry(0.25, 8, 8);
        
        function spawnDataFlow(start, end, colorHex, duration=600) {
            const pMat = new THREE.MeshBasicMaterial({color: colorHex});
            const pMesh = new THREE.Mesh(particleGeo, pMat);
            pMesh.position.copy(start);
            scene.add(pMesh);
            
            particles.push({
                mesh: pMesh,
                start: start.clone(),
                end: end.clone(),
                startTime: Date.now(),
                duration: duration,
                active: true
            });
        }

        // 6. GRANULAR STEP STATE MACHINE
        let stateMode = "FORWARD"; // FORWARD or BACKWARD
        let tIndex = 0; // 0 to 3
        let subPhase = 0; // 0, 1, 2 for Forward; 0, 1 for Backward

        function playNextStep() {
            if (stateMode === "FORWARD") {
                if (subPhase === 0) {
                    // X -> H
                    nodes[tIndex].x.group.visible = true;
                    spawnDataFlow(nodes[tIndex].x.group.position, nodes[tIndex].h.group.position, 0x00ff00);
                    document.getElementById('step-desc').innerHTML = `<span style="color:#0f0; font-size:16px;">[LAN TRUYỀN XUÔI - BƯỚC ${tIndex+1}] - Bước 1: Nhận Input</span><br><br>Nhận vector đặc trưng đầu vào <b>x<sub>${tIndex+1}</sub></b>.<br>Nhân với ma trận trọng số đầu vào <b>W</b>: <br><i>a = W &times; x<sub>${tIndex+1}</sub></i>`;
                    subPhase = 1;
                } 
                else if (subPhase === 1) {
                    // Update H
                    nodes[tIndex].h.group.visible = true;
                    // Flash core
                    nodes[tIndex].h.coreMesh.scale.set(3,3,3);
                    setTimeout(() => nodes[tIndex].h.coreMesh.scale.set(1,1,1), 200);

                    if (tIndex === 0) {
                        document.getElementById('step-desc').innerHTML = `<span style="color:#0ff; font-size:16px;">[LAN TRUYỀN XUÔI - BƯỚC ${tIndex+1}] - Bước 2: Cập nhật Trạng thái</span><br><br>Do là bước đầu tiên (không có quá khứ), trạng thái ẩn chỉ phụ thuộc vào đầu vào hiện tại:<br><b>h<sub>1</sub> = tanh(W &times; x<sub>1</sub> + b<sub>h</sub>)</b>`;
                    } else {
                        // Flow from prev H
                        spawnDataFlow(nodes[tIndex-1].h.group.position, nodes[tIndex].h.group.position, 0x00ffff);
                        document.getElementById('step-desc').innerHTML = `<span style="color:#0ff; font-size:16px;">[LAN TRUYỀN XUÔI - BƯỚC ${tIndex+1}] - Bước 2: Trộn Quá khứ & Hiện tại</span><br><br>Nhận trạng thái quá khứ <b>h<sub>${tIndex}</sub></b> nhân với ma trận hồi quy <b>U</b>, cộng với thông tin hiện tại, nén qua hàm phi tuyến tanh:<br><b>h<sub>${tIndex+1}</sub> = tanh(U &times; h<sub>${tIndex}</sub> + W &times; x<sub>${tIndex+1}</sub> + b<sub>h</sub>)</b>`;
                    }
                    subPhase = 2;
                }
                else if (subPhase === 2) {
                    // H -> Y
                    nodes[tIndex].y.group.visible = true;
                    spawnDataFlow(nodes[tIndex].h.group.position, nodes[tIndex].y.group.position, 0xff9900);
                    document.getElementById('step-desc').innerHTML = `<span style="color:#f90; font-size:16px;">[LAN TRUYỀN XUÔI - BƯỚC ${tIndex+1}] - Bước 3: Đưa ra Dự đoán</span><br><br>Sử dụng trạng thái ẩn vừa cập nhật để xuất ra dự đoán:<br><b>y&#770;<sub>${tIndex+1}</sub> = V &times; h<sub>${tIndex+1}</sub> + b<sub>y</sub></b><br><br>Tính Loss cục bộ <b>L<sub>${tIndex+1}</sub></b>.`;
                    
                    subPhase = 0;
                    tIndex++;
                    if (tIndex >= timesteps) {
                        stateMode = "BACKWARD";
                        tIndex = timesteps - 1; // start backward from end
                    }
                }
            } 
            else if (stateMode === "BACKWARD") {
                if (subPhase === 0) {
                    // Y -> H Error gradient
                    spawnDataFlow(nodes[tIndex].y.group.position, nodes[tIndex].h.group.position, 0xff00ff);
                    document.getElementById('step-desc').innerHTML = `<span style="color:#f0f; font-size:16px;">[LAN TRUYỀN NGƯỢC (BPTT) - BƯỚC ${tIndex+1}]</span><br><br>Tính đạo hàm của Loss tại bước ${tIndex+1}: <b>&part;L<sub>${tIndex+1}</sub> / &part;y&#770;<sub>${tIndex+1}</sub></b>.<br>Đẩy lỗi ngược về ma trận V và trạng thái ẩn <b>h<sub>${tIndex+1}</sub></b>.`;
                    nodes[tIndex].h.outerMesh.material.color.setHex(0xff00ff);
                    subPhase = 1;
                }
                else if (subPhase === 1) {
                    // H -> X and H -> prev H
                    spawnDataFlow(nodes[tIndex].h.group.position, nodes[tIndex].x.group.position, 0xff00ff);
                    
                    let msg = `<span style="color:#f0f; font-size:16px;">[LAN TRUYỀN NGƯỢC (BPTT) - BƯỚC ${tIndex+1}]</span><br><br>Cập nhật ma trận đầu vào <b>W</b> dựa trên đạo hàm <b>&part;L / &part;W</b>.`;
                    
                    if (tIndex > 0) {
                        spawnDataFlow(nodes[tIndex].h.group.position, nodes[tIndex-1].h.group.position, 0xff00ff);
                        msg += `<br><br>Lỗi tiếp tục lan truyền ngược về quá khứ qua ma trận <b>U</b> (Gây ra Jacobian Chain):<br><b>&part;h<sub>${tIndex+1}</sub> / &part;h<sub>${tIndex}</sub> = diag(1 - h<sub>${tIndex+1}</sub>&sup2;) &times; U</b><br><i>(Nguồn gốc của Vanishing/Exploding Gradient)</i>`;
                    }
                    
                    document.getElementById('step-desc').innerHTML = msg;
                    
                    subPhase = 0;
                    tIndex--;
                    if (tIndex < 0) {
                        stateMode = "DONE";
                    }
                }
            } else {
                document.getElementById('step-desc').innerHTML = "<span style='color:#0f0; font-size:18px;'><b>Hoàn tất Mô phỏng!</b></span><br><br>Toàn bộ gradient đã được tính xong. Trọng số U, W, V sẽ được cập nhật bằng thuật toán Gradient Descent.<br><br>Nhấn [Reset] để chạy lại vòng lặp mới.";
            }
        }

        document.getElementById('btn-next').addEventListener('click', playNextStep);
        document.getElementById('btn-reset').addEventListener('click', () => {
            stateMode = "FORWARD";
            tIndex = 0;
            subPhase = 0;
            particles.forEach(p => scene.remove(p.mesh));
            particles = [];
            nodes.forEach(n => {
                n.x.group.visible = false;
                n.h.group.visible = false;
                n.y.group.visible = false;
                n.h.outerMesh.material.color.setHex(0x00ffff);
            });
            document.getElementById('step-desc').innerHTML = "Đã Reset.<br>Nhấn [NEXT STEP] để bắt đầu mô phỏng từng nhịp.";
        });

        // 7. RENDER LOOP
        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();
            
            controls.update();

            // Rotate nodes
            nodes.forEach(n => {
                if(n.x.group.visible) n.x.outerMesh.rotation.y += delta;
                if(n.h.group.visible) {
                    n.h.outerMesh.rotation.x += delta;
                    n.h.outerMesh.rotation.y += delta;
                }
                if(n.y.group.visible) n.y.outerMesh.rotation.z += delta;
            });

            // Update particles
            const now = Date.now();
            for(let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                if (!p.active) continue;
                
                const progress = (now - p.startTime) / p.duration;
                if (progress >= 1) {
                    p.mesh.position.copy(p.end);
                    p.active = false;
                    scene.remove(p.mesh);
                } else {
                    p.mesh.position.lerpVectors(p.start, p.end, progress);
                }
            }

            composer.render();
            labelRenderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            composer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
