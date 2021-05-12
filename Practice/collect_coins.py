# Get maximum coins in a bag i.e maximum price minimum weight

def collect_coins(prices,weights):
	prices = normalize(prices)
	weights = normalize(weights)
	r1=[]
	r2=[]
	tmp_prices = prices[:]
	tmp_weights = weights[:]
	w,i = get_min_and_index(tmp_weights)
	p = tmp_prices[i]
	while len(tmp_weights)>0:
		r1.append((w,p))
		w2,i2 = get_min_and_index(tmp_weights)
		p2,j2 = get_max_and_index(tmp_prices)
		if p2 - p > w - w2:
			p = p2
			w = tmp_weights[j2]
		elif w -w2 > p2-p:
			w = w2
			p = tmp_price[i2]
	return r1
	
	
	
	
def get_min_and_index(arr):
	m = min(arr)
	i = arr.index(m)
	del arr[i]	
	return m,i

def get_max_and_index(arr):
	m = max(arr)
	i = arr.index(m)
	del arr[i]	
	return m,i

def normalize(a):
	max_ = max(a)
	a = [i/float(max_) for i in a]
	return a

if __name__ == '__main__':
	p = [1,4,2,6,7,9]
	w = [3,6,9,1,2,7]
	r = collect_coins(p,w)
	print (r)
