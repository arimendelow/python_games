class Board:
	def __init__(self, p1='X', p2='O'):
		self.p1 = p1
		self.p2 = p2
		self.board = [' '] * 9 # Initialize the board to 9 blank values
	
	def printBoard(self):
		print('   A   B   C')
		print(f'1  {self.board[0]} | {self.board[1]} | {self.board[2]}')
		print('  ---+---+---')
		print(f'2  {self.board[3]} | {self.board[4]} | {self.board[5]}')
		print('  ---+---+---')
		print(f'3  {self.board[6]} | {self.board[7]} | {self.board[8]}')

def main():
	board = Board()
	board.printBoard()

if __name__ == "__main__":
	main()
