"""
Signpost.py

Solver for 'Signpost' type puzzles.

Follow direction of the arrows and cover every square.

Express the puzzle as a top-down left to right comma separated list of directions.  If a square has a number, separate the direction with a hyphen '-'.

Up Arrow - U
Down Arrow - D
Left Arrow - L
Right Arrow - R
Up and Left Arrow - UL
Up and Right Arrow - UR
Down and Left Arrow - DL
Down and Right Arrow - DR
Puzzle End - Star

The first numbered block should be '1', or the puzzle will start in the upper left by default.

"""

from collections import deque

def idx_to_pos(idx,dims):
	return (idx%dims[0],idx//dims[1])

def pos_to_idx(pos,dims):
	return pos[1]*dims[0]+pos[0]

def pretty_print(path,dims):
	for y in range(dims[1]):
		for x in range(dims[0]):
			print(str(path.index((x,y))+1).zfill(2),end=' ')
		print()
	print()

def solve(puzzle,dims):

	puzzle = puzzle.strip().upper()
	arrows =     []
	known_idxs = []
	q = deque()

	deltas = { 'U'   : (0,-1),
		   'D'   : (0,1),
		   'L'   : (-1,0),
		   'R'   : (1,0),
		   'UL'  : (-1,-1),
		   'UR'  : (1,-1),
		   'DL'  : (-1,1),
		   'DR'  : (1,1),
		   'STAR': (0,0) }


	for entry in puzzle.split(','): 
		if '-' in entry:
			arrow,step = entry.split('-')
			arrows.append(arrow)
			known_idxs.append(int(step))
		else:
			arrows.append(entry)
			known_idxs.append(-1)

	if 1 in known_idxs:
		q.append((idx_to_pos(known_idxs.index(1),dims),[idx_to_pos(known_idxs.index(1),dims)],{idx_to_pos(known_idxs.index(1),dims),}))
	else:
		q.append(((0,0),[(0,0)],{(0,0),}))
		
	known_idxs_set = set(known_idxs)
	
	while q:
		pos,path,seen = q.popleft()
		x,y = pos
		if len(path) == dims[0]*dims[1] and arrows[pos_to_idx(pos,dims)] == 'STAR':
			pretty_print(path,dims)
			return # Find only one solution
		elif len(path) < dims[0]*dims[1]:
			dx,dy = deltas[arrows[pos_to_idx(pos,dims)]]
			nx,ny = x+dx,y+dy
			while nx >=0 and ny >=0 and nx < dims[0] and ny < dims[1] and (dx,dy) != (0,0):
				if (nx,ny) not in seen:
					if len(path)+1 not in known_idxs_set or len(path)+1 == known_idxs[pos_to_idx((nx,ny),dims)]:
						q.append(((nx,ny),path+[(nx,ny)],{*seen,(nx,ny)}))
				nx,ny = nx+dx,ny+dy
	

if __name__ == "__main__":
	
	# Example 4x4
	solve('DR-1,DR,R,DL,R,L,DL,UL,R,L,DR,DL,R,U,U-14,Star',(4,4))
	
	# Example 4x4, free ends
	solve('R,D,D,D,R,UR,R,L,U,Star,DL,UL,U,L,UL,L-1',(4,4))
	
	# Example 5x5
	solve('D-1,DR,L,D,DL,R-21,UR,DR,UR,L-20,R,UR,D,R,D,U,R,UR,L,DL,R,U-7,L-5,UL,Star',(5,5))
	
	# Example 3x5
	solve('D,D,DL,UR,UR,D,R,UR,DL,R,D,UL,U,L,Star',(3,5))
