from __builtins__ import *
from Move import *
from Mega_Crops import *
from Crops import *
from Special import *
from functions import *
from Config import *

def cactus():
	go_zero()
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			gplant(Entities.Cactus)
			move(North)
		go_next_bottom()
		
def first_plant_square(WORLD_SIZE, entity):
	for i in range(WORLD_SIZE):
		for j in range(WORLD_SIZE):
			till()
			gplant(entity)
			move(North)
		for j in range(WORLD_SIZE):
			move(South)
		move(East)


for i in range(WORLD_SIZE): #수확 후 심기
	for j in range(WORLD_SIZE):
		harvest()
		plant(Entities.Cactus)
		move(North)
	move(East)
	
	
	