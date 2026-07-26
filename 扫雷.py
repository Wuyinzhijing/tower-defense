import tkinter as tk
from tkinter import messagebox
import random
import sys

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.master.title("扫雷游戏")
        self.master.resizable(False, False)
        
        # 游戏配置
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.uncovered_cells = 0  # 已揭开的格子数
        self.game_over = False    # 游戏是否结束
        
        # 颜色配置（不同数字对应不同颜色）
        self.number_colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray"
        }
        
        # 初始化游戏面板
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        """创建界面组件"""
        # 顶部状态栏
        self.status_var = tk.StringVar(value=f"剩余地雷: {self.total_mines} | 游戏中")
        self.status_bar = tk.Label(
            self.master, textvariable=self.status_var, 
            font=("Arial", 12), padx=10, pady=5
        )
        self.status_bar.grid(row=0, column=0, columnspan=self.cols, sticky="we")
        
        # 游戏网格按钮
        self.buttons = []
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                btn = tk.Button(
                    self.master, width=2, height=1, font=("Arial", 10, "bold"),
                    command=lambda r=i, c=j: self.on_left_click(r, c),
                )
                # 绑定右键标记地雷
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.on_right_click(r, c))
                btn.grid(row=i+1, column=j, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        # 重置按钮
        self.reset_btn = tk.Button(
            self.master, text="重新开始", font=("Arial", 12),
            command=self.reset_game
        )
        self.reset_btn.grid(row=self.rows+1, column=0, columnspan=self.cols, pady=5)

    def reset_game(self):
        """重置游戏状态"""
        self.game_over = False
        self.uncovered_cells = 0
        self.flag_count = 0  # 标记的旗子数
        
        # 重置按钮状态
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(
                    text="", state="normal", bg="SystemButtonFace",
                    relief="raised"
                )
        
        # 生成地雷和数字面板
        self.generate_mines()
        self.calculate_numbers()
        
        # 更新状态栏
        self.status_var.set(f"剩余地雷: {self.total_mines} | 游戏中")

    def generate_mines(self):
        """随机生成地雷位置"""
        self.mine_positions = set()
        # 确保地雷数量不超过格子总数
        max_mines = self.rows * self.cols - 1
        self.total_mines = min(self.total_mines, max_mines)
        
        # 随机选择地雷位置
        while len(self.mine_positions) < self.total_mines:
            r = random.randint(0, self.rows-1)
            c = random.randint(0, self.cols-1)
            self.mine_positions.add((r, c))

    def calculate_numbers(self):
        """计算每个格子周围的地雷数量"""
        self.number_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions:
                    # 遍历8个相邻格子
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if (nr, nc) in self.mine_positions:
                                    count += 1
                    self.number_board[r][c] = count

    def on_left_click(self, r, c):
        """左键点击：揭开格子"""
        if self.game_over or self.buttons[r][c]['state'] == 'disabled':
            return
        
        btn = self.buttons[r][c]
        
        # 点中地雷，游戏结束
        if (r, c) in self.mine_positions:
            btn.config(text="💣", bg="red")
            self.game_over = True
            self.reveal_all_mines()
            messagebox.showinfo("游戏结束", "你踩到地雷了！游戏失败")
            self.status_var.set(f"剩余地雷: {self.total_mines - self.flag_count} | 游戏失败")
            return
        
        # 揭开空白格子（数字为0）
        if self.number_board[r][c] == 0:
            self.reveal_empty_cells(r, c)
        else:
            # 揭开有数字的格子
            btn.config(
                text=str(self.number_board[r][c]), 
                fg=self.number_colors[self.number_board[r][c]],
                state="disabled", relief="sunken"
            )
            self.uncovered_cells += 1
        
        # 检查是否获胜
        self.check_win()

    def on_right_click(self, r, c):
        """右键点击：标记/取消标记地雷"""
        if self.game_over or self.buttons[r][c]['state'] == 'disabled':
            return
        
        btn = self.buttons[r][c]
        
        # 切换标记状态
        if btn['text'] == "🚩":
            btn.config(text="", bg="SystemButtonFace")
            self.flag_count -= 1
        else:
            btn.config(text="🚩", bg="yellow")
            self.flag_count += 1
        
        # 更新状态栏
        remaining = self.total_mines - self.flag_count
        self.status_var.set(f"剩余地雷: {remaining} | 游戏中")

    def reveal_empty_cells(self, r, c):
        """递归揭开空白格子（数字为0的区域）"""
        if (r < 0 or r >= self.rows or c < 0 or c >= self.cols or
            self.buttons[r][c]['state'] == 'disabled'):
            return
        
        btn = self.buttons[r][c]
        btn.config(state="disabled", relief="sunken")
        self.uncovered_cells += 1
        
        # 如果是数字格子，显示数字
        if self.number_board[r][c] > 0:
            btn.config(
                text=str(self.number_board[r][c]),
                fg=self.number_colors[self.number_board[r][c]]
            )
            return
        
        # 递归揭开周围8个格子
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                self.reveal_empty_cells(r + dr, c + dc)

    def reveal_all_mines(self):
        """游戏失败时，显示所有地雷"""
        for (r, c) in self.mine_positions:
            if self.buttons[r][c]['text'] != "🚩":
                self.buttons[r][c].config(text="💣", bg="red")
        
        # 禁用所有按钮
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(state="disabled")

    def check_win(self):
        """检查是否获胜（揭开所有非地雷格子）"""
        total_safe_cells = self.rows * self.cols - self.total_mines
        if self.uncovered_cells == total_safe_cells:
            self.game_over = True
            messagebox.showinfo("恭喜", "你成功扫完所有地雷！游戏胜利")
            self.status_var.set(f"剩余地雷: {self.total_mines - self.flag_count} | 游戏胜利")
            
            # 标记所有未标记的地雷
            for (r, c) in self.mine_positions:
                if self.buttons[r][c]['text'] != "🚩":
                    self.buttons[r][c].config(text="🚩", bg="green")
            
            # 禁用所有按钮
            for i in range(self.rows):
                for j in range(self.cols):
                    self.buttons[i][j].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    # 可调整参数：行数、列数、地雷数
    game = Minesweeper(root, rows=10, cols=10, mines=10)
    root.mainloop()