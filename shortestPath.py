# scrambled
current = [['F', 'H', 'T', 'R', 'H'], 
    ['T', ' ', 'I', ' ', 'P'],
    ['E', 'S', 'G', 'L', 'L'],
    ['O', ' ', 'I', ' ', 'A'],
    ['H', 'R', 'O', 'O', 'Y']]

# solved
solved = [['F', 'L', 'E', 'S', 'H'],
    ['O', ' ', 'I', ' ', 'A'],
    ['R', 'I', 'G', 'O', 'R'],
    ['T', ' ', 'H', ' ', 'P'],
    ['H', 'O', 'T', 'L', 'Y']]

def twoSwap(current, solved, correctnessStr):
    for i in range(25):
        if correctnessStr[i] == "0":
            for j in range(i, 25):
                if correctnessStr[j] == "0": # found two incorrect cells
                    if current[i] == solved[j] and current[j] == solved[i]: # two swap found
                        return(((i, current[i]), (j, current[j])))
    return None

def buildCorrectnessStr(b1, b2):
    correctnessStr = ""
    for l in range(25):
        if b1[l] == b2[l]:
            correctnessStr += ("1")
        else:
            correctnessStr += ("0")
    return correctnessStr

# Args: (current, solved)
def main(p1, p2):
    b1 = "".join([letter for row in p1 for letter in row])
    b2 = "".join([letter for row in p2 for letter in row])
    
    correctnessStr = buildCorrectnessStr(b1, b2)

    # print(correctnessStr)
    currentSwap = twoSwap(b1, b2, correctnessStr)
    while(currentSwap is not None):
        print(currentSwap)

        idxA = currentSwap[0][0]
        idxB = currentSwap[1][0]
        temp = b1[idxA]

        b1List = list(b1)

        b1List[idxA] = b1List[idxB]
        b1List[idxB] = temp

        # updated vars
        b1 = "".join(b1List)
        correctnessStr = buildCorrectnessStr(b1, b2)

        currentSwap = twoSwap(b1, b2, correctnessStr)

main(current, solved)