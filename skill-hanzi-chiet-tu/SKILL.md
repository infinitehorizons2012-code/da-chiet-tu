---
name: hanzi-chiet-tu-animator
description: Kỹ năng tích hợp HanziWriter vào React để vẽ chữ Hán chiết tự, đổ nhiều màu mực khác nhau cho từng bộ thủ và hỗ trợ animation (mô phỏng quá trình viết chữ).
---

# Kỹ năng: Hanzi Chiết Tự Animator (React)

Kỹ năng này cung cấp giải pháp hoàn chỉnh để giải quyết bài toán khó nhất khi dùng thư viện `hanzi-writer`: **Tô màu khác nhau cho từng nét/từng bộ thủ của một chữ Hán và giữ nguyên màu đó trong lúc chạy animation (viết chữ).**

## 1. Vấn đề của HanziWriter
Mặc định `HanziWriter` chỉ cho phép đổi 1 màu duy nhất cho toàn bộ nét vẽ (thông qua `strokeColor`). Nếu dùng Javascript can thiệp vào DOM (`svg path`) bằng `style.fill`, màu sẽ bị mất/ghi đè khi gọi hàm `animateCharacter()` vì thư viện sẽ vẽ lại các nét bằng thẻ `<clipPath>` lồng nhau và ép màu inline.

## 2. Giải pháp: CSS Injection thần thánh
Thay vì dùng JS can thiệp DOM, ta sinh ra một đoạn mã CSS nội tuyến (inline `<style>`) sử dụng thuộc tính `:nth-child` để tát thẳng màu vào các nét vẽ. Bộ chọn CSS này được thiết kế để "bắt" dính nét vẽ bất kể nó nằm ở trạng thái tĩnh hay đang chạy animation lồng sâu trong `<g>` hay `<clipPath>`.

Bộ chọn CSS chuẩn xác 100%:
```css
.custom-hanzi-colors svg path:nth-child({idx + 1}) {
  fill: {color} !important;
  stroke: {color} !important;
}
```

## 3. Cấu trúc Dữ liệu mẫu (Database)
Để thư viện biết tô màu nét nào, dữ liệu chữ Hán phải liệt kê chính xác mảng `strokes` (dựa trên số thứ tự nét, bắt đầu từ 0).

```javascript
export const mockDatabase = {
  '茶': {
    char: '茶',
    components: [
      { type: 'Radical', char: '艹', color: '#2563eb', strokes: [0, 1, 2] },
      { type: 'Component', char: '人', color: '#e11d48', strokes: [3, 4] },
      { type: 'Component', char: '木', color: '#059669', strokes: [5, 6, 7, 8] }
    ]
  }
}
```

## 4. Component React Hoàn Chỉnh (`HanziDisplay.jsx`)
Dưới đây là component React chuẩn mực, có tích hợp nút "Xem cách viết":

```jsx
import { useEffect, useRef, useMemo } from 'react';
import HanziWriter from 'hanzi-writer';

export default function HanziDisplay({ char, components }) {
  const containerRef = useRef(null);
  const writerRef = useRef(null);

  // Sinh CSS ghi đè màu sắc cho từng nét vẽ
  const customCss = useMemo(() => {
    if (!components) return '';
    let css = '';
    components.forEach(comp => {
      if (comp.strokes) {
        comp.strokes.forEach(idx => {
          // idx + 1 vì nth-child đếm từ 1
          css += `
            .custom-hanzi-colors svg path:nth-child(${idx + 1}) {
              fill: ${comp.color} !important;
              stroke: ${comp.color} !important;
            }
          `;
        });
      }
    });
    return css;
  }, [components]);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Reset DOM
    containerRef.current.innerHTML = '';
    
    // Khởi tạo HanziWriter
    writerRef.current = HanziWriter.create(containerRef.current, char, {
      width: 150,
      height: 150,
      padding: 5,
      strokeColor: '#cbd5e1', // Màu xám nhạt mặc định nếu chưa định nghĩa màu
      radicalColor: null, 
      showOutline: false,
      strokeAnimationSpeed: 1.5,
      delayBetweenStrokes: 150
    });
  }, [char]);

  const handleAnimate = () => {
    if (writerRef.current) {
      writerRef.current.animateCharacter();
    }
  };

  return (
    <div className="char-display-container">
      <div className="custom-hanzi-colors" onClick={handleAnimate} style={{ cursor: 'pointer' }}>
        <style>{customCss}</style>
        <div ref={containerRef} className="char-writer" />
      </div>
      <button onClick={handleAnimate}>✍️ Xem cách viết</button>
    </div>
  );
}
```

## 5. Quy trình làm việc khi Agent được yêu cầu tạo web chiết tự
1. Khởi tạo dự án React/Vite.
2. Cài đặt `npm install hanzi-writer`.
3. Nhúng component `HanziDisplay` ở trên.
4. Xây dựng Database chữ Hán theo cấu trúc `strokes` index. Đảm bảo agent đếm số lượng nét chính xác để phân phối mảng `strokes` cho đúng với từng bộ thủ.
5. Đảm bảo thẻ bọc `div` có class `custom-hanzi-colors` nằm CHÍNH XÁC ở cấp chứa `<style>` và thẻ con chứa svg.
