html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>High-Tech RNN Simulation</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #050510; color: #fff; font-family: 'Consolas', monospace; user-select: none; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1;}
        #ui { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 10; background: rgba(10, 15, 30, 0.85); padding: 20px 40px; border-radius: 12px; border: 1px solid #0ff; box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); backdrop-filter: blur(5px); display: flex; flex-direction: column; align-items: center;}
        h1 { margin: 0 0 15px 0; font-size: 20px; color: #0ff; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #0ff;}
        .controls { display: flex; gap: 15px; }
        button { background: transparent; color: #0ff; border: 1px solid #0ff; padding: 10px 20px; cursor: pointer; border-radius: 4px; font-weight: bold; transition: 0.3s; font-family: 'Consolas', monospace; text-transform: uppercase; letter-spacing: 1px;}
        button:hover { background: rgba(0, 255, 255, 0.2); box-shadow: 0 0 15px rgba(0, 255, 255, 0.5); }
        button:active { background: #0ff; color: #000; }
        
        #info-panel { position: absolute; top: 30px; left: 30px; z-index: 10; background: rgba(10, 15, 30, 0.85); padding: 20px; border-radius: 8px; border: 1px solid #f0f; width: 300px; box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);}
        #info-panel h2 { margin: 0 0 10px 0; font-size: 16px; color: #f0f; }
        #step-desc { font-size: 14px; color: #aaa; line-height: 1.5; }

        /* CSS2D Node Labels */
        .node-label {
            color: #fff;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            padding: 4px 8px;
            background: rgba(0,0,0,0.7);
            border: 1px solid #fff;
            border-radius: 4px;
            pointer-events: none;
            white-space: nowrap;
            text-shadow: 0 0 5px #000;
        }
        .label-input { border-color: #0f0; color: #0f0; box-shadow: 0 0 10px rgba(0,255,0,0.5);}
        .label-hidden { border-color: #0ff; color: #0ff; box-shadow: 0 0 10px rgba(0,255,255,0.5);}
        .label-output { border-color: #f90; color: #f90; box-shadow: 0 0 10px rgba(255,153,0,0.5);}
        .math { font-style: italic; }
    </style>
</head>
<body>
    <div id="info-panel">
        <h2>Trạng Thái Hệ Thống</h2>
        <div id="step-desc">Đang khởi tạo mạng RNN...<br>Nhấn [NEXT STEP] để bắt đầu.</div>
    </div>

    <div id="ui">
        <h1>Bảng Điều Khiển Mạng Neural</h1>
        <div class="controls">
            <button id="btn-next">Next Step ❯</button>
            <button id="btn-reset">Reset ↺</button>
        </div>
    </div>

    <div id="canvas-container"></div>

    <!-- Three.js & Plugins -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <!-- Postprocessing -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>
    
    <!-- CSS2DRenderer -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/renderers/CSS2DRenderer.js"></script>

    <script>
        // 1. SETUP SCENE
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050510, 0.02);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 30);

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
        controls.maxPolarAngle = Math.PI / 2 - 0.1; // Khong cho nhin duoi dat

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
        
        // Materials (High-tech)
        const matX = new THREE.MeshBasicMaterial({color: 0x00ff00, wireframe: true}); // Input (Green)
        const matH = new THREE.MeshBasicMaterial({color: 0x00ffff, wireframe: true}); // Hidden (Cyan)
        const matY = new THREE.MeshBasicMaterial({color: 0xff9900, wireframe: true}); // Output (Orange)
        const matCore = new THREE.MeshBasicMaterial({color: 0xffffff}); // Core

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
            
            // HTML Label
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
            
            // X
            const xNode = createNode('x', new THREE.Vector3(xPos, -5, 0), `Input x<sub class="math">${i+1}</sub>`, 'label-input');
            // H
            const hNode = createNode('h', new THREE.Vector3(xPos, 0, 0), `Hidden h<sub class="math">${i+1}</sub>`, 'label-hidden');
            // Y
            const yNode = createNode('y', new THREE.Vector3(xPos, 5, 0), `Output y<sub class="math">${i+1}</sub>`, 'label-output');
            
            nodes.push({x: xNode, h: hNode, y: yNode});

            // Lines
            const matLine = new THREE.LineBasicMaterial({color: 0x444444});
            scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([xNode.group.position, hNode.group.position]), matLine));
            scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([hNode.group.position, yNode.group.position]), matLine));
            if(i > 0) {
                scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([nodes[i-1].h.group.position, hNode.group.position]), matLine));
            }
            
            // Turn off initial visibility to reveal step by step
            xNode.group.visible = false;
            hNode.group.visible = false;
            yNode.group.visible = false;
        }

        // 5. ANIMATION SYSTEM (PARTICLES)
        let particles = [];
        const particleGeo = new THREE.SphereGeometry(0.2, 8, 8);
        
        function spawnDataFlow(start, end, colorHex, textMsg, duration=800) {
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
            
            if(textMsg) document.getElementById('step-desc').innerHTML = textMsg;
        }

        // 6. STATE MACHINE FOR STEPS
        let currentStep = 0;
        /*
        Steps:
        1..4: Forward pass for t=1..4
        5..8: Backward pass (BPTT) for t=4..1
        */
        const maxSteps = timesteps * 2;

        function playNextStep() {
            if(currentStep >= maxSteps) return;
            currentStep++;
            
            if(currentStep <= timesteps) {
                // FORWARD PASS
                const t = currentStep - 1;
                nodes[t].x.group.visible = true;
                
                spawnDataFlow(nodes[t].x.group.position, nodes[t].h.group.position, 0x00ff00, 
                    `<span style="color:#0f0">Forward t=${t+1}:</span> Đọc Input x<sub>${t+1}</sub> qua trọng số <b>W</b>`, 500);
                
                setTimeout(() => {
                    nodes[t].h.group.visible = true;
                    // Flash core
                    nodes[t].h.coreMesh.scale.set(3,3,3);
                    setTimeout(() => nodes[t].h.coreMesh.scale.set(1,1,1), 200);
                    
                    let msg = `<span style="color:#0ff">Tính toán h<sub>${t+1}</sub> = tanh(W·x + b)</span>`;
                    if(t > 0) msg = `<span style="color:#0ff">Tính toán h<sub>${t+1}</sub> = tanh(W·x + U·h<sub>${t}</sub>)</span>`;
                    document.getElementById('step-desc').innerHTML = msg;

                    // If has prev H, send flow from prev H
                    if(t > 0) {
                        spawnDataFlow(nodes[t-1].h.group.position, nodes[t].h.group.position, 0x00ffff, null, 500);
                    }
                    
                    setTimeout(() => {
                        nodes[t].y.group.visible = true;
                        spawnDataFlow(nodes[t].h.group.position, nodes[t].y.group.position, 0xff9900, 
                            `<span style="color:#f90">Dự đoán Output:</span> y<sub>${t+1}</sub> = V·h<sub>${t+1}</sub>`, 500);
                    }, 500);

                }, 500);

            } else {
                // BACKWARD PASS (BPTT)
                const t = (maxSteps - currentStep); // 3, 2, 1, 0
                
                spawnDataFlow(nodes[t].y.group.position, nodes[t].h.group.position, 0xff00ff, 
                    `<span style="color:#f0f">BPTT t=${t+1}:</span> Tính Gradient Error từ Loss ngược về h<sub>${t+1}</sub>`, 600);
                
                setTimeout(() => {
                    nodes[t].h.outerMesh.material.color.setHex(0xff00ff);
                    
                    document.getElementById('step-desc').innerHTML = `<span style="color:#f0f">Cập nhật Gradient:</span> dL / dU, dL / dW`;
                    
                    spawnDataFlow(nodes[t].h.group.position, nodes[t].x.group.position, 0xff00ff, null, 600);
                    
                    if(t > 0) {
                        spawnDataFlow(nodes[t].h.group.position, nodes[t-1].h.group.position, 0xff00ff, 
                            `<span style="color:#f0f">Trôi Gradient về quá khứ:</span> h<sub>${t+1}</sub> $\\to$ h<sub>${t}</sub>`, 600);
                    }
                }, 600);
            }
        }

        document.getElementById('btn-next').addEventListener('click', playNextStep);
        document.getElementById('btn-reset').addEventListener('click', () => {
            currentStep = 0;
            particles.forEach(p => scene.remove(p.mesh));
            particles = [];
            nodes.forEach(n => {
                n.x.group.visible = false;
                n.h.group.visible = false;
                n.y.group.visible = false;
                n.h.outerMesh.material.color.setHex(0x00ffff); // reset color
            });
            document.getElementById('step-desc').innerHTML = "Đã Reset.<br>Nhấn [NEXT STEP] để bắt đầu.";
        });

        // 7. RENDER LOOP
        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();
            
            controls.update();

            // Rotate nodes for high-tech feel
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
</body>
</html>
"""
with open("rnn_hightech_sim.html", "w", encoding="utf-8") as f:
    f.write(html_content)
