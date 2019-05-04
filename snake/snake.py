import pygame
pygame.init() # Always need to do this

# Commonly used colors
black = (0, 0, 0,)
red = (255, 0, 0,)
green = (0, 255, 0)
blue = (0, 0, 255)

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window
pygame.display.set_caption("Your game name here!") # Give the window a title
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill(black)

# Allow us to change our FPS
clock = pygame.time.Clock()
fps = 10000 # Will get "list index out of range" if we go above this

# Track score
score = 0

# For displaying text
# font = pygame.font.Font('<font name>.ttf', 30) # Size 30

snakeVel = 5
class snakeLink(object):
	# For if character is a square
	def __init__(self, width, height, x, y):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
	
	def draw(self, win):
		self.hitbox = (self.x, self.y, self.width, self.height)
		# Draw the hitbox
		pygame.draw.rect(win, red, self.hitbox)

def redrawGameWindow():
	# Background
	win.blit(bg, (0,0))

	# Update any text - here, score
	# text = font.render('Score:' + str(score), 1, black)
	# win.blit(text, (10, 10))

	# Draw any characters here
	for link in snake:
		link.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

# Main loop

# Make the characters
linkWidth, linkHeight = 10, 10

snake = []
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

# Spawn in the middle of the screen
addSnakeLink(
	x = screenWidth // 2 - linkWidth // 2, 
	y = screenHeight // 2 - linkHeight // 2
)

# Track if the snake has just eaten
# (If we didnt just eat, erase the end of the snake to make up for adding a new beginning of the snake)
justAte = True

run = True
while run:

	# Control the speed of the game - speed it up as the snake gets longer
	clock.tick(100)

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
	if direction == "left" and snakeHead.x > snakeVel:
		direction = "left"
		addSnakeLink(
			x = snakeHead.x - linkWidth,
			y = snakeHead.y
		)
	
	if direction == "right" and snakeHead.x < screenWidth - snakeHead.width - snakeVel:
		direction = "right" 
		addSnakeLink(
			x = snakeHead.x + linkWidth,
			y = snakeHead.y
		)
	
	if direction == "up" and snakeHead.y > snakeVel:
		direction = "up"
		addSnakeLink(
			x = snakeHead.x,
			y = snakeHead.y - linkHeight
		)

	if direction == "down" and snakeHead.y < screenHeight - snakeHead.height - snakeVel:
		direction = "down"
		addSnakeLink(
			x = snakeHead.x,
			y = snakeHead.y + linkHeight
		)
	
	if not justAte:
		snake.pop(len(snake) - 1)

	redrawGameWindow()

pygame.quit()
