import sys

txtfile = 'board-2-1.txt'


# compute_manhattan_distance(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

# reads text file and writes to a two dimensional list
def get_board(txtfile):
    board = [line.strip() for line in open(txtfile, 'r')]
    # print (board)
    return board


# get_board('./boards/board-1-1.txt')


# recognizes a char in the board, and returns index
def get_position(char, board):
    for list in board:
        if char in list:
            # print (board.index(list), list.index(char))
            return [board.index(list), list.index(char)]
    else:
        print(char + " could not be found")
        sys.exit(1)


# get_position('B', get_board('./boards/board-1-1.txt'))


def get_heuristic(state, goal):
    return (abs(goal[0] - state[0]) + abs(goal[1] - state[1]))


class node:
    def __init__(self, state, goal):
        self.state = state
        self.goal = goal
        self.g = 0
        self.h = get_heuristic(self.state, goal)
        self.f = self.g + self.h
        # self.status = "open"
        self.children = []


def attach_and_eval(child, parent):
    child.parent = parent
    child.g = parent.g + cost(child)
    child.f = child.g + child.h


def cost(child):
    board = get_board(txtfile)
    if board[child.state[0]][child.state[1]] == '#':
        return 1000
    if board[child.state[0]][child.state[1]] == 'w':
        return 100
    if board[child.state[0]][child.state[1]] == 'm':
        return 50
    if board[child.state[0]][child.state[1]] == 'f':
        return 10
    if board[child.state[0]][child.state[1]] == 'g':
        return 5
    if board[child.state[0]][child.state[1]] == 'r':
        return 1
    return 1


def propagate_path_improvements(parent):
    for child in parent.children:
        if parent.g + cost(child) < child.g:
            child.parent = parent
            child.g = parent.g + cost(child)
            child.f = child.g + child.h
            propagate_path_improvements(child)


def find_path(n, start):
    path = [n]
    while n.state != start:
        n = n.parent
        path.append(n)
    # reverse path?
    return path


def gen_neighbours(parent):
    p_state = parent.state
    goal = parent.goal
    succ = []
    if p_state[0] < len(get_board(txtfile)):
        succ.append(node([p_state[0] + 1, p_state[1]], goal))
    if p_state[0] > 0:
        succ.append(node([p_state[0] - 1, p_state[1]], goal))
    if p_state[1] < len(get_board(txtfile)[0]):
        succ.append(node([p_state[0], p_state[1] + 1], goal))
    if p_state[1] > 0:
        succ.append(node([p_state[0], p_state[1] - 1], goal))
    for s in succ:
        s.g = parent.g + cost(s)

    # succ[0] = node([p_state[0]+1, p_state[1]], 0, goal)
    # succ[1] = node([p_state[0]-1, p_state[1]], 0, goal)
    # succ[2] = node([p_state[0], p_state[1]+1], 0, goal)
    # succ[3] = node([p_state[0], p_state[1]-1], 0, goal)
    return succ


def a_star():
    board = get_board(txtfile)
    start = get_position('A', board)
    goal = get_position('B', board)
    open = []  # sorted list (stigende) of unexpanded nodes
    closed = []  # list of expanded nodes
    n = node(start, goal)
    open.append(n)

    # counter = 0

    while n.state != goal:
        # print (counter)
        # counter += 1

        if not open:
            print("fant faen ikke veien")
            sys.exit(2)
        n = open.pop(0)
        if n.state == goal:
            visualize_path(find_path(n, start), board)
            return find_path(n, start)
        closed.append(n)
        succ = gen_neighbours(n)
        for s in succ:
            for i in open:
                if i.state == s.state:
                    s = i
            for i in closed:
                if i.state == s.state:
                    s = i
            n.children.append(s)
            if s not in open and s not in closed:
                attach_and_eval(s, n)
                open.append(s)
                open.sort(key=lambda x: x.f, reverse=False)
            else:
                if n.g + cost(s) < s.g:
                    attach_and_eval(s, n)
                    if s in closed:
                        propagate_path_improvements(s)


def visualize_path(list, board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            for k in list:
                if [i, j] == k.state:
                    temp = ""
                    for l in range(j):
                        temp += board[i][l]
                    temp += 'o'
                    for l in range(j + 1, len(board[i]), 1):
                        temp += board[i][l]
                    board[i] = temp
                    # board[i.state[0]][i.state[1]] = 'o'
    for i in board:
        print (i)


the_right_path = a_star()
# for i in the_right_path:
# print i.state