# Họ tên: Bùi Anh Khôi
# MSSV: 24110258
# Link Github: https://github.com/buianhkhoi020120-cloud/TicTacToe

import tkinter as tk
from tkinter import messagebox
from algorithms import get_best_move, check_win, check_draw

# Cấu hình màu sắc
BG_COLOR = "#0F172A"          # Slate 900 (Nền chính tối sâu)
CARD_BG = "#1E293B"           # Slate 800 (Khung phụ trợ chứa các cài đặt)
BORDER_COLOR = "#334155"      # Slate 700 (Đường viền tinh tế)
TEXT_COLOR = "#F8FAFC"        # Slate 50 (Chữ sáng chính)
TEXT_MUTED = "#94A3B8"        # Slate 400 (Chữ phụ màu nhạt)
COLOR_X = "#00E5FF"           # Neon Teal nổi bật cho X
COLOR_O = "#FF5722"           # Neon Coral tương phản tốt cho O
BTN_BG = "#334155"            # Nền nút bấm khi không chọn
BTN_HOVER = "#475569"         # Nền nút khi di chuột qua
HIGHLIGHT_WIN = "#10B981"     # Màu chữ cho dòng thắng cuộc
HIGHLIGHT_WIN_BG = "#064E3B"  # Nền phát sáng cho dòng thắng cuộc
CELL_BG = "#1E293B"           # Nền các ô cờ Tic Tac Toe

FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_BOARD = ("Segoe UI", 36, "bold") 

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI - Premium Edition")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        # Trạng thái trò chơi
        self.board = [' '] * 9
        self.current_player = 'X'
        self.ai_player = 'O'
        self.human_player = 'X'
        self.game_active = False
        # Cấu hình grid chính cho root để căn giữa toàn bộ content
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # Tạo pixel_img rỗng (1x1) để ép kích thước nút theo Pixel (giúp ô cờ vuông tuyệt đối)
        self.pixel_img = tk.PhotoImage(width=1, height=1)
        self.setup_ui()
        # Tính toán kích thước cửa sổ động và căn giữa màn hình để tránh lỗi tràn/cắt giao diện
        self.root.update_idletasks()
        width = max(460, self.root.winfo_reqwidth())
        height = max(580, self.root.winfo_reqheight())
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Container chính để gom nhóm và căn giữa
        self.main_container = tk.Frame(self.root, bg=BG_COLOR)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        title_label = tk.Label(self.main_container, text="TIC TAC TOE AI", font=("Segoe UI", 22, "bold"), fg=COLOR_X, bg=BG_COLOR)
        title_label.grid(row=0, column=0, pady=(0, 15), sticky="n")
        # --- Khung cài đặt (Card-like styling) ---
        settings_frame = tk.Frame(self.main_container, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1, bd=0)
        settings_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=3)
        # Chọn thuật toán 
        tk.Label(settings_frame, text="Thuật toán:", bg=CARD_BG, fg=TEXT_MUTED, font=FONT_BOLD).grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.algo_var = tk.StringVar(value="Alpha-Beta")
        algo_frame = tk.Frame(settings_frame, bg=CARD_BG)
        algo_frame.grid(row=0, column=1, padx=12, pady=10, sticky="w")
        self.btn_minimax = tk.Radiobutton(algo_frame, text="Minimax", variable=self.algo_var, value="Minimax",
                                          indicatoron=0, width=9, bg=BTN_BG, fg=TEXT_COLOR,
                                          activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                          font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_minimax.pack(side="left", padx=(0, 6))
        self.btn_alphabeta = tk.Radiobutton(algo_frame, text="Alpha-Beta", variable=self.algo_var, value="Alpha-Beta",
                                            indicatoron=0, width=10, bg=BTN_BG, fg=TEXT_COLOR,
                                            activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                            font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_alphabeta.pack(side="left", padx=(0, 6))
        self.btn_expectimax = tk.Radiobutton(algo_frame, text="Expectimax", variable=self.algo_var, value="Expectimax",
                                             indicatoron=0, width=10, bg=BTN_BG, fg=TEXT_COLOR,
                                             activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                             font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_expectimax.pack(side="left")

        # Chọn quân 
        tk.Label(settings_frame, text="Chọn quân:", bg=CARD_BG, fg=TEXT_MUTED, font=FONT_BOLD).grid(row=1, column=0, padx=12, pady=10, sticky="w")
        self.player_symbol_var = tk.StringVar(value="X")
        symbol_frame = tk.Frame(settings_frame, bg=CARD_BG)
        symbol_frame.grid(row=1, column=1, padx=12, pady=10, sticky="w")
        self.btn_x = tk.Radiobutton(symbol_frame, text="X", variable=self.player_symbol_var, value="X",
                                    indicatoron=0, width=6, bg=BTN_BG, fg=TEXT_COLOR,
                                    activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                    font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_x.pack(side="left", padx=(0, 6))
        self.btn_o = tk.Radiobutton(symbol_frame, text="O", variable=self.player_symbol_var, value="O",
                                    indicatoron=0, width=6, bg=BTN_BG, fg=TEXT_COLOR,
                                    activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                    font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_o.pack(side="left")
        # Chọn người đi trước (Người / AI)
        tk.Label(settings_frame, text="Đi trước:", bg=CARD_BG, fg=TEXT_MUTED, font=FONT_BOLD).grid(row=2, column=0, padx=12, pady=10, sticky="w")
        self.first_player_var = tk.StringVar(value="Người")
        first_frame = tk.Frame(settings_frame, bg=CARD_BG)
        first_frame.grid(row=2, column=1, padx=12, pady=10, sticky="w")
        self.btn_first_human = tk.Radiobutton(first_frame, text="Người", variable=self.first_player_var, value="Người",
                                              indicatoron=0, width=8, bg=BTN_BG, fg=TEXT_COLOR,
                                              activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                              font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_first_human.pack(side="left", padx=(0, 6))
        self.btn_first_ai = tk.Radiobutton(first_frame, text="AI", variable=self.first_player_var, value="AI",
                                           indicatoron=0, width=8, bg=BTN_BG, fg=TEXT_COLOR,
                                           activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                                           font=FONT_MAIN, relief="flat", bd=0, command=self.update_settings_ui)
        self.btn_first_ai.pack(side="left")
        # Khởi tạo trạng thái ban đầu của các nút settings
        self.update_settings_ui()
        # --- Khung chứa Nút Bắt đầu & Nút Chơi lại cạnh nhau ---
        btn_action_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        btn_action_frame.grid(row=2, column=0, pady=(5, 15), sticky="ew")
        btn_action_frame.columnconfigure(0, weight=1)
        btn_action_frame.columnconfigure(1, weight=1)
        self.btn_start = tk.Button(btn_action_frame, text="BẮT ĐẦU", command=self.start_game,
                                   bg=COLOR_X, fg=BG_COLOR, font=("Segoe UI", 11, "bold"),
                                   relief="flat", bd=0, cursor="hand2", pady=10)
        self.btn_start.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.btn_start.bind("<Enter>", lambda e: self.btn_start.config(bg="#00E5FF"))
        self.btn_start.bind("<Leave>", lambda e: self.btn_start.config(bg=COLOR_X))
        self.btn_reset = tk.Button(btn_action_frame, text="CHƠI LẠI", command=self.start_game,
                                   bg=BTN_BG, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"),
                                   relief="flat", bd=0, cursor="hand2", pady=10)
        self.btn_reset.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        self.btn_reset.bind("<Enter>", lambda e: self.btn_reset.config(bg=BTN_HOVER))
        self.btn_reset.bind("<Leave>", lambda e: self.btn_reset.config(bg=BTN_BG))
        # --- Khung Bàn cờ & Popup (Overlay container) ---
        self.board_container = tk.Frame(self.main_container, bg=BG_COLOR)
        self.board_container.grid(row=3, column=0, sticky="nsew", pady=(5, 5))
        self.board_container.grid_rowconfigure(0, weight=1)
        self.board_container.grid_columnconfigure(0, weight=1)
        # Căn giữa board_frame bằng cách loại bỏ sticky="nsew"
        self.board_frame = tk.Frame(self.board_container, bg=BORDER_COLOR, bd=2)
        self.board_frame.grid(row=0, column=0)
        self.buttons = []
        for i in range(9):
            # Dùng image=self.pixel_img và compound="center" để đặt width/height theo pixel (96x96 pixel là ô vuông hoàn hảo)
            btn = tk.Button(self.board_frame, text="", image=self.pixel_img, compound="center",
                            font=FONT_BOARD, width=96, height=96,
                            bg=CELL_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                            relief="flat", bd=0, command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)
            btn.bind("<Enter>", lambda e, b=btn: self.on_btn_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_btn_leave(b))
        # Popup overlay là con của board_frame để phủ chính xác lên bàn cờ 3x3
        self.overlay_frame = tk.Frame(self.board_frame, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.disable_board()

    def update_settings_ui(self):
        human_sym = self.player_symbol_var.get()
        ai_sym = "O" if human_sym == "X" else "X"
        color_human = COLOR_X if human_sym == "X" else COLOR_O
        color_ai = COLOR_O if human_sym == "X" else COLOR_X
        selected_algo = self.algo_var.get()
        for algo, btn in [("Minimax", self.btn_minimax), ("Alpha-Beta", self.btn_alphabeta), ("Expectimax", self.btn_expectimax)]:
            if selected_algo == algo:
                btn.config(bg=color_human, fg=BG_COLOR)
            else:
                btn.config(bg=BTN_BG, fg=TEXT_COLOR)
        if human_sym == "X":
            self.btn_x.config(bg=COLOR_X, fg=BG_COLOR)
            self.btn_o.config(bg=BTN_BG, fg=TEXT_COLOR)
        else:
            self.btn_x.config(bg=BTN_BG, fg=TEXT_COLOR)
            self.btn_o.config(bg=COLOR_O, fg=BG_COLOR)
        first_turn = self.first_player_var.get()
        if first_turn == "Người":
            self.btn_first_human.config(bg=color_human, fg=BG_COLOR)
            self.btn_first_ai.config(bg=BTN_BG, fg=TEXT_COLOR)
        else:
            self.btn_first_human.config(bg=BTN_BG, fg=TEXT_COLOR)
            self.btn_first_ai.config(bg=color_ai, fg=BG_COLOR)

    def on_btn_enter(self, btn):
        if btn["state"] == "normal" and self.game_active:
            btn.config(bg=BTN_HOVER)
            
    def on_btn_leave(self, btn):
        if btn["state"] == "normal" and self.game_active:
            btn.config(bg=CELL_BG)

    def start_game(self):
        # Ẩn overlay nếu đang hiện
        self.overlay_frame.grid_forget()
        self.board = [' '] * 9
        for btn in self.buttons:
            btn.config(text="", state="normal", bg=CELL_BG)
        self.human_player = self.player_symbol_var.get()
        self.ai_player = 'O' if self.human_player == 'X' else 'X'
        first_turn = self.first_player_var.get()
        if first_turn == "Người":
            self.current_player = self.human_player
        else:
            self.current_player = self.ai_player
        self.game_active = True
        self.update_settings_ui()
        if self.current_player == self.ai_player:
            self.root.after(300, self.ai_move)

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def on_click(self, idx):
        if self.board[idx] == ' ' and self.game_active and self.current_player == self.human_player:
            self.make_move(idx, self.human_player)
            if not self.check_game_over():
                self.current_player = self.ai_player
                self.root.after(300, self.ai_move)

    def make_move(self, idx, player):
        self.board[idx] = player
        color = COLOR_X if player == 'X' else COLOR_O
        self.buttons[idx].config(text=player, fg=color, disabledforeground=color, bg=CELL_BG, state="disabled")
        self.root.update_idletasks()

    def ai_move(self):
        if not self.game_active: return
        algo = self.algo_var.get()
        best_idx = get_best_move(self.board, algo, self.ai_player)
        if best_idx != -1:
            self.make_move(best_idx, self.ai_player)
            if not self.check_game_over():
                self.current_player = self.human_player

    def show_popup(self, result_text, text_color):
        for widget in self.overlay_frame.winfo_children():
            widget.destroy()
        self.overlay_frame.grid_rowconfigure(0, weight=1)
        self.overlay_frame.grid_rowconfigure(1, weight=0)
        self.overlay_frame.grid_rowconfigure(2, weight=1)
        self.overlay_frame.grid_columnconfigure(0, weight=1)
        # Tiêu đề kết quả
        lbl_result = tk.Label(self.overlay_frame, text=result_text, font=("Segoe UI", 18, "bold"),
                              fg=text_color, bg=CARD_BG, justify="center")
        lbl_result.grid(row=0, column=0, pady=(35, 10), sticky="s")
        # Nút chơi lại
        btn_replay = tk.Button(self.overlay_frame, text="Chơi lại", command=self.start_game,
                               bg=COLOR_X, fg=BG_COLOR, font=("Segoe UI", 12, "bold"),
                               relief="flat", bd=0, cursor="hand2", padx=20, pady=8)
        btn_replay.grid(row=1, column=0, pady=(10, 35), sticky="n")
        btn_replay.bind("<Enter>", lambda e: btn_replay.config(bg="#00E5FF"))
        btn_replay.bind("<Leave>", lambda e: btn_replay.config(bg=COLOR_X))
        # Định vị overlay đè lên trên bàn cờ (phủ toàn bộ 3 cột, 3 dòng)
        self.overlay_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.overlay_frame.lift()

    def check_game_over(self):
        if check_win(self.board, self.human_player):
            self.game_active = False
            self.highlight_win(self.human_player)
            self.root.update_idletasks()
            # Trì hoãn hiển thị popup 1 giây để người chơi nhìn rõ nước đi cuối và đường thắng màu xanh lục
            self.root.after(1000, lambda: self.show_popup("CHÚC MỪNG!\nBẠN ĐÃ CHIẾN THẮNG!", COLOR_X if self.human_player == 'X' else COLOR_O))
            return True
        elif check_win(self.board, self.ai_player):
            self.game_active = False
            self.highlight_win(self.ai_player)
            self.root.update_idletasks()
            # Trì hoãn hiển thị popup 1 giây để người chơi nhìn rõ nước đi cuối của AI
            self.root.after(1000, lambda: self.show_popup("GAME OVER!\nAI ĐÃ CHIẾN THẮNG!", COLOR_X if self.ai_player == 'X' else COLOR_O))
            return True
        elif check_draw(self.board):
            self.game_active = False
            self.root.update_idletasks()
            # Trì hoãn hiển thị popup 1 giây để người chơi nhìn rõ bàn cờ hòa trước khi bị che phủ
            self.root.after(1000, lambda: self.show_popup("TRẬN ĐẤU HÒA!\nKẾT QUẢ NGANG SỨC", TEXT_MUTED))
            return True
        return False

    def highlight_win(self, player):
        win_states = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for state in win_states:
            if self.board[state[0]] == self.board[state[1]] == self.board[state[2]] == player:
                for idx in state:
                    self.buttons[idx].config(bg=HIGHLIGHT_WIN_BG, fg=HIGHLIGHT_WIN, disabledforeground=HIGHLIGHT_WIN)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()