# ROCK-PAPER-SCISSORS

## Mô tả dự án
Game Rock-Paper-Scissors (Kéo-Búa-Bao) sử dụng Python với giao diện GUI Tkinter và kết nối TCP Socket. Người chơi có thể kết nối đến server và chơi game với máy tính.

## Công nghệ sử dụng
- **Language**: Python 3.x
- **GUI**: Tkinter
- **Network**: Socket TCP
- **Architecture**: Client-Server

## Cấu trúc dự án
```
RockPaperScissors/
│
├── server.py          # Server quản lý kết nối và logic game
├── client.py          # Client GUI + logic gửi/nhận
├── game_logic.py      # Xử lý logic game (so sánh kết quả)
├── utils.py           # Các hàm helper
└── README.md          # Hướng dẫn sử dụng
```

## Cách chạy dự án

### 1. Chạy Server
```bash
python server.py
```
Server sẽ chạy trên `localhost:12345` (mặc định)

### 2. Chạy Client
```bash
python client.py
```
- Nhập thông tin kết nối (Host: localhost, Port: 12345)
- Nhấn "Kết nối" để kết nối đến server
- Chọn Rock/Paper/Scissors để chơi game

## Tính năng

### Server (server.py)
- Quản lý kết nối TCP
- Xử lý logic game
- Hỗ trợ nhiều client đồng thời
- Gửi phản hồi kết quả

### Client (client.py)
- Giao diện GUI thân thiện với Tkinter
- Kết nối đến server
- Hiển thị kết quả game
- Thống kê thắng/thua/hòa

### Game Logic (game_logic.py)
- So sánh lựa chọn Rock/Paper/Scissors
- Xác định kết quả thắng/thua/hòa
- Hỗ trợ validation lựa chọn

### Utils (utils.py)
- Validation kết nối
- Format message JSON
- Helper functions

## Luật chơi
- **Rock (Đá) 🪨**: Thắng Scissors, Thua Paper
- **Paper (Giấy) 📄**: Thắng Rock, Thua Scissors  
- **Scissors (Kéo) ✂️**: Thắng Paper, Thua Rock

## Yêu cầu hệ thống
- Python 3.6+
- Tkinter (thường có sẵn với Python)
- Không cần thư viện bổ sung

## Hướng dẫn sử dụng
1. Khởi động server trước
2. Mở client và kết nối
3. Chọn Rock/Paper/Scissors
4. Xem kết quả và thống kê
