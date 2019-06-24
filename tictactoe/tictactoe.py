
def main():
	print("Welcome to Tic Tac Toe, a demo CL based game by Ari Mendelow!")
	p1 = input("What symbol do you want to use to represent player 1? (Default X)\n")
	p2 = input("What symbol do you want to use to represent player 2? (Default O)\n")
	if (p1 != p2 and p1 != "" and p2 != ""):
		board = Board(p1, p2)
	else:
		board = Board()
	print("Let's play!")
	board.printBoard()
	while(board.winnerIs() == None):
		move = list(input("Where do you want to go?\n")) # This will be something like 1A, 2C etc (see the board printout)
		board.go(move[0], move[1])
		board.printBoard()
	print(f"{board.winnerIs()} wins!")

class Board:
	def __init__(self, p1='X', p2='O'):
		self.p1 = p1
		self.p2 = p2
		# Initialize the board to 3 rows of 3 blank values
		self.board = [
			[' ', ' ', ' '],
			[' ', ' ', ' '],
			[' ', ' ', ' ']
			]
		self.turn = self.p1 # P1 goes first

	def go(self, row, col):
		# Convert x and y into indices of the board
		row = int(row) - 1 # Zero index it
		col = ord(col.lower()) - 97
		self.board[row][col] = self.turn
		if self.turn == self.p1:
			self.turn = self.p2
		else:
			self.turn = self.p1

	def printBoard(self):
		print("   A   B   C")
		print(f"1  {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}")
		print("  ---+---+---")
		print(f"2  {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}")
		print("  ---+---+---")
		print(f"3  {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}")
	
	def winnerIs(self):
		#	checks following combinations, after checking if not empty
		#		* * *
		#		- - -
		#		- - -
		#		
		# 	- - -
		#		* * *
		#		- - -
		#
		#		- - -
		#		- - -
		#		* * *
		#
		#		* - -
		#		- * -
		#		- - *
		#
		#		- - *
		#		- * -
		#		* - -
		#
		#		* - -
		#		* - -
		#		* - -
		#		
		# 	- * -
		#		- * -
		#		- * -
		#
		#		- - *
		#		- - *
		#		- - *

		winningCombos = [
			[[0, 0], [0, 1], [0, 2]],
			[[1, 0], [1, 1], [1, 2]],
			[[2, 0], [2, 1], [2, 2]],
			[[0, 0], [1, 1], [2, 2]],
			[[0, 2], [1, 1], [2, 0]],
			[[0, 0], [1, 0], [2, 0]],
			[[0, 1], [1, 1], [2, 1]],
			[[0, 2], [1, 2], [2, 2]],
		]
		for combo in winningCombos:
			[a, b, c] = combo
			# Check if match - need to turn the list of coordinates from above into two distinct integer indices
			if (self.board[a[0]][a[1]] != ' ' and self.board[a[0]][a[1]] == self.board[b[0]][b[1]] and self.board[a[0]][a[1]] == self.board[c[0]][c[1]]):
				# Return the glyph of the winner
				return self.board[a[0]][a[1]]
		# No winner yet
		return None

if __name__ == "__main__":
	main()
