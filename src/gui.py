import tkinter as tk
from tkinter import messagebox
from game_logic import Game2048

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048 Puzzle Game")
        self.geometry("400x500")
        self.game = Game2048()
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=10)
        self.cells = []
        self.create_grid()
        self.bind("<Key>", self.handle_keypress)
        self.update_grid()

    def create_grid(self):
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(self.grid_frame, text='', width=5, height=2, font=('Arial', 24), borderwidth=2, relief="ridge")
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.game.grid[i, j]
                self.cells[i][j].config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))

    def handle_keypress(self, event):
        moved = False
        if event.keysym == 'Left':
            moved = self.game.slide_left()
        elif event.keysym == 'Right':
            moved = self.game.slide_right()
        elif event.keysym == 'Up':
            moved = self.game.slide_up()
        elif event.keysym == 'Down':
            moved = self.game.slide_down()

        if moved:
            self.update_grid()
            if self.game.has_won():
                self.show_game_over("Congratulations, you reached 2048!")
            elif self.game.is_game_over():
                self.show_game_over("Game Over! No more moves left.")

    def show_game_over(self, message):
        messagebox.showinfo("2048", message)
        self.restart_game()

    def restart_game(self):
        self.game = Game2048()
        self.update_grid()

    def get_tile_color(self, value):
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")
