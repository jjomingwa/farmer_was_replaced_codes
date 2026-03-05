from __builtins__ import *
from Move import *
from Mega_Crops import *
from Crops import *
from Special import *
from functions import *

set_execution_speed(2.5)
world_size = 4
set_world_size(world_size)
go_zero()
for i in range(10):
	move(East)