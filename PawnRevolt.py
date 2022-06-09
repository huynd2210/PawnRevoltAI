import time

from easyAI import TwoPlayerGame

class PawnRevolt(TwoPlayerGame):
    def __init__(self, players, boardSize=(5, 3)):
        self.players = players
        self.current_player = 1
        self.boardSize = boardSize
        self.board = self.initBoard()

    def possible_moves(self):
        return self.getAllPossibleMoves(self.board, color=str(self.current_player))

    def make_move(self, move):
        self.move(self.board, move)

    def lose(self):
        return self.opponent_index == int(self.isEnd(self.board)[1])

    def is_over(self):
        return self.isEnd(self.board)[0] is True

    def show(self):
        self.printBoard()

    def scoring(self):
        return -100 if self.lose() else 0

    def initBoard(self):
        # board = [['2'] * 5, ['2'] * 5]
        # board.extend(['.'] * 5 for _ in range(3))
        # board.extend((['1'] * 5, ['1'] * 5))
        sizeI, sizeJ = self.boardSize
        board = [['2'] * sizeJ, ['2'] * sizeJ]
        board.extend(['.'] * sizeJ for _ in range(sizeI - 4))
        board.extend((['1'] * sizeJ, ['1'] * sizeJ))

        return board

    def isEnd(self, board):
        if '1' in board[0]:
            return True, '1'
        if '2' in board[len(board) - 1]:
            return True, '2'
        if all('1' not in i for i in board):
            return True, '2'
        if all('2' not in i for i in board):
            return True, '1'
        return False, '0'

    def getAllPossibleMoves(self, board, color):
        possibleMoves = (self.getAllPossibleMovesFor1(board)
                         if color == '1'
                         else self.getAllPossibleMovesFor2(board))
        return list(map(lambda move: "ABCDEFGHIJ"[move[0]] + str(move[1]) + " " + "ABCDEFGHIJ"[move[2]] + str(move[3]),
                        possibleMoves))


    def isInBound(self, board, i, j):
        return 0 <= i < len(board) and 0 <= j < len(board[0])

    def isLegalMove(self, board, move):
        originI, originJ, destinationI, destinationJ = move
        originPiece = board[originI][originJ]
        if originPiece == '.':
            return False

        if not self.isInBound(board, destinationI, destinationJ):
            return False

        destinationPiece = board[destinationI][destinationJ]
        if originPiece == destinationPiece:
            return False

        return True

    def getAllPossibleMovesFor1(self, board):
        possibleMoves = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '1':
                    allMovesForBluePawn = [(i - 1, j), (i - 1, j + 1), (i - 1, j - 1)]
                    for destination in allMovesForBluePawn:
                        destinationI, destinationJ = destination
                        move = (i, j, destinationI, destinationJ)
                        if self.isLegalMove(board, move):
                            possibleMoves.append(move)
        return possibleMoves

    def getAllPossibleMovesFor2(self, board):
        possibleMoves = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '2':
                    allMovesForRedPawn = [(i + 1, j), (i + 1, j + 1), (i + 1, j - 1)]
                    for destination in allMovesForRedPawn:
                        destinationI, destinationJ = destination
                        move = (i, j, destinationI, destinationJ)
                        if self.isLegalMove(board, move):
                            possibleMoves.append(move)
        return possibleMoves

    def move(self, board, move):
        move = tuple(map(lambda s: ("ABCDEFGHIJ".index(s[0]), int(s[1:])), move.split(" ")))
        origin, destination = move
        originI, originJ = origin
        destinationI, destinationJ = destination
        originPiece = board[originI][originJ]
        board[originI][originJ] = '.'
        board[destinationI][destinationJ] = originPiece

    def printBoard(self):
        board = self.board
        sizeI, sizeJ = self.boardSize
        print("  ", end="")
        for i in range(sizeJ):
            print(i, end=" ")

        print("")
        for i in range(len(board)):
            print("ABCDEFGHI"[i], end="")
            for j in range(len(board[i])):
                print(f' {board[i][j]}', end="")
            print("")
        print()


if __name__ == "__main__":
    from easyAI import AI_Player, Human_Player, Negamax
    start = time.time()
    ai = Negamax(8)
    # game = PawnRevolt([Human_Player(), AI_Player(ai)])
    game = PawnRevolt([AI_Player(ai), AI_Player(ai)])
    game.play()
    end = time.time()
    print("Time:", end - start)
    print("player %d wins after %d turns " % (game.opponent_index, game.nmove))
