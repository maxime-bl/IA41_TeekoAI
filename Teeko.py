from Minmax import minmax, INFINITY
from copy import deepcopy

class Teeko:  

    def count_pieces(self, state):
        grid = state[1]
        nb_pieces = [0,0]
        for x in range(5):
            for y in range(5):
                if grid[x][y] > 0:
                    nb_pieces[0] = nb_pieces[0] + 1
                elif grid[x][y] < 0:
                    nb_pieces[1] = nb_pieces[1] + 1
        return nb_pieces

    def eval(self, state):
        grid = state[1]

        square_completion = [0,0]
        h_line_completion = [0,0]
        v_line_completion = [0,0]
        d_line_completion = [0,0]
        dist_from_center = [0,0]

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
        max_asc_diag = [0,0]

        # Ascending
        for row in range (3,5):
            for column in range (0,2):

                # Check for 4 in a row ascending
                if grid[row][column] > 0 and grid[row - 1][column + 1] > 0 and grid[row - 2][column + 2] > 0 and grid[row - 3][column + 3] > 0:
                    max_asc_diag[0] = 4
                
                if grid[row][column] < 0 and grid[row - 1][column + 1] < 0 and grid[row - 2][column + 2] < 0 and grid[row - 3][column + 3] < 0:
                    max_asc_diag[1] = 4

        for row in range (2,5):
            for column in range (0,3):
                
                # Check for 3 in a row ascending
                if grid[row][column] > 0 and grid[row - 1][column + 1] > 0 and grid[row - 2][column + 2] > 0:
                    max_asc_diag[0] = max(max_asc_diag[0],3)

                if grid[row][column] < 0 and grid[row - 1][column + 1] < 0 and grid[row - 2][column + 2] < 0:
                    max_asc_diag[1] = max(max_asc_diag[1],3)

        for row in range (1,5):
            for column in range (0,4):   
                
                # Check for 2 in a row ascending
                if grid[row][column] > 0 and grid[row - 1][column + 1] > 0:
                    max_asc_diag[0] = max(max_asc_diag[0],2)

                if grid[row][column] < 0 and grid[row - 1][column + 1] < 0:
                    max_asc_diag[1] = max(max_asc_diag[1],2)

        # Case if 1 max ascending
        max_asc_diag[0] = max(max_asc_diag[0],1)
        max_asc_diag[1] = max(max_asc_diag[1],1)

        max_desc_diag = [0,0]
        # Descending

        for row in range (3,5):
            for column in range (3,5):

                # Check for 4 in a row descending
                if grid[row][column] > 0 and grid[row - 1][column - 1] > 0 and grid[row - 2][column - 2] > 0 and grid[row - 3][column - 3] > 0:
                    max_desc_diag[0] = 4

                if grid[row][column] < 0 and grid[row - 1][column - 1] < 0 and grid[row - 2][column - 2] < 0 and grid[row - 3][column - 3] < 0:
                    max_desc_diag[1] = 4

        for row in range (2,5):
            for column in range (2,5):
                
                # Check for 3 in a row ascending
                if grid[row][column] > 0 and grid[row - 1][column - 1] > 0 and grid[row - 2][column - 2] > 0:
                    max_desc_diag[0] = max(max_desc_diag[0],3)

                if grid[row][column] < 0 and grid[row - 1][column - 1] < 0 and grid[row - 2][column - 2] < 0:
                    max_desc_diag[1] = max(max_desc_diag[1],3)

        for row in range (1,5):
            for column in range (1,5):
                
                # Check for 2 in a row ascending
                if grid[row][column] > 0 and grid[row - 1][column - 1] > 0:
                    max_desc_diag[0] = max(max_desc_diag[0],2)

                if grid[row][column] < 0 and grid[row - 1][column - 1] < 0:
                    max_desc_diag[1] = max(max_desc_diag[1],2)

        # Case if 1 max descending
        max_desc_diag[0] = max(max_desc_diag[0],1)
        max_desc_diag[1] = max(max_desc_diag[1],1)
                    

        d_line_completion[0] = max(max_desc_diag[0],max_asc_diag[0])
        d_line_completion[1] = max(max_desc_diag[1],max_asc_diag[1])

        
        # checks the average distance to mid
        dfc = [0,0]
        nb_pieces = [0,0]
        for x in range(5):
            for y in range(5):
                if grid[x][y] > 0:
                    nb_pieces[0] = nb_pieces[0] + 1
                    dfc[0] = dfc[0] + ((2-x)**2+(2-y)**2)**0.5
                elif grid[x][y] < 0:
                    nb_pieces[1] = nb_pieces[1] + 1
                    dfc[0] = dfc[0] + ((2-x)**2+(2-y)**2)**0.5
        dist_from_center = [dfc[0] / nb_pieces[0] , dfc[1] / nb_pieces[1]]
        # print(dist_from_center[0],dist_from_center[1])
        # print(nb_pieces)
                    
        #print(d_line_completion[0]) 
        #teeko.display_state(state)       
        # print(square_completion)
        # print(h_line_completion)
        # print(v_line_completion)
        score = 0
        for i in range(2):
            score = score + (2*square_completion[i] + 1*h_line_completion[i] + v_line_completion[i] + d_line_completion[i] - 0.25*dist_from_center[i]) * pow(-1,i)
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

    def next_states_beginning(self, state):
        current_player, grid = state
        res = []

         # for each cell on the grid
        for x in range(5):
            for y in range(5):

                # if the cell is not occupied by a player
                    if grid[x][y] == 0:
                        new_grid = deepcopy(grid)
                        new_grid[x][y] = current_player
                        new_state = ((-current_player, new_grid))
                        res.append(new_state)
        return res


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

#stt = (1, [[0,1,0,0,0],[0,0,0,-1,0],[0,0,0,1,0],[0,-1,0,1,0],[-1,0,0,0,0]])
stt = (1, [[0,1,0,0,0],[0,0,0,-1,0],[0,1,0,1,0],[0,-1,0,1,0],[-1,0,0,0,-1]])
teeko = Teeko()

teeko.display_state(stt)
#print(teeko.eval(stt))
# for ans in teeko.next_states(stt):
#     teeko.display_state(ans)
#     print(f"eval : {teeko.eval(ans)}\n")
    
# print(f"\n{len(teeko.next_states(stt))}")
# for e in teeko.next_states(stt):
#     print(teeko.eval(e))
score, state2 = minmax(teeko, stt, 4, False)

teeko.display_state(state2)
print(score)