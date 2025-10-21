"""
Logic game Rock-Paper-Scissors
Xử lý so sánh kết quả và quyết định thắng thua
"""

import random

class GameLogic:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.server_choice = None
        
    def get_server_choice(self):
        """Lấy lựa chọn ngẫu nhiên của server"""
        self.server_choice = random.choice(self.choices)
        return self.server_choice
    
    def compare_choices(self, player_choice, server_choice):
        """
        So sánh lựa chọn của player và server
        Trả về: 'win', 'lose', hoặc 'tie'
        """
        if player_choice == server_choice:
            return 'tie'
        
        # Định nghĩa luật thắng thua
        win_conditions = {
            'rock': 'scissors',      # Rock thắng Scissors
            'paper': 'rock',         # Paper thắng Rock  
            'scissors': 'paper'      # Scissors thắng Paper
        }
        
        if win_conditions[player_choice] == server_choice:
            return 'win'
        else:
            return 'lose'
    
    def play_round(self, player_choice):
        """
        Chơi một vòng game
        Args:
            player_choice (str): Lựa chọn của người chơi
        Returns:
            str: Kết quả ('win', 'lose', 'tie')
        """
        # Validate lựa chọn
        if player_choice not in self.choices:
            raise ValueError(f"Lựa chọn không hợp lệ: {player_choice}")
        
        # Lấy lựa chọn của server
        server_choice = self.get_server_choice()
        
        # So sánh và trả về kết quả
        return self.compare_choices(player_choice, server_choice)
    
    def get_choice_emoji(self, choice):
        """Lấy emoji tương ứng với lựa chọn"""
        emoji_map = {
            'rock': '🪨',
            'paper': '📄', 
            'scissors': '✂️'
        }
        return emoji_map.get(choice, '❓')
    
    def get_choice_name(self, choice):
        """Lấy tên tiếng Việt của lựa chọn"""
        name_map = {
            'rock': 'Đá',
            'paper': 'Giấy',
            'scissors': 'Kéo'
        }
        return name_map.get(choice, 'Không xác định')
    
    def is_valid_choice(self, choice):
        """Kiểm tra lựa chọn có hợp lệ không"""
        return choice in self.choices
    
    def get_game_rules(self):
        """Trả về luật chơi"""
        return {
            'rock': 'Thắng Scissors, Thua Paper',
            'paper': 'Thắng Rock, Thua Scissors', 
            'scissors': 'Thắng Paper, Thua Rock'
        }
