import pygame
import random
import math
pygame.init() # Always need to do this

gameName = "Pong"

# Control the size of the elements
paddleWidth = 20
paddleHeight = 100
ballRad = 16

# What is the maximum angle (in degrees) of reflection from the paddle?
maxAngle = 45

# Controls the speed of the elements - in px/s
paddleVel = 10
ballVel = 10

# Allow us to set our FPS
clock = pygame.time.Clock()
# redraws per second
RPS = 20

# Commonly used colors
black = (0, 0, 0,)
white = (255, 255, 255)
red = (255, 0, 0,)
green = (0, 255, 0)
blue = (0, 0, 255)

# Colors of the different elements
bgColor = black
paddleColor = white
ballColor = white
textColor = white

# Make our window - this is what we'll draw on
screenWidth = 720
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

# class circle(object):
# 	# For if character is a square
# 	def __init__(self, radius = ballRad, x = screenWidth // 2, y = screenHeight // 2, color = ballColor, xvel = 0, dir = LEFT):
# 		self.radius = radius
# 		self.x = x
# 		self.y = y
# 		self.color = color
# 		self.vel = vel
# 		self.dir = dir

# 	def draw(self, win):
# 		# Draw the circle
# 		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class rectangle(object):
	def __init__(self, width, height, x, y, xVel = 0, yVel = 0, color = white):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.xVel = xVel
		self.yVel = yVel
		self.hitbox = (self.x, self.y, self.width, self.height)
		self.color = color

	def draw(self, win):
		self.hitbox = (self.x, self.y, self.width, self.height)
		# Draw the hitbox
		pygame.draw.rect(win, self.color, self.hitbox)

def redrawGameWindow():
	# Background
	win.blit(bg, (0,0))

	displayTextCenterAlign(20, f"Score: {score}", screenWidth // 2, 10, textColor)
	displayTextCenterAlign(15, f"High score: {highScore}", screenWidth // 2, 40, textColor)

	# Draw any characters here
		# Player
	player.draw(win)
		# Objectives
	ball.draw(win)
	
	# Need to refresh the window to show any s, ie draws
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
					yVel = paddleVel,
					color = paddleColor
				)
				# Generate our first ball
				ball = rectangle(
					width = ballRad,
					height = ballRad,
					x = screenWidth // 2,
					y = screenHeight // 2,
					xVel = -ballVel,
					yVel = 0,
					color = ballColor

				)
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
	timedelta = 0
	while run:
		clock.tick(60) # 60 FPS
		# For tracking how many ms it's been since we last did a display update
		timedelta += clock.tick(60)

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
		if keys[pygame.K_UP] and player.y > player.yVel:
			player.y -= player.yVel
		
		if keys[pygame.K_DOWN] and player.y < screenHeight - player.height - player.yVel:
			player.y += player.yVel

		# Bounce the ball
		# Off the walls
		#todo

		# Off the paddle
		# First of all, did it hit the user's paddle (which, remember, is on the left AKA x = 0)
		if ball.x <= player.x + player.width and ball.x + ball.width > player.x:
			if ball.y < player.y + player.height and ball.y + ball.height > player.y:
				# Hit! Now, bounce.
				# How far is the ball from the center of the paddle?
				ballCenter = ball.y + ballRad // 2
				paddleCenter = player.y + paddleHeight // 2
				ballDelta = ballCenter - paddleCenter # Negative if the ball is on the higher half of the paddle
				# Scale this delta into angle of reflection, from 0 to ±maxAngle°
				ballAngle = ballDelta * maxAngle / (paddleHeight / 2)
				# Now, break up the ball velocity into its x and y components according to this angle
				ball.xVel = abs(math.cos(ballAngle) * ballVel) # abs cuz it needs to be moving right after the bounce
				ball.yVel = math.cos(ballAngle) * ballVel
		
		# Move the ball - rather than controlling the direction of the ball here,
		# the xVel and yVel are made positive or negative by the code handling bouncing
		ball.x += ball.xVel
		ball.y += ball.yVel
			
		# Limit how often it's redrawn
		if timedelta > 1000 / RPS:
			timedelta = 0
			redrawGameWindow()

	pygame.quit()


homePage()