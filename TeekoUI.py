import tkinter as tk

# IA = 1, joueur = -1
class TeekoUI:

    def __init__(self) -> None:
        self.grid = [[-1,-1,0,0,0],[-1,0,0,0,1],[1,0,-1,1,0],[0,0,0,1,0],[0,0,0,0,0]]
        self.selected = (-1,-1)

        self.root = tk.Tk()
        self.root.configure(background='grey18')
        self.root.title("Teeko")

        self.can = tk.Canvas(self.root, width=508, height=508, bg='grey10', border=0)
        self.can.grid(column=0, row= 1, padx=10, pady=10)
        self.can.bind('<Button-1>', self.on_canvas_click)

        self.btn = tk.Button(text="Reset")
        self.btn.grid(column=0, row = 0)

        self.draw_grid()

        self.root.mainloop()


    def on_canvas_click(self, event):
        x = int(event.x/101)
        y = int(event.y/101) 
        # print(f"coordonées: {x},{y}")

        if (self.grid[x][y] == -1):
            if self.selected == (x,y):
                self.selected = (-1,-1)
            else:
                self.selected = (x,y)
        else:
            self.selected = (-1,-1)

        self.draw_grid()



    def draw_grid(self):
        self.can.delete('all')

        for i in range(4):
            self.can.create_line(0,i*102+100,508,i*102+100,width=2, fill='grey85')
            self.can.create_line(i*102+100,0,i*102+100,508,width=2, fill='grey85')

        for x in range(5):
            for y in range(5):
                # if there is a AI piece in the cell
                if self.grid[x][y] == 1:
                    self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='firebrick2', width=0)
                    # can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='firebrick2', width=4, outline='coral')

                # if these is a player piece in the cell
                elif self.grid[x][y] == -1:
                    #if the piece is selected
                    if self.selected == (x,y):
                        self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='dodger blue', width=4, outline='SteelBlue1')
                    else:
                        self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='dodger blue', width=0)

                # if the cell is empty and adjacent to the selected piece
                if self.selected != (-1,-1) and abs(x-self.selected[0]) <= 1 and abs(y-self.selected[1]) <= 1 and self.grid[x][y] == 0:
                    self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill=None, width=4, outline='SteelBlue1')



    def reset_game(self):
        pass
    

if __name__ == "__main__":
    tui = TeekoUI()




