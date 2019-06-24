
def main():
	print("Welcome to Tic Tac Toe, a demo CL based game by Ari Mendelow!")
	p1 = input("What symbol do you want to use to represent player 1? (Default X)\n")
	p2 = input("What symbol do you want to use to represent player 2? (Default O)\n")
	if (p1 != p2 and p1 != "" and p2 != ""):
		board = Board(p1, p2)
	else:
		board = Board()
	print(f"Player 1 is {board.p1} and player 2 is {board.p2}")

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

if __name__ == "__main__":
	main()
