import re

with open('rnn_hightech_sim.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_func = r"""function playNextStep() {
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
        }"""

html = re.sub(r"function playNextStep\(\) \{[\s\S]*?\}\s*document\.getElementById\('btn-next'\)", new_func + "\n\n        document.getElementById('btn-next')", html)

with open('rnn_hightech_sim.html', 'w', encoding='utf-8') as f:
    f.write(html)
