# Find number of prime numbers upto 2 million

def find_prime_numbers(n):
	primes = [2,3]
	result = 2
	if n<2:
		return 0
	t = 5
	while True:
		is_prime = is_prime_number(t,primes)
		if is_prime:
			result += 1
			primes.append(t)
		t += 1
		if t>n:
			break
	return result
	
def is_prime_number(t,checklist):
	is_prime = True
	for p in checklist:
		if p*p > t:
			break
		if t%p == 0:
			is_prime = False
			break
	return is_prime
	
if __name__ == '__main__':
	p = find_prime_numbers(2000000)
	print (p)
			
	
