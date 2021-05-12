def solution(array):
	j=0
	i=1
	results=[]
	while j<len(array):
		count=0
		if i<len(array): 
			while array[i]==array[i-1]+1:
				if i<len(array)-1:
					i+=1
					count+=1
				else:
					i+=1
					count+=1
					break

		if count>=2:
			results.append(str(array[j])+'-'+str(array[j]+count))
		elif count==1:
			results.append(str(array[j])+','+str(array[j+count]))
		else:
			results.append(str(array[j]))
		j=i
		i+=1
		
	return ','.join(results)

if __name__=='__main__':
	array = [-3,-2,-1,5,6,7,9,11,12,13,15,16]
	print solution(array)