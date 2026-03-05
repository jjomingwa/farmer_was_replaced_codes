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

def mixed_worker_logic(start_x):
    # 각 드론은 자신의 열에서 시작하여 체인을 따라가며 심음
    for start_y in range(WORLD_SIZE):
        go(start_x, start_y)
        
        # 1. 비어있는 공간일 때 체인 시작 (Grass는 Grassland에서 심을 수 있음)
        if get_entity_type() == None:
            # 시작 지면 확인: Grass를 심으려면 Grassland 필요
            if get_ground_type() == Grounds.Soil:
                till() # 200틱 소모하여 Grassland로 전환
            plant(Entities.Grass)
            
            # 2. 체인 추적 (최대 5단계)
            for i in range(5):
                companion = get_companion()
                if companion == None:
                    break
                    
                target_type = companion[0]
                pos = companion[1]
                tx = pos[0]
                ty = pos[1]
                
                go(tx, ty)
                
                # 3. 타겟 위치가 비어있을 때 지면 상태 확인 후 식재
                if get_entity_type() == None:
                    current_ground = get_ground_type()
                    
                    if target_type == Entities.Grass:
                        if current_ground == Grounds.Soil:
                            till() # Soil -> Grassland
                    else:
                        if current_ground == Grounds.Grassland:
                            till() # Grassland -> Soil
                    
                    plant(target_type)
                else:
                    # 이미 누군가 심었으므로 체인 중단 (중복 방지)
                    break

def mega_mixed_cultivation():
    # 1. 모든 드론을 사용하여 필드 초기화 (병렬 수확 및 동기화 대기)
    for_all(harvest)
    
    # 2. 32개의 드론 생성 (각 열 담당)
    drones = []
    for x in range(WORLD_SIZE):
        def spawn_worker(pos_x):
            def worker():
                mixed_worker_logic(pos_x)
            return spawn_drone(worker)
        
        d = spawn_worker(x)
        if d == None:
            # 드론 생성 실패 시 현재 드론이 직접 수행
            mixed_worker_logic(x)
        else:
            drones.append(d)

    # 3. 모든 드론의 작업 완료 대기
    for i in range(len(drones)):
        wait_for(drones[i])
        
    # 4. 최종 수확 (보너스 배율 적용됨)
    for_all(harvest)
