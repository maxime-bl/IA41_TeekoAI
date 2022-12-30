from Minmax import minmax, INFINITY
from copy import deepcopy
from Helper import range2D, print_state

PLAYER = -1
AI = 1

class Teeko:  

    def __init__(self) -> None:
        difficulty = ''


    def set_difficulty(self, diff):
        self.difficulty = diff


    def get_difficulty(self) -> chr:
        return self.difficulty
        

    def count_pieces(self, state) -> list:
        grid = state[1]

        nb_pieces = [0,0]
        for x in range(5):
            for y in range(5):
                if grid[x][y] == AI:
                    nb_pieces[0] = nb_pieces[0] + 1
                elif grid[x][y] == PLAYER:
                    nb_pieces[1] = nb_pieces[1] + 1
        return nb_pieces


    def eval(self, state, print_details=False):
        grid = state[1]

        square_completion = [0,0]
        h_line_completion = [0,0]
        v_line_completion = [0,0]
        d_line_completion = [0,0]
        dist_from_center = [0,0]

        # checks for squares
        for x,y in range2D((0,0), (3,3)):
            sc = [0,0]
            for x1, y1 in range2D((0,0), (1,1)):
                    if grid[x+x1][y+y1] == AI:
                        sc[0] = sc[0] + 1
                    elif grid[x+x1][y+y1] == PLAYER:
                        sc[1] = sc[1] + 1

            square_completion = [max(square_completion[i],sc[i]) for i in range(2)]
        
        # checks for horizontal and vertical lines
        for x in range(2):
            for y in range(5):
                hlc = [0,0]
                vlc = [0,0]
                for x1 in range(0,4):
                    if grid[x+x1][y] > 0:
                        hlc[0] = hlc[0] + 1
                    elif grid[x+x1][y] < 0:
                        hlc[1] = hlc[1] + 1

                    if grid[y][x+x1] > 0:
                        vlc[0] = vlc[0] + 1
                    elif grid[y][x+x1] < 0:
                        vlc[1] = vlc[1] + 1
                        
                h_line_completion = [max(h_line_completion[i],hlc[i]) for i in range(2)]
                v_line_completion = [max(v_line_completion[i],vlc[i]) for i in range(2)]

        # checks diagonal lines
        for x,y in range2D((0,0),(1,1)):
            adlc = [0,0] # ascending diagonals completion
            ddlc = [0,0] # descending diagonals completion

            for i in range(4):
                if grid[x+i][y+i] == AI:
                    ddlc[0] = ddlc[0] + 1
                elif grid[x+i][y+i] == PLAYER:
                    ddlc[1] = ddlc[1] + 1

                if grid[x+i][4-(y+i)] == AI:
                    adlc[0] = adlc[0] + 1
                elif grid[x+i][4-(y+i)] == PLAYER:
                    adlc[1] = adlc[1] + 1

            d_line_completion = [max(d_line_completion[i], ddlc[i], adlc[i]) for i in range(2)]
        
        
        # checks the average distance to mid       
        if self.count_pieces(state)[0] > 0 and self.count_pieces(state)[1] > 0:
            dfc = [0,0]
            nb_pieces = [0,0]
            for x in range(5):
                for y in range(5):
                    if grid[x][y] == AI:
                        nb_pieces[0] = nb_pieces[0] + 1
                        dfc[0] = dfc[0] + ((2-x)**2+(2-y)**2)**0.5
                    elif grid[x][y] == PLAYER:
                        nb_pieces[1] = nb_pieces[1] + 1
                        dfc[1] = dfc[1] + ((2-x)**2+(2-y)**2)**0.5
            dist_from_center = [dfc[0] / nb_pieces[0] , dfc[1] / nb_pieces[1]]
        

        # calculating score
        score = 0
        # first checks if it is a winning state
        for i, sign in [(0, AI), (1, PLAYER)]:
            for l in [v_line_completion, h_line_completion, square_completion, d_line_completion]:
                if l[i] == 4:
                    score = 10000 * sign

        if abs(score) < 10000:
            for i, sign in [(0, AI), (1, PLAYER)]:
                match(self.difficulty):
                    case 'f':
                        t=-2
                    case 'm':
                        t=-0.5
                    case 'd':
                        t=1
            
                score = score + (square_completion[i]**2) * sign*t
                score = score + (h_line_completion[i]**2) * sign
                score = score + (v_line_completion[i]**2) * sign*t
                score = score + 2*(d_line_completion[i]**2) * sign
                score = score + -2*dist_from_center[i] * sign 

        if print_details:
            print("max horizontal line : ", h_line_completion)
            print("max vertical line :   ", v_line_completion)
            print("max square :          ", square_completion)
            print("max diagonal line :   ", d_line_completion)
            print("avg dist from center  ", dist_from_center)
            print("score :               ", score)

        return score


    # generates all the possible next states from the current one
    # state : (current_player, [[],[],[],[],[]])
    def next_states(self, state) -> list:
        current_player, grid = state
        res = []

        # first phase of the game
        if self.count_pieces(state) != [4,4]:
            for x in range(5):
                for y in range(5):

                    # if the cell is not occupied by a player
                        if grid[x][y] == 0:
                            new_grid = deepcopy(grid)
                            new_grid[x][y] = current_player
                            new_state = ((-current_player, new_grid))
                            res.append(new_state)

        # second phase of the game
        else:
            for x,y in range2D((0,0), (4,4)):

                # if the cell contains one of the current player's pieces
                if grid[x][y] == current_player:

                    # tries to move the piece in all the adjacent cells
                    for x1 in range(x-1,x+2):
                        for y1 in range(y-1, y+2):
                            # if the cell is within the boundaries and is empty
                            if x1 in range(5) and y1 in range(5) and grid[x1][y1] == 0:
                                new_grid = deepcopy(grid)
                                new_grid[x][y] = 0
                                new_grid[x1][y1] = current_player
                                new_state = ((-current_player, new_grid))
                                res.append(new_state)                 
        return res

    def is_final(self, state) -> bool:
        if abs(self.eval(state)) >= 10000:
            return True
        else:
            return False