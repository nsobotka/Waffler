from testBoards import *
from viz import *

# scrambled
current = [['C', 'E', 'Y', 'A', 'S'], 
             ['P', ' ', 'E', ' ', 'M'],
             ['L', 'D', 'P', 'H', 'O'],
             ['R', ' ', 'U', ' ', 'R'],
             ['S', 'E', 'U', 'A', 'P']]

# solved
solved = [['C', 'A', 'M', 'P', 'S'],
           ['U', ' ', 'A', ' ', 'Y'],
           ['R', 'O', 'P', 'E', 'R'],
           ['D', ' ', 'L', ' ', 'U'],
           ['S', 'H', 'E', 'E', 'P']]

def twoSwap(current, solved, correctnessStr):
    for i in range(25):
        if correctnessStr[i] == "0":
            for j in range(i + 1, 25):
                if correctnessStr[j] == "0": # found two incorrect cells
                    if current[i] == solved[j] and current[j] == solved[i]: # two swap found
                        return(((i, current[i]), (j, current[j])))
    return None

def threeSwap(current, solved, correctnessStr):
    for i in range(25):
        if correctnessStr[i] == "0":
            for j in range(i + 1, 25):
                if correctnessStr[j] == "0": # found two incorrect cells
                    for k in range(j + 1, 25):
                        if correctnessStr[k] == "0": # found three incorrect cells
                            if ((current[i] == solved[j] and current[j] == solved[k] and current[k] == solved[i]) or
                               (current[i] == solved[k] and current[j] == solved[i] and current[k] == solved[j])): 
                                return(((i, current[i]), (j, current[j])))
    return None

def randSwap(current, solved, correctnessStr):
    for i in range(25):
            if correctnessStr[i] == "0":
                for j in range(i + 1, 25):
                    if correctnessStr[j] == "0": # found two incorrect cells
                        if current[i] == solved[j]: # two swap found
                            return(((i, current[i]), (j, current[j])))
    return None

def fourSwap(current, solved, correctnessStr):
    for i in range(25):
        if correctnessStr[i] == "0":
            for j in range(i + 1, 25):
                if correctnessStr[j] == "0": # found two incorrect cells
                    for k in range(j + 1, 25):
                        if correctnessStr[k] == "0": # found three incorrect cells
                            for l in range(k + 1, 25):
                                if correctnessStr[k] == "0": # found 4 incorrect cells
                                    if ((current[i] == solved[j] and current[j] == solved[k] and current[k] == solved[l] and current[l] == solved[i]) or
                                        (current[i] == solved[j] and current[j] == solved[l] and current[k] == solved[i] and current[l] == solved[k])):
                                        return(((i, current[i]), (j, current[j])))
                                    if ((current[i] == solved[k] and current[k] == solved[j] and current[j] == solved[l] and current[l] == solved[i]) or 
                                        (current[i] == solved[k] and current[k] == solved[l] and current[j] == solved[i] and current[l] == solved[j])):
                                        return(((i, current[i]), (k, current[k])))
                                    if ((current[i] == solved[l] and current[l] == solved[k] and current[k] == solved[j] and current[j] == solved[i]) or
                                        (current[i] == solved[l] and current[l] == solved[j] and current[k] == solved[i] and current[j] == solved[k])): 
                                        return(((i, current[i]), (l, current[l])))
    return None

def buildCorrectnessStr(b1, b2):
    correctnessStr = ""
    for l in range(25):
        if b1[l] == b2[l]:
            correctnessStr += ("1")
        else:
            correctnessStr += ("0")
    return correctnessStr

def swap(b1, currentSwap):
    idxA = currentSwap[0][0]
    idxB = currentSwap[1][0]
    temp = b1[idxA]

    b1List = list(b1)

    b1List[idxA] = b1List[idxB]
    b1List[idxB] = temp

    # updated vars
    b1 = "".join(b1List)
    return b1

# Args: (current, solved)
def main(p1, p2):
    b1 = "".join([letter for row in p1 for letter in row])
    b2 = "".join([letter for row in p2 for letter in row])
    correctnessStr = buildCorrectnessStr(b1, b2)
    swapList = []

    unsolved = True
    changeInner = True
    changeOuter = True
    changeOuterOuter = True
    while unsolved and changeOuterOuter:
        changeInner = True
        changeOuter = True
        changeOuterOuter = False
        while changeOuter:
            changeOuter = False
            changeInner = True
            while changeInner:
                changeInner = False
                currentSwap = twoSwap(b1, b2, correctnessStr)

                # looks for 2 swap
                while(currentSwap is not None):
                    swapList.append(currentSwap)
                    b1 = swap(b1, currentSwap)
                    changeInner = True
                    correctnessStr = buildCorrectnessStr(b1, b2)
                    currentSwap = twoSwap(b1, b2, correctnessStr)

                # Looks for 3 swap
                currentSwap = threeSwap(b1, b2, correctnessStr)
                if currentSwap is not None:
                    swapList.append(currentSwap)
                    b1 = swap(b1, currentSwap)
                    correctnessStr = buildCorrectnessStr(b1, b2)
                    changeInner = True

            # Looks for 4 swap
            currentSwap = fourSwap(b1, b2, correctnessStr)
            if currentSwap is not None:
                swapList.append(currentSwap)
                b1 = swap(b1, currentSwap)
                correctnessStr = buildCorrectnessStr(b1, b2)
                changeOuter = True

        # Looks for random swap
        currentSwap = randSwap(b1, b2, correctnessStr)
        if currentSwap is not None:
            swapList.append(currentSwap)
            b1 = swap(b1, currentSwap)
            correctnessStr = buildCorrectnessStr(b1, b2)
            changeOuterOuter = True

        if b1 != b2:
            unsolved = True
    return swapList


swapList = main(scrambled4, correct4)
viz_swaps(swapList)