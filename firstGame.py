import pygame
pygame.init() # Always need to do this

#---------Intro to pygame: just has a colored rectangle that moves around with the arrow keys---------

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window

pygame.display.set_caption("First Game") # Give the window a title

# making our character
x = screenWidth // 2
y = screenHeight // 2
width = 40
height = 60
vel = 5

# Is our character currently jumping?
isJump = False
jumpHeight = 10
jumpCount = jumpHeight

# All pygame programs have a main loop for keeping track of the game
run = True
while run:
	# Give loop a time delay - like a clock in the game
	# pygame.time.delay(100) # Time in MS - this makes it kinda glitchy cuz it's basically saying "wait x MS before updating the frame"

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
	# Right arrow key and less than the screen width
	if keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
		x += vel
	# For jumping:
	if not(isJump):
		# Up arrow key
		if keys[pygame.K_UP] and y > vel:
			y -= vel
		# Down arrow key
		if keys[pygame.K_DOWN] and y < screenHeight - height - vel:
			y += vel
		# Spacebar (jump)
		if keys[pygame.K_SPACE]:
			isJump = True
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
	# draw our character as a rect
	# Cover the window so that we don't just get our character drawn all over the place
	win.fill((0,0,0)) # Just filling it with black
	#			 surface,  color,	   rect
	pygame.draw.rect(win, (255, 50, 100), (x, y, width, height))
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

pygame.quit()