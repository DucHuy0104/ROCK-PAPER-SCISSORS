"""
Các hàm helper cho game Rock-Paper-Scissors
"""

import socket
import re
import json
from typing import Tuple, Optional

def validate_connection(host: str, port: int) -> bool:
    """
    Kiểm tra thông tin kết nối có hợp lệ không
    
    Args:
        host (str): Địa chỉ host
        port (int): Cổng kết nối
        
    Returns:
        bool: True nếu hợp lệ, False nếu không
    """
    # Kiểm tra host
    if not host or not isinstance(host, str):
        return False
    
    # Kiểm tra port
    if not isinstance(port, int) or port < 1 or port > 65535:
        return False
    
    # Kiểm tra format host (IPv4 hoặc localhost)
    if host not in ['localhost', '127.0.0.1']:
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(ip_pattern, host):
            return False
    
    return True

def test_connection(host: str, port: int, timeout: int = 5) -> bool:
    """
    Kiểm tra kết nối đến server có thành công không
    
    Args:
        host (str): Địa chỉ host
        port (int): Cổng kết nối
        timeout (int): Thời gian timeout (giây)
        
    Returns:
        bool: True nếu kết nối thành công, False nếu không
    """
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(timeout)
        result = test_socket.connect_ex((host, port))
        test_socket.close()
        return result == 0
    except Exception:
        return False

def format_message(message_type: str, **kwargs) -> str:
    """
    Tạo message JSON chuẩn
    
    Args:
        message_type (str): Loại message
        **kwargs: Các tham số khác
        
    Returns:
        str: Message JSON
    """
    message = {"type": message_type}
    message.update(kwargs)
    return json.dumps(message)

def parse_message(message: str) -> Optional[dict]:
    """
    Parse message JSON
    
    Args:
        message (str): Message JSON
        
    Returns:
        dict: Dictionary parsed hoặc None nếu lỗi
    """
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return None

def get_local_ip() -> str:
    """
    Lấy địa chỉ IP local
    
    Returns:
        str: Địa chỉ IP local
    """
    try:
        # Tạo socket tạm để lấy IP
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def find_available_port(start_port: int = 12345, max_attempts: int = 100) -> Optional[int]:
    """
    Tìm cổng khả dụng
    
    Args:
        start_port (int): Cổng bắt đầu tìm
        max_attempts (int): Số lần thử tối đa
        
    Returns:
        int: Cổng khả dụng hoặc None nếu không tìm được
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('localhost', port))
            test_socket.close()
            return port
        except OSError:
            continue
    return None

def log_message(message: str, level: str = "INFO") -> None:
    """
    Ghi log message
    
    Args:
        message (str): Nội dung log
        level (str): Mức độ log
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def validate_choice(choice: str) -> bool:
    """
    Kiểm tra lựa chọn game có hợp lệ không
    
    Args:
        choice (str): Lựa chọn của người chơi
        
    Returns:
        bool: True nếu hợp lệ, False nếu không
    """
    valid_choices = ['rock', 'paper', 'scissors']
    return choice.lower() in valid_choices

def normalize_choice(choice: str) -> str:
    """
    Chuẩn hóa lựa chọn về dạng lowercase
    
    Args:
        choice (str): Lựa chọn gốc
        
    Returns:
        str: Lựa chọn đã chuẩn hóa
    """
    return choice.lower().strip()

def get_choice_display_name(choice: str) -> str:
    """
    Lấy tên hiển thị của lựa chọn
    
    Args:
        choice (str): Lựa chọn
        
    Returns:
        str: Tên hiển thị
    """
    display_names = {
        'rock': 'Đá 🪨',
        'paper': 'Giấy 📄',
        'scissors': 'Kéo ✂️'
    }
    return display_names.get(choice.lower(), 'Không xác định')

def calculate_win_rate(wins: int, total_games: int) -> float:
    """
    Tính tỷ lệ thắng
    
    Args:
        wins (int): Số lần thắng
        total_games (int): Tổng số game
        
    Returns:
        float: Tỷ lệ thắng (0.0 - 1.0)
    """
    if total_games == 0:
        return 0.0
    return wins / total_games
