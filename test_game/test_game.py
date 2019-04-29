import pygame
pygame.init() # Always need to do this

# Load the images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

# Allow us to change our FPS
clock = pygame.time.Clock()
fps = 27 # Will get "list index out of range" if we go above this

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window

pygame.display.set_caption("First Game") # Give the window a title

# setting our character constants
width = 64
height = 64
x = screenWidth // 2
y = screenHeight -  width - 10 # Ten above the bottom
vel = 5

# Is our character currently jumping?
isJump = False
jumpHeight = 10
jumpCount = jumpHeight

# Need to know which frame is on the screen so that we can accurately display it
left = False
right = False
walkCount = 0

def redrawGameWindow():
	global walkCount # Global because we'll be changing it elsewhere

	# Put the BG pic
	win.blit(bg, (0,0))
	
	# If walkCount goes over 27, we'll run out of sprites
	if walkCount + 1 >= fps:
		walkCount = 0
	
	if left:
		win.blit(walkLeft[walkCount // 3], (x, y))
		walkCount += 1
	elif right:
		win.blit(walkRight[walkCount // 3], (x, y))
		walkCount += 1
	else: #otherwise, standing still or jumping
		win.blit(char, (x, y))
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

# All pygame programs have a main loop for keeping track of the game
run = True
while run:
	# Give loop a time delay - like a clock in the game
	clock.tick(fps) # Set to 27 FPS

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
	if keys[pygame.K_LEFT] and x > vel:
		x -= vel
		left = True
		right = False
	# Right arrow key and less than the screen width
	elif keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
		x += vel
		left = False
		right = True
	else: # Otherwise, if not moving left or right
		left = False
		right = False
		walkCount = 0
	# For jumping:
	if not(isJump):
		# Enable the below if you want to be able to move up and down
		# # Up arrow key
		# if keys[pygame.K_UP] and y > vel:
		# 	y -= vel
		# # Down arrow key
		# if keys[pygame.K_DOWN] and y < screenHeight - height - vel:
		# 	y += vel

		# Spacebar (jump)
		if keys[pygame.K_SPACE]:
			isJump = True
			# Not moving side to side
			right = False
			left = False
			walkCount = 0
	else:
		if jumpCount >= -jumpHeight:
			# Want our jump to be parabolic in velocity
			neg = 1
			if jumpCount < 0:
				# Controls upwards or downwards movement
				neg = -1
			y -= (jumpCount ** 2) * 0.5 * neg # Square jump count until we reach the max height
			jumpCount -= 1 # Decrement the counter
		else: #jump has concluded
			isJump = False
			jumpCount = jumpHeight
	redrawGameWindow()

pygame.quit()