
def main():
	print("Welcome to Tic Tac Toe, a demo CL based game by Ari Mendelow!")
	p1 = input("What symbol do you want to use to represent player 1? (Default X)\n")
	p2 = input("What symbol do you want to use to represent player 2? (Default O)\n")
	if (p1 != p2 and p1 != "" and p2 != ""):
		board = Board(p1, p2)
	else:
		board = Board()
	print("Let's play!")
	board.isGameOver()


class Board:
	def __init__(self, p1='X', p2='O'):
		self.p1 = p1
		self.p2 = p2
		self.board = [' '] * 9 # Initialize the board to 9 blank values
	
	def printBoard(self):
		print("   A   B   C")
		print(f"1  {self.board[0]} | {self.board[1]} | {self.board[2]}")
		print("  ---+---+---")
		print(f"2  {self.board[3]} | {self.board[4]} | {self.board[5]}")
		print("  ---+---+---")
		print(f"3  {self.board[6]} | {self.board[7]} | {self.board[8]}")
	
	def isGameOver(self):
		winningCombos = [
			[0, 1, 2],
			[3, 4, 5],
			[6, 7, 8],
			[0, 3, 6],
			[1, 4, 7],
			[2, 5, 8],
			[0, 4, 8],
			[2, 4, 6]
		]
		for combo in winningCombos:
			[a, b, c] = combo
			# Check if match
			if (self.board[a] != ' ' and self.board[a] == self.board[b] and self.board[a] == self.board[c]):
				# Return the glyph of the winner
				return self.board[a]
		# No winner yet
		return None

if __name__ == "__main__":
	main()
