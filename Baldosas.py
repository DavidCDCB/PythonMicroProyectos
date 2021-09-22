def crearM():
	m=[[0,0,0,1,1],[0,1,0,0,1],[0,0,1,0,0],[1,0,0,1,0],[1,1,0,0,0]]
	return m
	
def Llenar(m,i,j):
	if(m[i][j]==0):
		
		if(j<len(m[0])-1 and m[i][j+1]==0):
			m[i][j+1]=2
			m[i][j]=2
			
			if(i<len(m)-1):
				j+=1
				if(j==len(m[0])):
					i+=1
					j=0
				Llenar(m,i,j)
			
		if(i<len(m)-1 and m[i+1][j]==0):
			m[i+1][j]=2
			m[i][j]=2
			
			if(i<len(m)-1):
				j+=1
				if(j==len(m[0])):
					i+=1
					j=0
				Llenar(m,i,j)
			
		if(j>len(m[0])-1 and m[i][j-1]==0):
				m[i][j-1]=2
				m[i][j]=2
				
				if(i<len(m)-1):
					j+=1
					if(j==len(m[0])):
						i+=1
						j=0
					Llenar(m,i,j)
			
		if(i>len(m)-1 and m[i-1][j]==0):
			m[i-1][j]=2
			m[i][j]=2
			
			if(i<len(m)-1):
				j+=1
				if(j==len(m[0])):
					i+=1
					j=0
				Llenar(m,i,j)

	if(i<len(m)-1 or j<len(m[0])-1):
		j+=1
		if(i<len(m)-1 and j==len(m[0])):
			i+=1
			j=0
		Llenar(m,i,j)

		
def verM(m):
	for i in range(len(m)):
		print(m[i])
		
		
m=crearM()
verM(m)
Llenar(m,0,0)
print()
verM(m)
