#Sotiria Kastana, 2995

import sys
import heapq
from heapq import nlargest
import time

mal_dict = dict()
males = open('males_sorted.txt','r')
K = int(sys.argv[1])
minheap = [0]*K
joins = []
start_time_h = time.time()

def f(a,b):
	c = a + b
	return c

for male in males:
	age_mal = int(male.split(', ')[1])
	marital_mal = male.split(', ')[8] 
	if age_mal >= 18 and marital_mal[0:7] != 'Married' :
		if male.split(', ')[1] in mal_dict:
			VAL = [] 
			value = male.split(', ')[0]+', '+male.split(', ')[1]+', '+male.split(', ')[25]
			VAL = mal_dict.get(male.split(', ')[1])
			VAL.append(value)
			mal_dict.update({male.split(', ')[1] : VAL})
		else:
			VAL = [] 
			value = male.split(', ')[0]+', '+male.split(', ')[1]+', '+male.split(', ')[25]
			VAL.append(value)
			mal_dict.update({male.split(', ')[1] : VAL})
			
with open('females_sorted.txt') as females:
	female = females.readline()
	while female:
		age_fem = int(female.split(', ')[1])
		marital_fem = female.split(', ')[8] 
		if age_fem >= 18 and marital_fem[0:7] != 'Married' :
			if female.split(', ')[1] in mal_dict:	
				MAL = mal_dict.get(female.split(', ')[1])
				for md in range(0,len(MAL)):
					res0 = MAL[md].split(', ')[0] 					
					res1 = female.split(', ')[0] 					
					r1= float(MAL[md].split(', ')[2])
					r2=float(female.split(', ')[25])
					res = f(r1,r2)					
					result = res0 +', '+ res1    
					if len(joins)<K:
						heapq.heappush(joins, (res, result))
					else:
						min_join = float(joins[0][0])
						if min_join >= res:					
							break;									
						else: 
							heapq.heappushpop(joins, (res, result))	


		female = females.readline()

minheap = nlargest(K, joins)

k=1
for mh in minheap:
	print(str(k)+'. pair: '+str(mh[1].split(', ')[0])+','+str(mh[1].split(', ')[1])+' score: '+str(mh[0]))
	k+=1

ht = time.time()-start_time_h
print('\n'+'The execution time of B top-k join algorithm is : '+str(ht)+' '+'secs'+'\n')
