#Starting with a 1-indexed array of zeros and a list of operations, for each operation add a value to 
#each of the array element between two given indices, inclusive. Once all operations have been performed,
# return the maximum value in your array.

'''
if __name__ == '__main__':
	n,m = input().split(' ')
	n,m = int(n),int(m)
	operator_array = []
	arr = [0]*n
	# print(arr)
	for _ in range(m):
		a,b,k = map(int,input().split(' '))
		operator_array.append((a,b,k))
	
	for a,b,k in operator_array:
		for i in range(a,b+1):
			arr[i-1]+=k
	# print (arr)
	print(max(arr))
		
	'''
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the arrayManipulation function below.
def arrayManipulation(n, queries):
	arr = [0]*n
	for q in queries:
		a = q[0]-1
		b = q[1]-1
		k = q[2]
		arr = arr[:a] + [e+k for e in arr[a:b+1]] + arr[b+1:]
		
	
	return max(arr)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nm = input().split()

    n = int(nm[0])

    m = int(nm[1])

    queries = []

    for _ in range(m):
        queries.append(tuple(map(int, input().rstrip().split())))

    result = arrayManipulation(n, queries)

    fptr.write(str(result) + '\n')

    fptr.close()

	
