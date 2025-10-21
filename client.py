"""
Client GUI cho game Rock-Paper-Scissors
Sử dụng Tkinter cho giao diện người dùng
"""

import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json
import threading
from utils import validate_connection

class RockPaperScissorsClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors - Client")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Kết nối
        self.socket = None
        self.connected = False
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame kết nối
        connection_frame = ttk.LabelFrame(self.root, text="Kết nối", padding=10)
        connection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Host và Port
        ttk.Label(connection_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.host_entry = ttk.Entry(connection_frame, width=15)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=0, column=3, padx=5)
        
        # Nút kết nối
        self.connect_btn = ttk.Button(connection_frame, text="Kết nối", command=self.connect_to_server)
        self.connect_btn.grid(row=0, column=4, padx=10)
        
        # Frame game
        game_frame = ttk.LabelFrame(self.root, text="Chơi game", padding=10)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Hướng dẫn
        ttk.Label(game_frame, text="Chọn một trong ba lựa chọn:", font=("Arial", 12)).pack(pady=10)
        
        # Nút lựa chọn
        button_frame = ttk.Frame(game_frame)
        button_frame.pack(pady=20)
        
        self.rock_btn = ttk.Button(button_frame, text="🪨 Rock", command=lambda: self.play("rock"))
        self.rock_btn.pack(side=tk.LEFT, padx=10)
        
        self.paper_btn = ttk.Button(button_frame, text="📄 Paper", command=lambda: self.play("paper"))
        self.paper_btn.pack(side=tk.LEFT, padx=10)
        
        self.scissors_btn = ttk.Button(button_frame, text="✂️ Scissors", command=lambda: self.play("scissors"))
        self.scissors_btn.pack(side=tk.LEFT, padx=10)
        
        # Kết quả
        self.result_label = ttk.Label(game_frame, text="Kết quả sẽ hiển thị ở đây", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # Thống kê
        stats_frame = ttk.LabelFrame(self.root, text="Thống kê", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Thắng: 0 | Thua: 0 | Hòa: 0")
        self.stats_label.pack()
        
        # Khởi tạo thống kê
        self.wins = 0
        self.losses = 0
        self.ties = 0
        
        # Vô hiệu hóa nút game ban đầu
        self.set_game_buttons_state(tk.DISABLED)
        
    def connect_to_server(self):
        """Kết nối đến server"""
        try:
            host = self.host_entry.get()
            port = int(self.port_entry.get())
            
            if not validate_connection(host, port):
                messagebox.showerror("Lỗi", "Thông tin kết nối không hợp lệ!")
                return
                
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            self.connect_btn.config(text="Đã kết nối", state=tk.DISABLED)
            self.set_game_buttons_state(tk.NORMAL)
            
            messagebox.showinfo("Thành công", f"Đã kết nối đến {host}:{port}")
            
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối: {e}")
            self.connected = False
    
    def play(self, choice):
        """Gửi lựa chọn đến server"""
        if not self.connected:
            messagebox.showerror("Lỗi", "Chưa kết nối đến server!")
            return
            
        try:
            # Gửi lựa chọn
            message = json.dumps({"type": "play", "choice": choice})
            self.socket.send(message.encode('utf-8'))
            
            # Nhận phản hồi
            response = self.socket.recv(1024).decode('utf-8')
            result_data = json.loads(response)
            
            self.handle_result(result_data, choice)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chơi game: {e}")
    
    def handle_result(self, result_data, player_choice):
        """Xử lý kết quả từ server"""
        result = result_data.get('result')
        server_choice = result_data.get('server_choice')
        
        # Cập nhật thống kê
        if result == 'win':
            self.wins += 1
            result_text = "🎉 Bạn thắng!"
        elif result == 'lose':
            self.losses += 1
            result_text = "😞 Bạn thua!"
        else:
            self.ties += 1
            result_text = "🤝 Hòa!"
        
        # Hiển thị kết quả
        display_text = f"{result_text}\n\nBạn chọn: {player_choice.title()}\nServer chọn: {server_choice.title()}"
        self.result_label.config(text=display_text)
        
        # Cập nhật thống kê
        self.stats_label.config(text=f"Thắng: {self.wins} | Thua: {self.losses} | Hòa: {self.ties}")
    
    def set_game_buttons_state(self, state):
        """Thiết lập trạng thái các nút game"""
        self.rock_btn.config(state=state)
        self.paper_btn.config(state=state)
        self.scissors_btn.config(state=state)
    
    def run(self):
        """Chạy ứng dụng"""
        try:
            self.root.mainloop()
        finally:
            if self.socket:
                self.socket.close()

if __name__ == "__main__":
    client = RockPaperScissorsClient()
    client.run()
