import pygame
import random
pygame.init() # Always need to do this

# Control the size of the elements
foodWidth, foodHeight = 10, 10
linkWidth, linkHeight = 20, 20

# Control the delay of the game - higher numbers means the game moves slower
gameDelay = 0

# Commonly used colors
black = (0, 0, 0,)
white = (255, 255, 255)
red = (255, 0, 0,)
green = (0, 255, 0)
blue = (0, 0, 255)

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window
pygame.display.set_caption("Snake") # Give the window a title
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill(black)

# Track score
score = 0
highScore = 0

# For displaying text
def displayTextCenterAlign(fontSize, text, x, y, color = white):
	font = pygame.font.Font('snake/pixelmix_bold.ttf', fontSize)
	text = font.render(text, True, color)
	textRect = text.get_rect()
	textRect.center = (x, y)
	win.blit(text, textRect)
def displayTextLeftAlign(fontSize, text, x, y, color = white):
	font = pygame.font.Font('snake/pixelmix_bold.ttf', fontSize)
	text = font.render(text, True, color)
	win.blit(text, (x, y))

class snakeLink(object):
	# For if character is a square
	def __init__(self, width, height, x, y):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.hitbox = (self.x, self.y, self.width, self.height)

	def draw(self, win):
		self.hitbox = (self.x, self.y, self.width, self.height)
		# Draw the hitbox
		pygame.draw.rect(win, red, self.hitbox)

class snakeFood(object):
	def __init__(self, width, height, x, y):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.hitbox = (self.x, self.y, self.width, self.height)

	def draw(self, win):
		self.hitbox = (self.x, self.y, self.width, self.height)
		# Draw the hitbox
		pygame.draw.rect(win, white, self.hitbox)

def redrawGameWindow():
	# Background
	win.blit(bg, (0,0))

	displayTextLeftAlign(10, f"Score: {score}", 10, 10, white)

	# Draw any characters here
	for link in snake:
		link.draw(win)
	
	for food in foods:
		food.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

def waitForStart():
	global snake
	global foods
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYUP:
				snake = []
				foods = []
				playGame()
				gameOver()

