from Minmax import minmax, INFINITY
from copy import deepcopy

class Teeko:  

    def eval(self, state):
        grid = state[1]

        square_completion = [0,0]
        h_line_completion = [0,0]
        v_line_completion = [0,0]
        d_line_completion = [0,0]

        # checks for squares
        for i in range(4):
            for j in range(4):
                sc = [0,0]
                for x in range(i, i+2):
                    for y in range(j, j+2):
                        if grid[x][y] > 0:
                            sc[0] = sc[0] + 1
                        elif grid[x][y] <0:
                            sc[1] = sc[1] + 1
                square_completion = [max(square_completion[e],sc[e]) for e in range(2)]

        # checks for horizontal and vertical lines
        for i in range(2):
            for j in range(5):
                hlc = [0,0]
                vlc = [0,0]
                for k in range(i, i+4):
                    if grid[j][k] > 0:
                        hlc[0] = hlc[0] + 1
                    elif grid[j][k] < 0:
                        hlc[1] = hlc[1] + 1

                    if grid[k][j] > 0:
                        vlc[0] = vlc[0] + 1
                    elif grid[k][j] < 0:
                        vlc[1] = vlc[1] + 1
                h_line_completion = [max(h_line_completion[e],hlc[e]) for e in range(2)]
                v_line_completion = [max(v_line_completion[e],vlc[e]) for e in range(2)]

        # checks for diagonal lines

                    
                
        # print(square_completion)
        # print(h_line_completion)
        # print(v_line_completion)
        score = 0
        for i in range(2):
            score = score + (2*square_completion[i] + 1*h_line_completion[i] + v_line_completion[i] + d_line_completion[i]) * pow(-1,i)
        for i in range(2):
            if (square_completion[i]==4 or h_line_completion[i]==4 or v_line_completion[i]==4 or d_line_completion[i]==4):
                score = 10000 * pow(-1,i)
        return score     
        

        #check how many pieces missing for a square
        #check how many pieces mising for a horizontal line
        #check how many pieces mising for a vertical line
        #check how many pieces mising for a diagonal line
        #check how close to the center/corners the pieces are -> closer to center = better for max

        #if winning state-> INFINITY
        #if lossing state -> - INFINITY
        #else -> polynomial function with plenty of coefficients


    # generates all the possible next states from the current one
    # state : (current_player, [[],[],[],[],[]])
    def next_states(self, state):
        current_player, grid = state
        res = []

        # for each cell on the grid
        for x in range(5):
            for y in range(5):

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

    def display_state(self, state):
        player, grid = state
        print(f"{player} is playing")
        for row in grid:
            print("|", end="")
            for cell in row:
                if cell>0:
                    print("+|" , end="")
                elif cell<0:
                    print("-|", end="")
                else:
                    print("0|", end="")
            print("")

stt = (1, [[0,0,0,1,0],[0,1,-1,-1,0],[0,-1,0,1,0],[0,0,1,0,0],[0,0,0,0,-1]])
teeko = Teeko()
teeko.display_state(stt)
# print(teeko.eval(stt))
# for ans in teeko.next_states(stt):
#     teeko.display_state(ans)
#     print(f"eval : {teeko.eval(ans)}\n")
    
# print(f"\n{len(teeko.next_states(stt))}")
# for e in teeko.next_states(stt):
#     print(teeko.eval(e))
score, state2 = minmax(teeko, stt, 2, False)

teeko.display_state(state2)
print(score)