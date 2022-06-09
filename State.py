class State:
    def __init__(self, board, isEnd = False, currentPlayerTurn = 'Blue'):
        self.board = board
        self.isEnd = isEnd
        self.currentPlayerTurn = currentPlayerTurn