def homePage():
	win.fill(black)
	displayTextCenterAlign(45, "Welcome to Snake!", screenWidth // 2, screenHeight // 3, white)
	displayTextCenterAlign(20, "press any key to begin", screenWidth // 2, screenHeight // 2, white)
	displayTextCenterAlign(15, "(Controls: Arrow Keys)", screenWidth // 2, screenHeight // 2 + 20, white)
	displayTextCenterAlign(10, "by Ari Mendelow", screenWidth // 2, screenHeight - 10, white)
	pygame.display.update()
	waitForStart()

def gameOver():
	win.fill(black)
	displayTextCenterAlign(45, "You lose!!", screenWidth // 2, screenHeight // 3, white)
	displayTextCenterAlign(30, f"Last score: {score}, high score: {highScore}", screenWidth // 2, screenHeight // 3 + 50, white)
	displayTextCenterAlign(20, "press any key to restart", screenWidth // 2, screenHeight // 2, white)
	displayTextCenterAlign(15, "(Controls: Arrow Keys)", screenWidth // 2, screenHeight // 2 + 20, white)
	displayTextCenterAlign(10, "by Ari Mendelow", screenWidth // 2, screenHeight - 10, white)
	pygame.display.update()
	pygame.time.delay(200)
	waitForStart()

	

# ------------------ Main loop ------------------
snake = []
foods = []
def playGame():
	# Make the characters

	global snake
	global score
	global highScore

	# Direction is always either up, down, left, or right
	direction = "right"

	def addSnakeLink(x, y):
		snake.insert(
			0,
			snakeLink(
				width = linkWidth,
				height = linkHeight,
				x = x,
				y = y
			)
		)
	
	def generateSnakeFood():
		foods.append(
			snakeFood(
				width = foodWidth,
				height = foodHeight,
				x = random.randint(foodWidth, screenWidth - foodWidth),
				y = random.randint(foodHeight, screenHeight - foodHeight)
			)
		)

	# Spawn in the middle of the screen
	addSnakeLink(
		x = screenWidth // 2 - linkWidth // 2, 
		y = screenHeight // 2 - linkHeight // 2
	)

	# Track if the snake has just eaten
	# (If we didnt just eat, erase the end of the snake to make up for adding a new beginning of the snake)
	generateSnakeFood()

	run = True
	while run:
		
		justAte = False
		# Control the speed of the game - speed it up as the snake gets longer
		pygame.time.delay(gameDelay)

		# Check for events - anything that happens from the user
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # If the exit button is pressed
				run = False
		
		# Different ways to check if a key is pressed.
		# - Can check the event as above, but that won't account for keys being held down
		# - Can put all of the pressed keys into a list -> going to do this:
		keys = pygame.key.get_pressed()

		# -------Move the character---------
		# (Grid (0,0) is top left, bottom right is (max, max))
		# Left arrow key and don't want them to move off the screen

		left = True if keys[pygame.K_LEFT] else False
		right = True if keys[pygame.K_RIGHT] else False
		up = True if keys[pygame.K_UP] else False
		down = True if keys[pygame.K_DOWN] else False

		# Make sure only one button is pressed
		if left + right + up + down == 1:
			direction = "left" if left and direction != "right" else direction
			direction = "right" if right and direction != "left"else direction
			direction = "up" if up and direction != "down" else direction
			direction = "down" if down and direction != "up" else direction

		snakeHead = snake[0]
		snakeHead.color = green
		# Check collisions between the head and the rest of the body
		for link in snake[2:]:
			# Check y overlap
			if snakeHead.hitbox[1] < link.hitbox[1] + link.hitbox[3] and snakeHead.hitbox[1] + snakeHead.hitbox[3] > link.hitbox[1]:
				# Check x overlap
				if snakeHead.hitbox[0] < link.hitbox[0] + link.hitbox[2] and snakeHead.hitbox[0] + snakeHead.hitbox[2] > link.hitbox[0]:
					# Overlap
					return # end the game


		if direction == "left":
			direction = "left"
			# If going off the left of the screen
			if snakeHead.x <= 0:
				x = screenWidth - linkWidth
			else:
				x = snakeHead.x - linkWidth
			addSnakeLink(
				x = x,
				y = snakeHead.y
			)
		
		if direction == "right":
			direction = "right" 
			# If going off the right of the screen
			if snakeHead.x + linkWidth >= screenWidth:
				x = 0
			else:
				x = snakeHead.x + linkWidth
			addSnakeLink(
				x = x,
				y = snakeHead.y
			)
		
		if direction == "up":
			direction = "up"
			# If going off the top of the screen
			if snakeHead.y <= 0:
				y = screenHeight - linkHeight
			else:
				y = snakeHead.y - linkHeight
			addSnakeLink(
				x = snakeHead.x,
				y = y
			)

		if direction == "down":
			direction = "down"
			# If going off the bottom of the screen
			if snakeHead.y + linkHeight >= screenHeight:
				y = 0
			else:
				y = snakeHead.y + linkHeight
			addSnakeLink(
				x = snakeHead.x,
				y = y
			)
		
		# Check collisions between head and food
		food = foods[0]
		# Check y overlap
		if snakeHead.hitbox[1] < food.hitbox[1] + food.hitbox[3] and snakeHead.hitbox[1] + snakeHead.hitbox[3] > food.hitbox[1]:
			# Check x overlap
			if snakeHead.hitbox[0] < food.hitbox[0] + food.hitbox[2] and snakeHead.hitbox[0] + snakeHead.hitbox[2] > food.hitbox[0]:
				# Overlap
				score += 1
				highScore = score if score > highScore else highScore
				justAte = True
				foods.pop(0)
				generateSnakeFood()

		if not justAte:
			snake.pop(len(snake) - 1)

		redrawGameWindow()

	pygame.quit()


homePage()