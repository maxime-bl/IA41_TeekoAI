def range2D(tpl1: tuple[int, int], tpl2: tuple[int, int]) -> list:
    x1, y1 = tpl1
    x2, y2 = tpl2
    
    return_list = []
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            return_list.append((x,y))

    return return_list

def adjacentCells():
    pass

def print_state(state) -> None:
        player, grid = state
        print(f"{player} is playing")
        for x in range(5):
            print("|", end="")
            for y in range(5):
                cell = grid[y][x]
                if cell>0:
                    print("+|" , end="")
                elif cell<0:
                    print("-|", end="")
                else:
                    print("0|", end="")
            print("")