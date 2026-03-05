from __builtins__ import *
from Config import *
from Move import go_zero

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

def for_all(f):
    drones = []
    def row_task():
        for _ in range(WORLD_SIZE - 1):
            f()
            move(East)
        f()
    
    for _ in range(WORLD_SIZE):
        # 1틱 비용의 num_drones()로 200틱 비용의 spawn_drone() 호출을 방어
        if num_drones() < max_drones():
            d = spawn_drone(row_task)
            if d == None:
                row_task() # 실패 시 직접 수행
            else:
                drones.append(d)
        else:
            row_task() # 한도 도달 시 직접 수행
        move(North)
    
    # 생성된 모든 드론이 작업을 마칠 때까지 대기
    for i in range(len(drones)):
        wait_for(drones[i])
    
    # 모든 작업 완료 후 원점 복귀 (동기화 보장)
    go_zero()
