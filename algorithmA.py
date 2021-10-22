#Sotiria Kastana, 2995

import sys
import heapq
from heapq import nlargest
import time

K = int(sys.argv[1])
k = 0
mal_max = 0.0
mal_cur = 0.0
fem_max = 0.0
fem_cur = 0.0
iw_mal = 0.0
iw_fem = 0.0
mal_dict = dict()
fem_dict = dict()
Q = [] 
T = 0.0
valid_males = 0
valid_females = 0
start_time_h = time.time()
all_lines = 0
eof_males = 0
eof_females = 0

def f(a,b):
	c = a + b
	return c
	
def GetValidLine(file):  								#returns valid line, 0 if eof
	line = file.readline()	
	while line:
		age = int(line.split(', ')[1])
		marital = line.split(', ')[8]
		if age>=18 and marital[0:7] != 'Married':
			return line
		else:
			line = file.readline()
	return 0  									
			
def probe(dict,age,gender,id,cur,Q):
	dict_list = dict.get(age)
	result=[0,0,0]
	for dl in range(0,len(dict_list)):
		weight = float(dict_list[dl].split(', ')[2])
		sum = f(cur,weight) 
		if gender == 'Female': 
			res0 = dict_list[dl].split(', ')[0]
			res1 = id		
		else:
			res0 = id
			res1 = dict_list[dl].split(', ')[0]
		sum_neg = -sum
		result = [sum_neg , res0, res1]
		heapq.heappush(Q, result)
	return Q

		
with open('males_sorted.txt') as males:
	with open('females_sorted.txt') as females:
		#1st male & 1st female
		k = 0
		gender = 'Male'
		line_mal = GetValidLine(males)
		valid_males += 1
		mal_max = float(line_mal.split(', ')[25])	
		mal_cur = float(line_mal.split(', ')[25])	
		VAL = []
		value = line_mal.split(', ')[0]+', '+line_mal.split(', ')[1]+', '+line_mal.split(', ')[25]
		VAL.append(value)
		mal_dict.update({line_mal.split(', ')[1] : VAL})

		gender = 'Female'
		line_fem = GetValidLine(females)	
		valid_females += 1		
		fem_max = float(line_fem.split(', ')[25])
		fem_cur = float(line_fem.split(', ')[25])
		f1 = f(mal_max,fem_cur)
		f2 = f(mal_cur,fem_max)
		T = max(f1,f2)
		VAL = []
		value = line_fem.split(', ')[0]+', '+line_fem.split(', ')[1]+', '+line_fem.split(', ')[25]
		VAL.append(value)
		fem_dict.update({line_fem.split(', ')[1] : VAL})
		
		if line_fem.split(', ')[1] in mal_dict:
			Q = probe(mal_dict,line_fem.split(', ')[1],gender,line_fem.split(', ')[0],fem_cur,Q)
			
		if len(Q):		
			F_neg = float(Q[0][0])
			F = -F_neg
			if F >= T:
				print(str(k+1)+'. pair: '+str(Q[0][1])+','+str(Q[0][2])+' score: '+str(F))
				k += 1
				heapq.heappop(Q)	
		gender = 'Male'
		
		#for each male & each female
		while k<K:

			if gender == 'Male':
				line_mal = GetValidLine(males)
				if line_mal != 0:
					valid_males += 1
					mal_cur = float(line_mal.split(', ')[25])
					f1 = f(mal_max,fem_cur)
					f2 = f(mal_cur,fem_max)
					T = max(f1,f2)

					if line_mal.split(', ')[1] in mal_dict: 
						VAL = []
						value = line_mal.split(', ')[0]+', '+line_mal.split(', ')[1]+', '+line_mal.split(', ')[25]
						VAL = mal_dict.get(line_mal.split(', ')[1])
						VAL.append(value)
						mal_dict.update({line_mal.split(', ')[1] : VAL})
					else:
						VAL = []
						value = line_mal.split(', ')[0]+', '+line_mal.split(', ')[1]+', '+line_mal.split(', ')[25]
						VAL.append(value)
						mal_dict.update({line_mal.split(', ')[1] : VAL})
			
					if line_mal.split(', ')[1] in fem_dict:
						Q = probe(fem_dict,line_mal.split(', ')[1],gender,line_mal.split(', ')[0],mal_cur,Q)	
				else:
					eof_males = 1
				gender = 'Female'	
				
			else:
				line_fem = GetValidLine(females)	
				if line_fem != 0:    
					valid_females += 1
					fem_cur = float(line_fem.split(', ')[25])
					f1 = f(mal_max,fem_cur)
					f2 = f(mal_cur,fem_max)
					T = max(f1,f2)
					
					if line_fem.split(', ')[1] in fem_dict: 
						VAL = []
						value = line_fem.split(', ')[0]+', '+line_fem.split(', ')[1]+', '+line_fem.split(', ')[25]
						VAL = fem_dict.get(line_fem.split(', ')[1])
						VAL.append(value)
						fem_dict.update({line_fem.split(', ')[1] : VAL})
					else:
						VAL = []
						value = line_fem.split(', ')[0]+', '+line_fem.split(', ')[1]+', '+line_fem.split(', ')[25]
						VAL.append(value)
						fem_dict.update({line_fem.split(', ')[1] : VAL})
					
					if line_fem.split(', ')[1] in mal_dict:	
						Q = probe(mal_dict,line_fem.split(', ')[1],gender,line_fem.split(', ')[0],fem_cur,Q)
				else:
					eof_females = 1
				gender = 'Male'
	
			while Q and k<K:		
				F_neg = float(Q[0][0])
				F = -F_neg
				if F >= T:
					print(str(k+1)+'. pair: '+str(Q[0][1])+','+str(Q[0][2])+' score: '+str(F))
					k += 1
					heapq.heappop(Q)
				else:
					break;	
					
			if eof_males == 1 and eof_females == 1:
				while Q and k < K :
					F_neg = float(Q[0][0])
					F = -F_neg
					print(str(k+1)+'. pair: '+str(Q[0][1])+','+str(Q[0][2])+' score: '+str(F))	
					heapq.heappop(Q)
					k += 1
					
all_lines = valid_males + valid_females				
ht = time.time()-start_time_h
print('\n'+'The execution time of A top-k join algorithm is : '+str(ht)+' '+'secs'+'\n')
print('algorithm reads : '+str(valid_males)+' valid lines from males.sorted & '+str(valid_females)+' valid lines from females.sorted')
print('So, all valid lines are: '+str(all_lines))
