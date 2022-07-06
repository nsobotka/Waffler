# visualizer
def viz(p):
    for row in p:
        print(f"{row}\n")

# Prints out the board
def viz_solutions(l):
    for i in range(len(l)):
        if i < 3:
            print(f'row {i + 1} {l[i]} \n \n')
        else:
            print(f'col {i - 2} {l[i]} \n \n')