import pygame
import random
pygame.init() # Always need to do this

# Control the size of the elements
playerRad = 8
objRad = 8
obstRad = 5

# Controls the speed of the elements
playerVel = 12
obstVel = 10

# Control the delay of the game - higher numbers means the game moves slower
gameDelay = 0

# Allow us to set our FPS
clock = pygame.time.Clock()

# Commonly used colors
black = (0, 0, 0,)
white = (255, 255, 255)
red = (255, 0, 0,)
green = (0, 255, 0)
blue = (0, 0, 255)

# Colors of the different elements
bgColor = black
playerColor = blue
objColor = green
obstColor = red
textColor = white

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window
pygame.display.set_caption("Eskiv") # Give the window a title
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill(bgColor)

# Track score
score = 0
highScore = 0

# Directions
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

# For displaying text
def displayTextCenterAlign(fontSize, text, x, y, color = textColor):
	font = pygame.font.Font('snake/pixelmix_bold.ttf', fontSize)
	text = font.render(text, True, color)
	textRect = text.get_rect()
	textRect.center = (x, y)
	win.blit(text, textRect)
def displayTextLeftAlign(fontSize, text, x, y, color = textColor):
	font = pygame.font.Font('snake/pixelmix_bold.ttf', fontSize)
	text = font.render(text, True, color)
	win.blit(text, (x, y))

class circle(object):
	# For if character is a square
	def __init__(self, radius, x, y, color, vel = 0, dir = LEFT):
		self.radius = radius
		self.x = x
		self.y = y
		self.color = color
		self.vel = vel
		self.dir = dir

	def draw(self, win):
		# Draw the circle
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redrawGameWindow():
	# Background
	win.blit(bg, (0,0))

	displayTextLeftAlign(20, f"Score: {score}", 10, 10, textColor)
	displayTextLeftAlign(15, f"High score: {highScore}", 10, 40, textColor)

	# Draw any characters here
		# Player
	player.draw(win)
		# Objectives
	for obj in objs:
		obj.draw(win)
		# Obstacles
	for obst in obsts:
		obst.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

def waitForStart():
	global snake
	global foods
	global score
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYUP:
				snake = []
				foods = []
				score = 0
				playGame()
				gameOver()

def homePage():
	win.fill(bgColor)
	displayTextCenterAlign(45, "Welcome to Eskiv!", screenWidth // 2, screenHeight // 3, textColor)
	displayTextCenterAlign(20, "press any key to begin", screenWidth // 2, screenHeight // 2, textColor)
	displayTextCenterAlign(15, "(Controls: Arrow Keys)", screenWidth // 2, screenHeight // 2 + 20, textColor)
	displayTextCenterAlign(10, "by Ari Mendelow", screenWidth // 2, screenHeight - 10, textColor)
	pygame.display.update()
	waitForStart()

def gameOver():
	win.fill(bgColor)
	displayTextCenterAlign(45, "You lose!!", screenWidth // 2, screenHeight // 3, textColor)
	displayTextCenterAlign(30, f"Last score: {score}, high score: {highScore}", screenWidth // 2, screenHeight // 3 + 50, textColor)
	displayTextCenterAlign(20, "press any key to restart", screenWidth // 2, screenHeight // 2, textColor)
	displayTextCenterAlign(15, "(Controls: Arrow Keys)", screenWidth // 2, screenHeight // 2 + 20, textColor)
	displayTextCenterAlign(10, "by Ari Mendelow", screenWidth // 2, screenHeight - 10, textColor)
	pygame.display.update()
	pygame.time.delay(200)
	waitForStart()
	
# ------------------ Main loop ------------------

# Spawn in the middle of the screen
player = circle(playerRad, screenWidth // 2, screenHeight // 2, playerColor, playerVel)
objs = []
obsts = []

def playGame():
	# Make the characters

	global player
	global objs
	global obsts
	global score
	global highScore

	def generateObj():
		objs.append(
			circle(
				radius = objRad,
				x = random.randint(obstRad, screenWidth - obstRad),
				y = random.randint(obstRad, screenHeight - obstRad),
				color = objColor
			)
		)
	
	def generateObst():
		obsts.append(
			circle(
				radius = obstRad,
				x = random.randint(obstRad, screenWidth - obstRad),
				y = random.randint(obstRad, screenHeight - obstRad),
				color = obstColor,
				vel = obstVel,
				dir = random.randint(0, 3)
			)
		)

	# Generate our first objective
	generateObj()

	# Generate our first obstacle
	generateObst()

	run = True
	while run:
		
		# Control the speed of the game - speed it up as the snake gets longer
		pygame.time.delay(gameDelay)
		clock.tick(30) # Pygame will never show more than 30 frames/second

		# Check for events - anything that happens from the user
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # If the exit button is pressed
				run = False

		# Move the obsticles
		for obst in obsts:
			# Direction, plus if hitting the edge of the screen, bounce baby bounce
			if obst.dir == LEFT or obst.dir == RIGHT:
				# Going off left side
				if obst.dir == LEFT and obst.x < obst.vel:
					obst.dir = RIGHT
				# Going off right side
				if obst.dir == RIGHT and obst.x > screenWidth - obst.radius:
					obst.dir = LEFT
				# Move it
				obst.x = obst.x + obst.vel if obst.dir == RIGHT else obst.x - obst.vel
			# If moving up or down
			else:
				# Going off top
				if obst.dir == UP and obst.y < obst.vel:
					obst.dir = DOWN
				# Going off bottom
				if obst.dir == DOWN and obst.y > screenHeight - obst.radius:
					obst.dir = UP
				# Move it
				obst.y = obst.y + obst.vel if obst.dir == DOWN else obst.y - obst.vel
		
		# Different ways to check if a key is pressed.
		# - Can check the event as above, but that won't account for keys being held down
		# - Can put all of the pressed keys into a list -> going to do this:
		keys = pygame.key.get_pressed()

		# -------Move the character---------
		# (Grid (0,0) is top left, bottom right is (max, max))
		# Left arrow key and don't want them to move off the screen

		if keys[pygame.K_LEFT] and player.x > player.vel:
			player.x -= player.vel
		
		if keys[pygame.K_RIGHT] and player.x < screenWidth - player.radius:
			player.x += player.vel
		
		if keys[pygame.K_UP] and player.y > player.vel:
			player.y -= player.vel
		
		if keys[pygame.K_DOWN] and player.y < screenHeight - player.radius:
			player.y += player.vel

		# Check collisions between player and obsticle
			# Game over
		
		# Check collisions between player and objective
		for obj in objs:
			if obj.y - obj.radius < player.y + player.radius and obj.y + obj.radius > player.y - player.radius:
				if obj.x - obj.radius < player.x + player.radius and obj.x + obj.radius > player.x - player.radius:
					score += 1
					objs.pop(objs.index(obj))
					generateObj()
					generateObst()
		
		# Check collisions between player and obstacles
		for obst in obsts:
			if obst.y - obst.radius < player.y + player.radius and obst.y + obst.radius > player.y - player.radius:
				if obst.x - obst.radius < player.x + player.radius and obst.x + obst.radius > player.x - player.radius:
					# Game over
					return

		redrawGameWindow()

	pygame.quit()


homePage()