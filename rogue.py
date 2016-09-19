import pygame
import math
import time
import random
import sys

pygame.init()

clock = pygame.time.Clock()  
f_size = f_width, f_height = 640, 480
size = width, height = 480,480 
screen = pygame.display.set_mode((f_size),pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

img_player = pygame.image.load('images/player.jpg')
img_enemy = pygame.image.load('images/enemy.jpg')
player_pos = (0,0)
done = False
removed = []
num_squares = 256
square_size = width/math.sqrt(num_squares)
square_size = (int(square_size))-2
squares = []

for x in range(int(math.sqrt(num_squares))):
		for y in range(int(math.sqrt(num_squares))):
			pygame.draw.rect(screen, (255,255,255),pygame.Rect(x*square_size,y*square_size,square_size,square_size),1)
			squares.append((x*square_size,y*square_size))

floor_num = 0

map_square_size = 3

#Class to handle enemy logic
#Implemented:
#Implementing: Movement Logic/Pathfinding
#To be implemented: Combat, Multiple Enemy types
class Enemy: #x is index 0 y is index 1 for loc, player is opposite
	health = 0
	damage = 0
	attack_range = 1
	speed = 1
	loc = (-1,-1)
	lastSpace = None

	def __init__(self):
		self.loc = removed[random.randint(0,len(removed)-1)]
		floor = zip(*info[0])

	def move(self):
		arrived = False
		openS = []
		closedS = []
		path = []
		last_dist = 0
		closedS.append(self.loc)

		while not arrived:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						done = True
						pygame.quit()
						sys.exit()
			
			if(tuple(map(sum,zip(closedS[-1], (0,-1))))) in removed and (tuple(map(sum,zip(closedS[-1], (0,-1))))) not in closedS:
				openS.append(tuple(map(sum,zip(closedS[-1], (0,-1)))))
			if(tuple(map(sum,zip(closedS[-1], (0,1))))) in removed and (tuple(map(sum,zip(closedS[-1], (0,1))))) not in closedS:
				openS.append(tuple(map(sum,zip(closedS[-1], (0,1))))) 
			if(tuple(map(sum,zip(closedS[-1], (-1,0))))) in removed and (tuple(map(sum,zip(closedS[-1], (-1,0))))) not in closedS:
				openS.append(tuple(map(sum,zip(closedS[-1], (-1,0)))))
			if(tuple(map(sum,zip(closedS[-1], (1,0))))) in removed and (tuple(map(sum,zip(closedS[-1], (1,0))))) not in closedS:
				openS.append(tuple(map(sum,zip(closedS[-1], (1,0)))))
			
			scores = {}

			for sq in openS:
				if sq == player_pos:
					break
					arrived = True
				startToPoint = last_dist+1
				pointToEnd = math.hypot(sq[0] - player_pos[1], sq[1] - player_pos[0])
				scores[sq] = startToPoint + pointToEnd
				
			if not arrived:
				lowest = []
				for (point, score) in scores.iteritems():
					if lowest == []:
						lowest = [(point, score)]
					else:
						if score < lowest[0][1]:
							lowest = [(point, score)]
						elif score == lowest:
							lowest.append((point,score))
				path.append(lowest[-1][0])
				closedS.append(lowest[-1][0])
		self.loc = path[0]

#Handles drawing the mini map to the screen.
def show_map(floor, screen, enemy):
	floor = zip(*floor)
	for x in range( 60+floor_num ):
		for y in range( 60+floor_num ):
			if (y,x) == player_pos: #player
				pygame.draw.rect(screen, (102,51,0),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),0)
			elif (x,y) == enemy.loc: #enemy
				pygame.draw.rect(screen, (255,0,255),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),0)
			elif floor[y][x] == 'x': #wall
				pygame.draw.rect(screen, (255,0,0),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),0)
					
			elif floor[y][x] == 'S': #start location
				pygame.draw.rect(screen, (0,0,255),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),0)
				
			elif floor[y][x] == 'E': #end of floor
				pygame.draw.rect(screen, (0,255,150),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),0)
				
			else:	#walkable ground
				pygame.draw.rect(screen, (255,255,255),pygame.Rect(462 + x*map_square_size,y*map_square_size,map_square_size,map_square_size),1)
			
			
# def place_room(s, floor, removed):
# 	size = random.randint(10, 20)

# 	x = random.randint(1,s-12)
# 	y = random.randint(1,s-12)

# 	for iy in range(0,size):
# 		for ix in range(0,size):
# 			if iy == 0 or ix == 0:
# 				floor[y+iy][x+ix] = '-'
# 			else:
# 				floor[y+iy][x+ix] = '|'
# 			removed.append((x,y))


