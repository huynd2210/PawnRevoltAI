import copy

from State import State
import random


def initRoot():
    board = initBoard()
    root = State(board)
    return root


def initBoard():
    board = [['r'] * 5, ['r'] * 5]
    board.extend(['.'] * 5 for _ in range(3))
    board.extend((['b'] * 5, ['b'] * 5))
    return board


def isInBound(board, i, j):
    return 0 <= i < len(board) and 0 <= j < len(board[0])


def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f'|{board[i][j]}', end="")
        print("|")
    print()


def printState(state):
    printBoard(state.board)
    print(state.currentPlayerTurn)
    print(state.isEnd)


def move(board, origin, destination):
    boardCopy = copy.deepcopy(board)
    originPiece = boardCopy[origin[0]][origin[1]]
    if originPiece == '.':
        return False

    if not isInBound(boardCopy, destination[0], destination[1]):
        return False
    destinationPiece = boardCopy[destination[0]][destination[1]]

    boardCopy[origin[0]][origin[1]] = '.'

    if destinationPiece == '.' or destinationPiece != originPiece:
        boardCopy[destination[0]][destination[1]] = originPiece
    else:
        return False

    return boardCopy


def isEnd(board):
    if 'b' in board[0]:
        return True, 'Blue'
    if 'r' in board[len(board) - 1]:
        return True, 'Red'
    if all('b' not in i for i in board):
        return True, 'Red'
    if all('r' not in i for i in board):
        return True, 'Blue'
    return False, 'None'


def isBluePieceExists(board):
    return any('b' not in i for i in board)


def getAllPossibleMoves(board, color):
    return (
        getAllPossibleMovesForBlue(board)
        if color == 'Blue'
        else getAllPossibleMovesForRed(board)
    )


def getAllNextStates(board, color):
    possibleMoves = getAllPossibleMoves(board, color)
    return [
        State(move, isEnd(board), invertColor(color)) for move in possibleMoves
    ]


def invertColor(color):
    return 'Red' if color == 'Blue' else 'Blue'


def getAllPossibleMovesForRed(board):
    possibleMoves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'r':
                firstMove = move(board, (i, j), (i + 1, j))
                secondMove = move(board, (i, j), (i + 1, j + 1))
                thirdMove = move(board, (i, j), (i + 1, j - 1))
                tmp = [firstMove, secondMove, thirdMove]
                possibleMoves.extend(m for m in tmp if m is not False)
    return possibleMoves


def getAllPossibleMovesForBlue(board):
    possibleMoves = []
    for i in range(len(board) - 2, len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'b':
                firstMove = move(board, (i, j), (i - 1, j))
                secondMove = move(board, (i, j), (i - 1, j + 1))
                thirdMove = move(board, (i, j), (i - 1, j - 1))
                tmp = [firstMove, secondMove, thirdMove]
                possibleMoves.extend(m for m in tmp if m is not False)
    return possibleMoves


if __name__ == '__main__':
    board = initBoard()
    # print(board)
    # printBoard(board)
    # move(board, (0, 0), (2, 0))
    # printBoard(board)
    possibleMoves = getAllNextStates(board, 'Blue')
    for i in possibleMoves:
        printState(i)
