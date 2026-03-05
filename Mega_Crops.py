from __builtins__ import *
from Config import *
from Move import *
from functions import *

def mega_tree(x): #0이나 1을 받는다.
	while True:
		for i in range(4):
			for j in range(WORLD_SIZE):
				if (j + 1 - x) % 2: 
					harvest()
					plant(Entities.Tree)
					move(North)
				else: 
					harvest()
					move(North)
			for j in range(4):
				move(East)

def mega_pum():
	for i in range(6):
		if i % 2: #up
			for j in range(5):
				till()
				plant(Entities.Pumpkin)
				move(South)
			till()
			plant(Entities.Pumpkin)
		else: #down
			for j in range(5):
				till()
				plant(Entities.Pumpkin)
				move(North)
			till()
			plant(Entities.Pumpkin)
		move(East)
	for i in range(6):
		move(West)

	while True:
		big = 1
		while big != 0:
			big = 0
			for i in range(6):
				if i % 2: #up
					for j in range(5):
						if can_harvest() == False: 
							big = 1
							plant(Entities.Pumpkin)
						move(South)
					if can_harvest() == False: 
						big = 1
						plant(Entities.Pumpkin)
				else: #down
					for j in range(5):
						if can_harvest() == False: 
							big = 1
							plant(Entities.Pumpkin)
						move(North)
					if can_harvest() == False: 
						big = 1
						plant(Entities.Pumpkin)				
				move(East)
			for i in range(6):
				move(West)
		harvest()

def mega_carrot():
	for i in range(WORLD_SIZE / max_drones()):
		for j in range(WORLD_SIZE):
			till()
			plant(Entities.carrot)
			move(North)
		for j in range(max_drones()):
			move(East)
	while True:
		for i in range(WORLD_SIZE / max_drones()):
			for j in range(WORLD_SIZE):
				harvest()
				plant(Entities.carrot)
				move(North)
			for j in range(max_drones()):
				move(East)

def mega_cactus_first():
	line_till()
	line_plant(Entities.Cactus)
	sort(WORLD_SIZE, North)
	n = get_pos_x()
	go(0, WORLD_SIZE - n - 1)
	sort(WORLD_SIZE, East)
	
def mega_cactus():
	line_plant(Entities.Cactus)
	sort(WORLD_SIZE, North)
	n = get_pos_x()
	go(0, WORLD_SIZE - n - 1)
	sort(WORLD_SIZE, East)
	
def mega_cactus_16():#메가 선인장 16드론
	drone = []
	## 드론 생성 및 메가 선인장 심기 ##
	for i in range(WORLD_SIZE - 1):  
		drone.append(spawn_drone(mega_cactus_first))
		move(East)
	mega_cactus_first()
	#드론 소멸 기다리기#
	for i in range(WORLD_SIZE - 1):
		wait_for(drone[i])
	harvest()

	#반복#
	while True:
		for i in range(WORLD_SIZE - 1):  
			drone.append(spawn_drone(mega_cactus))
			move(East)
		mega_cactus()
		for i in range(WORLD_SIZE-1):
			wait_for(drone[i])
		harvest()
