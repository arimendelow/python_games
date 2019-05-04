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

# Track score
score = 0

# For displaying text
# font = pygame.font.Font('<font name>.ttf', 30) # Size 30

# Character template
class player(object):
	# For if character is a square
	def __init__(self, width, height, x, y, vel):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.vel = vel
	
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
	p1.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

# Main loop

# Make the characters
p1Width, p1Height = 10, 10
p1 = player(width = p1Width,
	height = p1Height,
	# Spawn in the middle of the screen
	x = screenWidth // 2 - p1Width // 2,
	y = screenHeight // 2 - p1Height // 2,
	vel = 5)

run = True
while run:
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
	if keys[pygame.K_LEFT] and p1.x > p1.vel:
		p1.x -= p1.vel
	
	# Right arrow key and less than the screen width
	elif keys[pygame.K_RIGHT] and p1.x < screenWidth - p1.width - p1.vel:
		p1.x += p1.vel
	
	# Up arrow key
	if keys[pygame.K_UP] and p1.y > p1.vel:
		p1.y -= p1.vel
	# Down arrow key
	if keys[pygame.K_DOWN] and p1.y < screenHeight - p1.height - p1.vel:
		p1.y += p1.vel
	
	redrawGameWindow()

pygame.quit()