#The main logic for generating a dungeon floor.
#The basic idea for floor generation is this:
#	1. A 2D list is created to represent the floor, initially filled with all walls.
#	2. A random starting location is chosen within the list, and that location is turned into a walkable floor space.
#	3. The generator chooses a random direction, and moves 1 space in that direction, turning that into a floor as well. 
#	4. This is repeated over and over until a dungeon is created.
#	5. Finally a start location is chosen, as well as an exit location that must be a certain distance from the start. 
def gen_floor(floor_num): 
	floor = []
	removed = []
	size = 60 + floor_num

	for y in range(size):
		floor.append(['x'] * size)

	#choose starting location
	starty = random.randint(1,size-2)
	startx = random.randint(1,size-2)

	y, x = starty, startx
	removed.append((x,y))

	for i in range(6000):
		works = False
		while not works:
			UpDownLeftRight = random.randint(0,3)
			if UpDownLeftRight == 0: #up
				if y > 1 and (x,y-1):
					works = True
			if UpDownLeftRight == 1: #down
				if y < size-2 and (x,y+1):
					works = True
			if UpDownLeftRight == 2: #left
				if x > 1 and (x-1,y):
					works = True
			if UpDownLeftRight == 3: #right
				if x < size-2 and (x+1,y):
					works = True
		if UpDownLeftRight == 0: #up
			y -= 1
		if UpDownLeftRight == 1: #down
			y += 1
		if UpDownLeftRight == 2: #left
			x -= 1	
		if UpDownLeftRight == 3: #right
			x += 1
		floor[y][x] = '|'
		if (x,y) not in removed:
			removed.append((y,x))
	
	exit_set = False
	while not exit_set:
		exit = removed[random.randint(0,len(removed)-1)]
		if exit != (startx,starty) and abs(math.hypot(exit[0] - starty, exit[1] - startx)) > 20:
			exit_set = True
	
	floor[starty][startx] = 'S'
	floor[exit[0]][exit[1]] = 'E'
	info = [floor, removed, (startx, starty), exit]
	return info

#Handles the movement of the player
#Uses wasd for movement, holding the spacebar allows for quicker movement. 
#Also checks for the user trying to quit with the escape key.
def player_movement(player_pos, enemy):
	move_left = (0,-1)
	move_right = (0,1)
	move_up = (-1,0)
	move_down = (1,0)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_SPACE]:
		if keys[pygame.K_w]:
			if player_pos[1] > 1:
				if info[0][player_pos[1]][player_pos[0]-1] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_up)))
					enemy.move()
		if keys[pygame.K_s]:
			if player_pos[1] < 451:
				if info[0][player_pos[1]][player_pos[0]+1] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_down)))
					enemy.move()
		if keys[pygame.K_a]:
			if player_pos[0] > 1:
				if info[0][player_pos[1]-1][player_pos[0]] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_left)))
					enemy.move()
		if keys[pygame.K_d]:
			if player_pos[0] < 451:
				if info[0][player_pos[1]+1][player_pos[0]] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_right)))
					enemy.move()
		
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				done = True
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_w:
				if info[0][player_pos[1]][player_pos[0]-1] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_up)))
					enemy.move()
			if event.key == pygame.K_s:
				if info[0][player_pos[1]][player_pos[0]+1] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_down)))
					enemy.move()
			if event.key == pygame.K_a:
				if info[0][player_pos[1]-1][player_pos[0]] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_left)))
					enemy.move()
			if event.key == pygame.K_d:
				if info[0][player_pos[1]+1][player_pos[0]] != 'x':
					player_pos = tuple(map(sum,zip(player_pos,move_right)))
					enemy.move()
	return player_pos

#Handles drawing the visible portion of the map onto the screen.
#Converts the map list into the various types of squares as denoted by the ascii map.
def draw_playarea():
	screen.fill((0,0,0))
	for x in range( player_pos[1]-(8), player_pos[1]+(8) ):
		for y in range( player_pos[0]-(8), player_pos[0]+(8) ):
			try:
				if (x,y) == enemy.loc: #enemy
					screen.blit(img_enemy, ((x-player_pos[1]+8)*square_size,(y-player_pos[0]+8)*square_size))

				elif info[0][x][y] == 'x': #wall
					pygame.draw.rect(screen, (255,0,0),pygame.Rect((x-player_pos[1]+8)*square_size,(y-player_pos[0]+8)*square_size,square_size,square_size),0)
					
				elif info[0][x][y] == 'S': #start location
					pygame.draw.rect(screen, (0,0,255),pygame.Rect((x-player_pos[1]+8)*square_size,(y-player_pos[0]+8)*square_size,square_size,square_size),0)
					pass
					
				elif info[0][x][y] == 'E': #end of floor
					pygame.draw.rect(screen, (255,127,0),pygame.Rect((x-player_pos[1]+8)*square_size,(y-player_pos[0]+8)*square_size,square_size,square_size),0)
					
				else: #walkable ground
					pygame.draw.rect(screen, (255,255,255),pygame.Rect((x-player_pos[1]+8)*square_size,(y-player_pos[0]+8)*square_size,square_size,square_size),1)
				
			except:
				pass
					
		screen.blit(img_player, player_coord) #overlay the player


info = gen_floor(floor_num)

player_pos = info[2]
exit_loc = info[3]
removed = info[1]
player_coord = (square_size * math.sqrt(num_squares)/2,square_size * math.sqrt(num_squares)/2)
enemy = Enemy()
show_map(info[0], screen, enemy)

while not done:
	player_pos = player_movement(player_pos, enemy)			
	draw_playarea()
	show_map(info[0], screen, enemy)

	#test if the player reached the end of the floor
	if player_pos[1] == exit_loc[0] and player_pos[0] == exit_loc[1]:
		floor_num+=2
		info = gen_floor(floor_num)
		show_map(info[0], screen, enemy)
		player_pos = info[2]
		removed = info[1]
		exit_loc = info[3]

	pygame.display.flip()

	clock.tick(60) #lock the game to 60 fps for consistency
