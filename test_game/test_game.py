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

# setting our character constants
characterWidth = 64
characterHeight = 64

pygame.display.set_caption("First Game") # Give the window a title

class player(object):
	def __init__(self, width, height, x, y):
		# setting our character constants
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.vel = 5

		# Is our character currently jumping?
		self.isJump = False
		self.jumpHeight = 10
		self.jumpCount = self.jumpHeight

		# Track if our character is standing still
		self.standing = True
		
		# Need to know which frame is on the screen so that we can accurately display it
		self.left = False
		self.right = False
		self.walkCount = 0
	
	def draw(self, win):
		# If walkCount goes over 27 (fps), we'll run out of sprites
		if self.walkCount + 1 >= fps:
			self.walkCount = 0
		
		# If not standing, walking. So animate that
		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
		else: # Otherwise, standing still or jumping
			# Only states when standing still are facing right and left
			if self.right:
				win.blit(walkRight[0], (self.x, self.y)) # Show first image in walkRight array
			else:
				win.blit(walkLeft[0], (self.x, self.y)) # Show first image in walkLeft array

class projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing # 'facing' determines the direction of the projectile

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
	# Put the BG pic
	win.blit(bg, (0,0))

	# Draw the character
	p1.draw(win)

	# Draw the projectiles
	for ammo in projectiles:
		ammo.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

# Main loop
p1 = player(characterWidth, characterHeight, screenWidth // 2, screenHeight -  characterWidth - 10) # -10 to put it 10px above the bottom
projectiles = []
run = True
while run:
	# Give loop a time delay - like a clock in the game
	clock.tick(fps) # Set to 27 FPS

	# Check for events - anything that happens from the user
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If the exit button is pressed
			run = False

	for ammo in projectiles:
		# If ammo is on the screen
		if ammo.x < screenWidth and ammo.x > 0:
			ammo.x += ammo.vel # Move the ammo
		else:
			projectiles.pop(projectiles.index(ammo))

	# Different ways to check if a key is pressed.
	# - Can check the event as above, but that won't account for keys being held down
	# - Can put all of the pressed keys into a list -> going to do this:
	keys = pygame.key.get_pressed()

	if keys[pygame.K_SPACE]:
		if len(projectiles) < 5: # Change this to limit the amount of projectiles that can be on the screen
			if p1.left:
				facing = -1
			else:
				facing = 1
			# Make sure the ammo is coming from the middle of the man
			# Setting radius to 5 and color to black (RGB)
			projectiles.append(projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 5, (0, 0, 0,), facing))

	# -------Move the character---------
	# (Grid (0,0) is top left, bottom right is (max, max))
	# Left arrow key and don't want them to move off the screen
	if keys[pygame.K_LEFT] and p1.x > p1.vel:
		p1.x -= p1.vel
		p1.left = True
		p1.right = False
		p1.standing = False
	# Right arrow key and less than the screen width
	elif keys[pygame.K_RIGHT] and p1.x < screenWidth - p1.width - p1.vel:
		p1.x += p1.vel
		p1.left = False
		p1.right = True
		p1.standing = False
	else: # Otherwise, if not moving left or right
		p1.standing = True
		p1.walkCount = 0
	# For jumping:
	if not(p1.isJump):
		# Up arrow (jump)
		if keys[pygame.K_UP]:
			p1.isJump = True
			# Not moving side to side
			p1.right = False
			p1.left = False
			p1.walkCount = 0
	else:
		if p1.jumpCount >= -p1.jumpHeight:
			# Want our jump to be parabolic in velocity
			neg = 1
			if p1.jumpCount < 0:
				# Controls upwards or downwards movement
				neg = -1
			p1.y -= (p1.jumpCount ** 2) * 0.5 * neg # Square jump count until we reach the max height
			p1.jumpCount -= 1 # Decrement the counter
		else: #jump has concluded
			p1.isJump = False
			p1.jumpCount = p1.jumpHeight
	redrawGameWindow()

pygame.quit()
