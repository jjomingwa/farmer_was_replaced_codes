from __builtins__ import *
from Config import *

def tree():
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			if j % 2 == i % 2: 
				plant(Entities.Tree)
				use_item(Items.Fertilizer)
				move(North)
			else:
				harvest()
				use_item(Items.Fertilizer)
				move(North)
		move(East)
	while True:
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				if j % 2 == i % 2: 
					harvest()
					plant(Entities.Tree)
					use_item(Items.Fertilizer)
					move(North)
				else: 
					harvest()
					use_item(Items.Fertilizer)
					move(North)
			move(East)
			
def carrot():
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			plant(Entities.carrot)
			move(North)
		move(East)
	while True:
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				harvest()
				plant(Entities.carrot)
				move(North)
			move(East)
			
def cact():
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			if j == 0:
				plant(Entities.Sunflower)
			else:
				plant(Entities.Cactus)
			move(North)
		move(East)
	while True:
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				harvest()
				if j == 0:
					plant(Entities.Sunflower)
				else:
					plant(Entities.Cactus)
				move(North)
			move(East)

def pum():
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			plant(Entities.Pumpkin)
			move(North)
		move(East)
	while True:
		big = 1
		while big != 0:
			big = 0
			for i in range(WORLD_SIZE):
				for j in range(WORLD_SIZE):
					if can_harvest(): 
						move(North)
					else: 
						big = 1
						plant(Entities.Pumpkin)
						move(North)
				move(East)
		harvest()
		
def mixed_cult():
	while True:
		while True:
			x = get_pos_x()
			y = get_pos_y()
			type, (x_, y_) = get_companion()
			#print( get_companion(), x_ - x, y_ - y)
			
			if x_ - x >= 0:					
				for i in range(x_ - x):
					move(East)
			else:
				for i in range(x - x_):
					move(West)
			if y_ - y >= 0:
				for i in range(y_ - y):
					move(North)
			else:
				for i in range(y - y_):
					move(South)
				
			if type == Entities.Carrot:
				till()
				plant(type)
			else:
				plant(type)
		#print(get_entity_type())
		go_zero()
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				harvest()
				move(North)
			move(East)					
			
				
				
			
