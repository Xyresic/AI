import sys,random,time
class BoardNode:
    def __init__(self,layout):
        self.layout = list(layout)
        self.moves_left = self.layout.count('_')
        if self.moves_left % 2 == 0:
            self.turn = 'o'
        else:
            self.turn = 'x'
        self.endstate = self.check_for_termination()
        self.move_made = None
        self.children = []
        if self.endstate is None and self.moves_left != 9:
            self.generate_children()
        if self.endstate is not None:
            self.best_move = -1
        elif self.moves_left == 9:
            self.best_move = random.randint(0,8)
        else:
            best_score = -2
            best_child = None
            for child in self.children:
                child_score = child.calculate_score(self.turn)
                if child_score > best_score:
                    best_score = child_score
                    best_child = child
            self.best_move = best_child.move_made
        self.moves_to_end = 0

    def check_for_termination(self):
        board = self.layout
        for x in range(3):
            if board[3*x] != '_' and board[3*x] == board[3*x+1] and board[3*x] == board[3*x+2]:
                return board[3*x]
            if board[x] != '_' and board[x] == board[x+3] and board[x] == board[x+6]:
                return board[x]
        if board[4] != '_' and ((board[0] == board[4] and board[0] == board[8]) or (board[2] == board[4] and board[2] == board[6])):
            return board[4]
        if '_' not in board:
            return 'd'
        return None

    def generate_children(self):
        empty = [i for i in range(9) if self.layout[i] == '_']
        for i in empty:
            new_board = self.layout.copy()
            new_board[i] = self.turn
            new_board = ''.join(new_board)
            new_node = BoardNode(new_board)
            new_node.move_made = i
            self.children.append(new_node)

    def calculate_score(self,player):
        if self.endstate == player:
            return 1
        elif self.endstate == 'd':
            return 0
        elif self.endstate is not None:
            return -1
        scores = []
        for move in self.children:
            scores.append(move.calculate_score(player))
        if self.turn == player:
            best = max(scores)
        else:
            best = min(scores)
        return best

    def calculate_moves_to_end(self):
        if self.moves_left == 9:
            self.moves_to_end = 9
            self.final_state = 'd'
        elif self.endstate is not None:
            self.final_state = self.endstate
        else:
            moves = 0
            current = self
            while True:
                if current.endstate is not None:
                    self.final_state = current.endstate
                    break
                for child in current.children:
                    if child.move_made == current.best_move:
                        current = child
                        moves += 1
            self.moves_to_end = moves

parse = {
    -1: 'to not move',
    0: 'upper left',
    1: 'upper center',
    2: 'upper right',
    3: 'middle left',
    4: 'center',
    5: 'middle right',
    6: 'lower left',
    7: 'lower center',
    8: 'lower right',
    'x': 'x wins',
    'o': 'o wins',
    'd': 'draw'
}

start = time.time()
game = BoardNode(sys.argv[2])
game.calculate_moves_to_end()
elapsed = time.time() - start
print(elapsed)
print(game.best_move)
print(game.moves_to_end)
print(game.final_state)
output = str(game.best_move)
output += '\nbest move is %s' % parse[game.best_move]
output += '\n%s in %d move%s' % (parse[game.final_state],game.moves_to_end,'s' if game.moves_to_end != 1 else '')
with open(sys.argv[1],'w') as f:
    f.write(output)
