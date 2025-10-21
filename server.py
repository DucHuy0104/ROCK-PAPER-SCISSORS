"""
Server cho game Rock-Paper-Scissors
Quản lý kết nối và logic game
"""

import socket
import threading
import json
from game_logic import GameLogic

class RockPaperScissorsServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.game_logic = GameLogic()
        self.running = False
        
    def start_server(self):
        """Khởi động server"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            print(f"Server đang chạy trên {self.host}:{self.port}")
            print("Chờ kết nối từ client...")
            
            while self.running:
                client_socket, address = self.server_socket.accept()
                print(f"Client kết nối từ {address}")
                
                # Tạo thread riêng cho mỗi client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
                
        except Exception as e:
            print(f"Lỗi server: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, client_socket, address):
        """Xử lý kết nối từ client"""
        try:
            self.clients.append(client_socket)
            
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                message = json.loads(data)
                response = self.process_message(message)
                
                # Gửi phản hồi về client
                client_socket.send(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            print(f"Lỗi xử lý client {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"Client {address} đã ngắt kết nối")
    
    def process_message(self, message):
        """Xử lý tin nhắn từ client"""
        message_type = message.get('type')
        
        if message_type == 'play':
            choice = message.get('choice')
            result = self.game_logic.play_round(choice)
            return {
                'type': 'result',
                'result': result,
                'server_choice': self.game_logic.server_choice
            }
        elif message_type == 'ping':
            return {'type': 'pong'}
        else:
            return {'type': 'error', 'message': 'Unknown message type'}
    
    def stop_server(self):
        """Dừng server"""
        self.running = False
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server đã dừng")

if __name__ == "__main__":
    server = RockPaperScissorsServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nĐang dừng server...")
        server.stop_server()
