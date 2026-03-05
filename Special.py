from Config import *
from __builtins__ import *
import random 

def bomool(D):
	while True:
		# 방향 순서 정의 (북:0, 동:1, 남:2, 서:3)
		dirs = [North, East, South, West]
		direction = 0  # 초기 방향: 북쪽
		if D == "right": # 오른쪽 우선
			DA = [1, 0, 3, 2]
		elif D == "left": # 왼쪽 우선
			DA = [3, 0, 1, 2]
		elif D == "forward": # 직진 우선(오른쪽 차선)
			DA = [0, 1, 3, 2]
		while True:
			# 현재 방향 기준 우선순위: 오른쪽(+1), 직진(+0), 왼쪽(+3), 후진(+2)
			# % 4 연산을 통해 인덱스 범위를 0~3으로 유지
			for i in DA:
				next_dir_idx = (direction + i) % 4
				target = dirs[next_dir_idx]
				if can_move(target):
					move(target)
					direction = next_dir_idx
					break  # 이동 성공 시 우선순위 체크 중단
				
			# 이동 후 보물이 있는지 확인
			if get_entity_type() == Entities.Treasure:
				harvest()
				plant(Entities.Bush)
				#다시 심기#
				substance = WORLD_SIZE * 2**(num_unlocked(Unlocks.Mazes) - 1)
				use_item(Items.Weird_Substance, substance)

def bomool_right():
	bomool("right")

def bomool_left():
	bomool("left")

def bomool_forward():
	bomool("forward")

