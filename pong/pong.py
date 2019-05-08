import pygame
import random
import math
pygame.init() # Always need to do this

gameName = "Pong"

# Control the size of the elements
paddleWidth = 10
paddleHeight = 50
ballRad = 8

# Controls the speed of the elements
paddleVel = 20
obstVel = 20

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
paddleColor = white
textColor = white

# Make our window - this is what we'll draw on
screenWidth = 1080
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window
pygame.display.set_caption(gameName) # Give the window a title
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

# Global variables
player = object
opponent = object
ball = object

# For displaying text
def displayTextCenterAlign(fontSize, text, x, y, color = textColor):
	font = pygame.font.Font(f"{gameName}/pixelmix_bold.ttf", fontSize)
	text = font.render(text, True, color)
	textRect = text.get_rect()
	textRect.center = (x, y)
	win.blit(text, textRect)
def displayTextLeftAlign(fontSize, text, x, y, color = textColor):
	font = pygame.font.Font(f"{gameName}/pixelmix_bold.ttf", fontSize)
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

class rectangle(object):
	def __init__(self, width, height, x, y, vel, color):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.vel = vel
		self.hitbox = (self.x, self.y, self.width, self.height)
		self.color = color

	def draw(self, win):
		self.hitbox = (self.x, self.y, self.width, self.height)
		# Draw the hitbox
		pygame.draw.rect(win, self.color, self.hitbox)

def redrawGameWindow():
	# Background
	win.blit(bg, (0,0))

	displayTextLeftAlign(20, f"Score: {score}", 10, 10, textColor)
	displayTextLeftAlign(15, f"High score: {highScore}", 10, 40, textColor)

	# Draw any characters here
		# Player
	player.draw(win)
		# Objectives
	# ball.draw(win)
		# Opponent
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

def waitForStart():
	global player
	global ball
	global opponent
	global score
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYUP:
				# Spawn in the middle of the right side of the screen
				player = rectangle(
					width = paddleWidth,
					height = paddleHeight,
					x = 0,
					y = screenHeight // 2 - paddleHeight // 2,
					vel = paddleVel,
					color = paddleColor
				)
				# Generate our first ball
				# todo
				# Generate our opponent
				# todo
				score = 0
				playGame()
				gameOver()

def homePage():
	win.fill(bgColor)
	displayTextCenterAlign(45, f"Welcome to {gameName}!", screenWidth // 2, screenHeight // 3, textColor)
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

def playGame():

	global player
	global ball
	global opponent
	global score
	global highScore

	run = True
	while run:

		clock.tick(60) # Pygame will never show more than 30 frames/second

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
		
		# Paddle can move up and down
		if keys[pygame.K_UP] and player.y > player.vel:
			player.y -= player.vel
		
		if keys[pygame.K_DOWN] and player.y < screenHeight - player.height - player.vel:
			player.y += player.vel



		redrawGameWindow()

	pygame.quit()


homePage()