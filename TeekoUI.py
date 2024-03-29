import tkinter as tk
from Minmax import minmax
from Teeko import Teeko, PLAYER, AI
from random import choice

UNSELECTED = (-1,-1)
EMPTY = 0
class TeekoUI:

    

    def __init__(self) -> None:
        


        self.teeko = Teeko()
        # self.current_state = (-1, [[1, 0, 0, 0, 0], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0], [0, -1, 0, 1, 0], [-1, 0, -1, 0, 0]])
        self.current_state = (-1, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
        self.selected = UNSELECTED

        DIFFCHOICE = tk.Tk()
        DIFFCHOICE.title('choix de la difficulté')
        DIFFCHOICE.configure(bg='grey16')
        width=400
        height=400
        screenwidth= DIFFCHOICE.winfo_screenwidth()
        screenheight=DIFFCHOICE.winfo_screenheight()
        alignstr='%dx%d+%d+%d' %(width, height, (screenwidth-width)/2,(screenheight-height)/2)
        DIFFCHOICE.geometry(alignstr)

        def facile():
            self.teeko.set_difficulty('f')
            DIFFCHOICE.destroy()

        def moyen():
            self.teeko.set_difficulty('m')
            DIFFCHOICE.destroy()

        def difficile():
            self.teeko.set_difficulty('d')
            DIFFCHOICE.destroy()

        tk.Label(DIFFCHOICE, text='Choisissez votre difficulté',fg='white',bg='grey16',width=200,height=10).pack()
        tk.Button(DIFFCHOICE, text='facile',bg='white',fg='grey16',width=20,height=2,command=facile).pack()
        tk.Button(DIFFCHOICE, text='moyen',bg='white',fg='grey16',width=20,height=2,command=moyen).pack()
        tk.Button(DIFFCHOICE, text='difficile',bg='white',fg='grey16',width=20,height=2,command=difficile).pack()
        DIFFCHOICE.mainloop()

    

        self.root = tk.Tk()
        self.root.configure(background='grey16')
        self.root.title("Teeko")
        width=530
        height=680
        screenwidth_teeko= self.root.winfo_screenwidth()
        screenheight_teeko=self.root.winfo_screenheight()
        alignstr_teeko='%dx%d+%d+%d' %(width, height, (screenwidth_teeko-width)/2,(screenheight_teeko-height)/2)
        self.root.geometry(alignstr_teeko)

        self.can = tk.Canvas(self.root, width=508, height=508, bg='grey10', border=0)
        self.can.grid(column=0, row= 1, padx=10)
        self.can.bind('<Button-1>', self.on_canvas_click)

        self.reset_btn = tk.Button(text="Reset", font=('Helvetica',18), pady=0, command=self.reset_game)
        self.reset_btn.grid(column=0, row = 0, pady=15)

        self.label = tk.Label(self.root, text="", bg='grey16', fg='white', font=('Helvetica',20))
        self.label.grid(column=0, row=2, pady=10)

        self.update_ui()

        self.root.mainloop()


    def on_canvas_click(self, event):
        # ignores clicks on the canvas when the AI is playing
        if self.current_state[0] == PLAYER and not self.teeko.is_final(self.current_state):

            # coordinates of the cell in the grid
            x = int(event.x/101)
            y = int(event.y/101) 

            grid = self.current_state[1]

            # when the game is in the second phase
            if self.teeko.count_pieces(self.current_state) == [4,4]:
                if (grid[x][y] == PLAYER):
                    # unselects the selected piece
                    if self.selected == (x,y):
                        self.selected = UNSELECTED
                    # selects the piece
                    else:
                        self.selected = (x,y)
                    self.update_ui()


                # moves the selected piece to one of the adjacent cells
                elif self.selected != UNSELECTED and abs(x-self.selected[0]) <= 1 and abs(y-self.selected[1]) <= 1 and grid[x][y] == 0:
                    grid[self.selected[0]][self.selected[1]] = EMPTY
                    grid[x][y] = PLAYER
                    self.selected = UNSELECTED
                    self.current_state = (AI,grid)
                    self.update_ui()
                    # lets the AI play
                    self.get_ai_move()

                else:
                    self.selected = UNSELECTED
                    self.update_ui()

            # when the game is in the first phase
            else :
                if grid[x][y] == EMPTY:
                    grid[x][y] = PLAYER
                    self.current_state = (AI,grid)
                    self.update_ui()
                    # lets the AI play
                    self.get_ai_move()


    def update_ui(self):
        self.draw_grid()
        
        if self.teeko.is_final(self.current_state):
            if self.current_state[0] == PLAYER:
                self.label.config(text = "Victoire de l'IA", fg='firebrick1')
            else:
                self.label.config(text = "Victoire du joueur", fg='green2')
        else:
            if self.current_state[0] == PLAYER:
                self.label.config(text = "C'est à votre tour de jouer", fg='white')
            else:
                self.label.config(text = "L'ordinateur est en train de jouer", fg='gold')

            self.root.update()


    def draw_grid(self):
        self.can.delete('all')
        grid = self.current_state[1]

        for i in range(4):
            self.can.create_line(0,i*102+100,508,i*102+100,width=2, fill='grey85')
            self.can.create_line(i*102+100,0,i*102+100,508,width=2, fill='grey85')

        for x in range(5):
            for y in range(5):
                # if there is a AI piece in the cell
                if grid[x][y] == AI:
                    self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='firebrick2', width=0)
                    # can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='firebrick2', width=4, outline='coral')

                # if these is a player piece in the cell
                elif grid[x][y] == PLAYER:
                    #if the piece is selected
                    if self.selected == (x,y):
                        self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='dodger blue', width=4, outline='SteelBlue1')
                    else:
                        self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill='dodger blue', width=0)

                # if the cell is empty and adjacent to the selected piece
                if self.selected != UNSELECTED and abs(x-self.selected[0]) <= 1 and abs(y-self.selected[1]) <= 1 and grid[x][y] == 0:
                    self.can.create_oval(x * 101.5 + 5,y * 101.5 + 5,x * 101.5 + 95,y * 101.5 + 95, fill=None, width=4, outline='SteelBlue1')

    def reset_game(self):
        self.current_state = (-1, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
        self.update_ui()


    def get_ai_move(self):
        if not self.teeko.is_final(self.current_state):
            if self.teeko.get_difficulty() == 'd':
                _, new_state = minmax(self.teeko, self.current_state, 4)
            elif self.teeko.get_difficulty == 'm':
                _, new_state = minmax(self.teeko, self.current_state, 2)
            else:
                _, new_state = minmax(self.teeko, self.current_state, 1)

            self.current_state = new_state
            self.update_ui()

if __name__ == "__main__":
    tui = TeekoUI()




