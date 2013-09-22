test = [ [ [0]*2 for j in range(2) ] for k in range(3)]

test[0][0][0]+=1

for i in range(0,3):
	for j in range(0,2):
		for k in range(0,2):
			print i,j,k,test[i][j][k]