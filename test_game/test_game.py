import pygame
pygame.init() # Always need to do this

# Load the images
bg = pygame.image.load('bg.jpg')

# Allow us to change our FPS
clock = pygame.time.Clock()
fps = 27 # Will get "list index out of range" if we go above this

# Make our window - this is what we'll draw on
screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) # Giving it a touple with the size of the window

# Setting our character constants
characterWidth = 64
characterHeight = 64

# Colors used throughout
black = (0, 0, 0,)
red = (255, 0, 0,)
green = (0, 128, 0)

# Track score
score = 0

pygame.display.set_caption("Silly Dumb Test Game HOORAY! (in all honesty you cannot win this game)") # Give the window a title

class player(object):
	# Load images
	walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
	walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

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
		self.left = True
		self.right = False
		self.walkCount = 0

		# Hitbox, for collision
		self.hitbox = (self.x + 20, self.y + 12, 22, 50)

		# Penalty, when hit
		self.penalty = 5
	
	def draw(self, win):
		# If walkCount goes over 27 (fps), we'll run out of sprites
		if self.walkCount + 1 >= fps:
			self.walkCount = 0
		
		# If not standing, walking. So animate that
		if not(self.standing):
			if self.left:
				win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
		else: # Otherwise, standing still or jumping
			# Only states when standing still are facing right and left
			if self.right:
				win.blit(self.walkRight[0], (self.x, self.y)) # Show first image in walkRight array
			else:
				win.blit(self.walkLeft[0], (self.x, self.y)) # Show first image in walkLeft array
		
		self.hitbox = (self.x + 20, self.y + 12, 22, 50) # Update the hitbox's location
		# Draw the characters hitbox, for testing
		# pygame.draw.rect(win, red, self.hitbox, 2)
	
	def hit(self):
		# Reset location
		self.x = screenWidth // 2
		self.y = screenHeight -  characterHeight - 10
		self.walkCount = 0
		font1 = pygame.font.Font('pixelmix_bold.ttf', 50) # Size 30
		text = font1.render("You lose!", 1, red)
		win.blit(text, (screenWidth // 2 - text.get_width() // 2, screenHeight // 2 - text.get_height()))
		pygame.display.update()

		# Freeze the game for a moment, but allow the user to still quit
		for x in range(100):
			pygame.time.delay(10)
			for event in pygame.event.get():
				if event.type == pygame.quit:
					x = 100 * 10 + 1 # Skip to the end of the counter
					pygame.quit()

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

class enemy(object):
	# Load images
	walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
	walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

	def __init__(self, width, height, x, y, end):
		# setting our enemy constants
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.end = end
		self.path = [self.x, self.end] # Track where we're starting and ending
		self.walkCount = 0 # For knowing which image we're on
		self.vel = 3

		self.hitbox = (self.x + 17, self.y + 2, 31, 57)

		self.maxHealth = 10
		self.health = self.maxHealth
		# self.visible = True # Once his health is done, we're going to get rid of him
	
	def draw(self, win):
		self.move()
		# Only draw him if he's alive (visible)
		# if self.visible:
		if self.walkCount + 1 >= 33: # 33 because 11 images
			self.walkCount = 0
		if self.vel > 0: # Moving right
			win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
			self.walkCount += 1
		else: # Moving left
			win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
			self.walkCount += 1
	
		# Draw the health bar
		# Make the hitbox 20 over the character, 50 wide, and 10 high
		barWidth = 50
		barHeight = 10
		barOffset = 20
		pygame.draw.rect(win, red, (self.hitbox[0], self.hitbox[1] - barOffset, barWidth, barHeight))
		pygame.draw.rect(win, green, (self.hitbox[0], self.hitbox[1] - barOffset, barWidth - ((barWidth/self.maxHealth) * (self.maxHealth -  self.health)), barHeight))

		self.hitbox = (self.x + 17, self.y + 2, 31, 57) # Update the hitbox's location
		# Draw the characters hitbox, for testing
		# pygame.draw.rect(win, (255, 0, 0,), self.hitbox, 2)
		
	# Just going to move side to side
	def move(self):
		if self.vel > 0: # If moving to the right
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
		else: # If moving to the left
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
	
	def hit(self):
		if self.health > 0:
			self.health -= 1
		# else:
		# 	self.visible = False

def redrawGameWindow():
	# Put the BG pic
	win.blit(bg, (0,0))

	# Show the score
	text = font.render('Score:' + str(score), 1, black)
	win.blit(text, (10, 10))

	# Draw the characters
	p1.draw(win)
	for enemy in enemies:
		enemy.draw(win)

	# Draw the projectiles
	for ammo in projectiles:
		ammo.draw(win)
	
	# Need to refresh the window to show any updates, ie draws
	pygame.display.update()

# Main loop
projectiles = []
enemies = []

p1 = player(width = characterWidth,
	height = characterHeight,
	x = screenWidth // 2,
	y = screenHeight - characterHeight - 10) # -10 to put it 10px above the bottom

def newEnemy():
	enemies.append(
		enemy(width = characterWidth,
		height = characterHeight,
		x = 0,
		y = screenHeight -  characterHeight - 10,
		end = screenWidth - 200))

newEnemy()

# For making each press of the spacebar cause only one shot
space_up = True
# For score displaying
font = pygame.font.Font('pixelmix_bold.ttf', 30) # Size 30

run = True
while run:
	# Give loop a time delay - like a clock in the game
	clock.tick(fps) # Set to 27 FPS

	# Check for events - anything that happens from the user
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If the exit button is pressed
			run = False

	# Collision checking between enemy and player
	# Named it 'e' instead of 'enemy' because the object is already called 'enemy'
	for e in enemies:
		# If the y range of the e overlaps with that of the player...
		if e.hitbox[1] < p1.hitbox[3] + p1.hitbox[1] and e.hitbox[1] + e.hitbox[3] > p1.hitbox[1]:
			# ... AND if the x range of the e overlaps with that of the player
			if e.hitbox[0] < p1.hitbox[0] + p1.hitbox[2] and e.hitbox[0] + e.hitbox[2] > p1.hitbox[0]:
				p1.hit()
				# Reset game
				score = 0

				# In case of jumping while death
				p1.isJump = False
				p1.jumpCount = p1.jumpHeight

				enemies.pop(enemies.index(e))
				newEnemy()

	# Collision checking between ammo and enemy
	for ammo in projectiles:
		for e in enemies:
			# if above the bottom of the hitbox, AND below the top of the hitbox...
			if ammo.y - ammo.radius < e.hitbox[1] + e.hitbox[3] and ammo.y + ammo.radius > e.hitbox[1]:
				# ...and if between the right side of the hitbox AND the left side of the hitbox...
				if ammo.x - ammo.radius < e.hitbox[0] + e.hitbox[2] and ammo.x + ammo.radius > e.hitbox[0]:
					# ...then the ammo is totally in the hitbox, and we have collision
					e.hit()
					score += 1
					projectiles.pop(projectiles.index(ammo))
					# If the enemy is dead, pop em and make a new one
					if e.health == 0:
						enemies.pop(enemies.index(e))
						newEnemy()

		# If ammo is on the screen
		if ammo.x < screenWidth and ammo.x > 0:
			ammo.x += ammo.vel # Move the ammo
		else:
			projectiles.pop(projectiles.index(ammo))

	# Different ways to check if a key is pressed.
	# - Can check the event as above, but that won't account for keys being held down
	# - Can put all of the pressed keys into a list -> going to do this:
	keys = pygame.key.get_pressed()

	# Ammo
	if keys[pygame.K_SPACE] and space_up:
		space_up = False
		if p1.left:
			facing = -1
		else:
			facing = 1
		# Make sure the ammo is coming from the middle of the man
		# Setting radius to 5 and color to black (RGB)
		projectiles.append(projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 5, black, facing))
	# If the spacebar has been released, flip this boolean so that another ammo can be shot
	if not keys[pygame.K_SPACE]:
		space_up = True
	
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
