from __builtins__ import *
from Config import *

def go_zero():
	x = get_pos_x()
	y = get_pos_y()
	for i in range(x):
		move(West)
	for i in range(y):
		move(South)


def go_next_bottom():
	pos = (get_pos_x(), get_pos_y())
	for i in range(pos[1]):
		move(South)
	move(East)
	
def go(x, y):
	x_ = x - get_pos_x()
	y_ = y - get_pos_y()
	if x_ < 0:
		for i in range(-x_):
			move(West)
	else:
		for i in range(x_):
			move(East)
	
	if y_ < 0:
		for i in range(-y_):
			move(South)
	else:
		for i in range(y_):
			move(North)
			