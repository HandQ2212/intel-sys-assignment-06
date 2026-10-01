import re

with open('rnn_slides.tex', 'r') as f:
    content = f.read()

# Fix unescaped ampersands in titles/text
replacements = {
    r'Hiện tượng Nổ Gradient & Gradient Clipping': r'Hiện tượng Nổ Gradient \& Gradient Clipping',
    r'Chuỗi giá vàng & bạc hàng ngày (Gold & Silver': r'Chuỗi giá vàng \& bạc hàng ngày (Gold \& Silver',
    r'Chuỗi biến động giá & khối lượng': r'Chuỗi biến động giá \& khối lượng',
    r'Kết quả Thực nghiệm & Hiện tượng Nghịch lý': r'Kết quả Thực nghiệm \& Hiện tượng Nghịch lý',
    r'Bài học & Giải pháp khắc phục': r'Bài học \& Giải pháp khắc phục',
    r'Tổng kết & Bức tranh Toàn cảnh': r'Tổng kết \& Bức tranh Toàn cảnh',
    r'$U > 1\(:\)\Vert U^{T-k} \Vert$': r'$U > 1$: $\Vert U^{T-k} \Vert$'
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Fix table row endings: space backslash newline to space backslash backslash newline
content = re.sub(r' \\\n', r' \\\\\n', content)

with open('rnn_slides.tex', 'w') as f:
    f.write(content)
print("Fixed issues")
