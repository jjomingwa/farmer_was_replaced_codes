from __builtins__ import *
from Config import *

def first_plant_square(entity):
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			gplant(entity)
			move(North)
		for j in range(WORLD_SIZE):
			move(South)
		move(East)
		

def gplant(entity): #1행에 해바라기 심는 심기함수
	if get_pos_y() == 0:
		plant(Entities.Sunflower)
		return plant(Entities.Sunflower)
	else:
		plant(entity)
		return plant(entity)

def gal():
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			if j == 0:
				plant(Entities.Sunflower)
			move(North)
		move(East)

def sort(size, direction):
		for i in range(size - 1):
			if measure() > measure(direction):
					swap(direction)
			for j in range(size - 2 - i):
				move(direction)
				if measure() > measure(direction):
					swap(direction)
			if direction == North:
				for j in range(size - 2 - i): #돌아오기
					move(South)		
			if direction == East:
				for j in range(size - 2 - i): #돌아오기
					move(West)	
						
def line_till_plant_cactus(): #열 경작 후 심기
	for i in range(WORLD_SIZE): 
		till()
		plant(Entities.Cactus)
		move(North)

def line_plant(entity): #열 심기
	for i in range(WORLD_SIZE):
		plant(entity)
		move(North)		

def line_till(): #열 경작
	for i in range(WORLD_SIZE):
		till()
		move(North)		
				
def area_till_plant_cactus(): #전체 경작 후 심기
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			plant(Entities.Cactus)
			move(North)
	move(East)

