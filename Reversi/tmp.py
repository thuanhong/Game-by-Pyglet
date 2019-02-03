def getPos(bo, x, y, enemy): # take position of enemy in 8 directions
    tmp0 = [[x, y-1], [x, y+1], [x+1, y], [x-1, y]]
    tmp1 = [[x-1, y-1], [x-1, y+1], [x+1, y-1], [x+1, y+1]]
    arr = tmp0 + tmp1
    pos = []

    for index in arr:
        if index[0] in range(0, 8) and index[1] in range(0,8):
            if bo[index[0]][index[1]] == enemy:
                pos.append(index)
    return pos


def getValue(bo, statePos, x, y, enemy, diction): # take positions be flip
    step = [statePos[0] - x, statePos[1] - y]
    list = []

    while True:
        x = x + step[0]
        y = y + step[1]
        if not x in range(0, 8) or not y in range(0, 8):
            return
        elif bo[x][y] == enemy:
            list.append([x, y])
        elif bo[x][y] == '.':
            tmp = [x*10+y, list]
            diction.append(tmp)
            return x * 10 + y
        elif bo[x][y] != enemy:
            return


def print_valid_choice(bo, enemy, diction = []): # find move can choice
    the_move = []
    dic = {}
    for x in range(len(bo)): # find positions to be enemy
        for y in range(len(bo)):
            if bo[x][y] != enemy and bo[x][y] != '.':
                dic[x * 10 + y] = getPos(bo, x, y, enemy)

    for x in dic: # return a list contain move can be choice
        for y in dic[x]:
            row = int(x / 10)
            column = int(x % 10)
            the_move.append(getValue(bo, y, row, column, enemy, diction))

    the_move = list(set(the_move))
    if None in the_move:
        the_move.remove(None)
    the_move.sort()
    return the_move


def count(board): # count score of both 2 player
    b = 0
    w = 0
    for x in board:
        b = b + x.count('B')
        w = w + x.count('W')
    return w * 100 + b

def checkend(board): # true if the game cannot continue
    for list in board:
        if '.' in list:
            return False
    return True


def main(board, enemy, pos, can):

    if pos != 100:
        diction = []
        print_valid_choice(board, enemy, diction)

        for x in diction: # Flip all chess have choice follow move choice
            if pos == x[0]:
                for y in x[1]:
                    board[y[0]][y[1]] = 'B' if enemy == 'W' else 'W'

        board[int(pos/10)][int(pos%10)] = 'B' if enemy == 'W' else 'W'
        can = 2
    else:
        can -= 1
    if enemy is 'B':
        enemy = 'W'
    else:
        enemy = 'B'
    return [enemy, can]
