import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from game import Game
import json


from player import Player


class MahjongGUI(tk.Tk):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.title("Mahjong Game")

        with open('tileImages.json', 'r') as file:
            self.tileImages = json.load(file)  # Creates a dictionary containing an entire set of tiles

        self.image_buttons = []
        self.selected_image = None
        self.selected_tile = None

        # Initialize GUI components
        self.create_widgets()

    def create_widgets(self):
        # Frame for player's hand
        self.hand_frame = ttk.Frame(self)
        self.hand_frame.pack(pady=10)

        # Label for player's hand
        ttk.Label(self.hand_frame, text="Player's Hand:").grid(row=0, column=0, padx=5, pady=5)

        # Label to display player's hand
        self.hand_label = ttk.Label(self.hand_frame, text="")
        self.hand_label.grid(row=1, column=0, padx=5, pady=5)

        # Button to draw tile
        self.draw_button = ttk.Button(self, text="Draw Tile", command=self.draw_tile)
        self.draw_button.pack(pady=5)

        # Button to discard tile
        self.discard_button = ttk.Button(self, text="Discard Tile", command=lambda: self.discard_tile())
        self.discard_button.pack(pady=5)

        # Status bar to display game information
        self.status_bar = ttk.Label(self, text="Player's Turn")
        self.status_bar.pack(side="bottom", fill="x")

        # Update hand display
        self.update_hand_display()

    def update_hand_display(self):

        self.selected_tile = None
        self.selected_image = None
        for button in self.image_buttons:
            button.destroy()
        self.image_buttons = []

        # Update the displayed hand based on the player's current hand
        index = 0
        #self.player._hand.sort()
        for i in self.player._hand:
            image_path = self.tileImages.get(i) # Grab the path to the tile's image file based on whats in the hand
            img = PhotoImage(file=image_path)
            img = img.subsample(20, 20) # Shrink each icon so the screen isnt filled by TWO TILES LIKE TF

            tile = [index, i]

            # Add the tile to an array of tiles to display
            image_button = tk.Button(self, image=img, command=lambda t=tile: self.select_image(t))
            image_button.image = img
            image_button.pack(side=tk.LEFT, padx=5)
            self.image_buttons.append(image_button)
            index += 1

        hand_str = ", ".join(self.player._hand)
        self.hand_label.config(text=hand_str)

    def select_image(self, tile):
        print(tile[1])
        if self.selected_image:
            # Deselect the previously selected image
            self.selected_image.config(relief=tk.RAISED)
            self.selected_image = None

            # Select the clicked image
        self.selected_image = self.image_buttons[tile[0]]
        self.selected_image.config(relief=tk.SUNKEN)
        self.selected_tile = tile[1]

    def draw_tile(self):
        # Logic for drawing a tile
        if len(self.player._hand) != 13:
            messagebox.showinfo("Draw Tile", "Discard a tile first!")
        else:
            drawn_tile = self.player.draw()
            if drawn_tile:
                messagebox.showinfo("Draw Tile", f"You drew: {drawn_tile}")
                self.update_hand_display()
            else:
                messagebox.showinfo("Draw Tile", "No more tiles to draw!")

    def discard_tile(self):
        # Logic for discarding a tile
        if len(self.player._hand) != 14:
            messagebox.showinfo("Discard Tile", "Draw a tile first!")
        elif self.player._hand:
            discarded_tile = self.player.p_discard(self.selected_tile)  # Assume Player class has a discard_tile method
            messagebox.showinfo("Discard Tile", f"You discarded: {discarded_tile}")
            self.update_hand_display()
        else:
            messagebox.showinfo("Discard Tile", "Hand is already empty!")

# Example usage
if __name__ == "__main__":
    # Initialize the player
    game = Game()
    player = Player(["2_char", "3_char", "5aka_char", "2_circ", "3_circ", "6_circ", "6_circ", "6_bamb", "7_bamb", "7_bamb", "r_drag", "r_drag", "r_drag"], "e", game)

    # Create and run the GUI
    app = MahjongGUI(player)
    app.mainloop()
