import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

'''
Picks and returns a random move.
'''
def findRandomMove(validMoves):
	return validMoves[random.randint(0, len(validMoves)-1)]

'''
Find the best move based on material alone.
'''
def findBestMove(gs, validMoves):
	turnMultiplier = 1 if gs.whiteToMove else -1
	opponentMinMaxScore = CHECKMATE
	bestPlayerMove = None
	random.shuffle(validMoves)
	for playerMove in validMoves:
		gs.makeMove(playerMove)
		opponentsMoves = gs.getValidMoves()
		if gs.stalemate:
			opponentMaxScore = STALEMATE
		elif gs.checkmate:
			opponentMaxScore = -CHECKMATE
		else:
			opponentMaxScore = -CHECKMATE
			for opponentsMove in opponentsMoves:
				gs.makeMove(opponentsMove)
				gs.getValidMoves()
				if gs.checkmate:
					score = CHECKMATE
				elif gs.stalemate:
					score = STALEMATE
				else:
					score = -turnMultiplier * scoreMaterial(gs.board)
				if score > opponentMaxScore:
					OpponentMaxScore = score
				gs.undoMove()
		if opponentMaxScore < opponentMinMaxScore:
			opponentMinMaxScore = opponentMaxScore
			bestPlayerMove = playerMove
		gs.undoMove()
	return bestPlayerMove

'''
Helper method to make first recursive call
'''
def findBestMove(gs, validMoves):
	global nextMove
	nextMove = None
	findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
	return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
	global nextMove
	if depth == 0:
		return scoreMaterial(gs.board)

	if whiteToMove:
		maxScore = -CHECKMATE
		for move in validMoves:
			gs.makeMove(move)
			nextMoves = gs.getValidMoves()
			score = findMoveMinMax(gs, nextMoves, depth - 1, False)
			if score > maxScore:
				maxScore = score
				if depth == DEPTH:
					nextMove = move
			gs.undoMove()
		return maxScore

	else:
		minScore = CHECKMATE
		for move in validMoves:
			gs.makeMove(move)
			nextMoves = gs.getValidMoves()
			score = findMoveMinMax(gs, nextMoves, depth - 1, True)
			if score < minScore:
				minScore = score
				if depth == DEPTH:
					nextMove = move
			gs.undoMove()
		return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
	global nextMove
	if depth == 0:
		return turnMultiplier * scoreBoard(gs)

	maxScore = -CHECKMATE
	for move in validMoves:
		gs.makeMove(move)
		nextMoves = gs.getValidMoves()
		score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
		if score > maxScore:
			maxScore = score
			if depth == DEPTH:
				nextMove = move
		gs.undoMove()
	return maxScore


'''
A positive score is good for white, a negative score is good for black
'''
def scoreBoard(gs):
	if gs.checkmate:
		if gs.whiteToMove:
			return -CHECKMATE #black wins
		else:
			return CHECKMATE #white wins
	elif  gs.stalemate:
		return STALEMATE

	score = 0
	for row in gs.board:
		for square in row:
			if square[0] == 'w':
				score += pieceScore[square[1]]
			elif square[0] == 'b':
				score -= pieceScore[square[1]]
			
	return score

'''
Score the board based on material.
'''
def scoreMaterial(board):
	score = 0
	for row in board:
		for square in row:
			if square[0] == 'w':
				score += pieceScore[square[1]]
			elif square[0] == 'b':
				score -= pieceScore[square[1]]
			
	return score