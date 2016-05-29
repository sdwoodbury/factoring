#!/usr/bin/python

'''
the script takes an integer as a command line argument. The integer should be at least 50. have tested up to 3000. 1024 and 2048 will be done in a reasonable amount of time but 3000 may take a few minutes.

the script outputs the public key, private key, and the modulus, which should be the number of bits specified at the command line

I have appended a test of the encryption to the end of the file. it works as follows:
	pass the message, public key, and modulus, to encode()
	encode() returns an array
	pass the array, private key, and modulus, to decode()
	decode retuns the original message

the test prints out: the message, the encoded array, and the decoded message.


1) description of multiplication algorithm:
	python provides native support for long numbers. it  uses arbitrary-
	length precision. Python uses karastuba's algorithm for long 
	multiplication.

2) description of modualr reduction algorithm:
	Python provides native support for modular reduction. It uses a
	function called l_divmod to perform modular reductions.  To find 
	a mod b, python simply calculates a - b(floor(a/b))

3) description of modular exponentiation algorithm:
		I did not use a library for modular exponentiation. I implemented 
	a left-right modular exponentiation algorithm. I represented the
	exponent as a sequene of bits and iterated over them, high to low.  
		At bits which were not zero, I multiplied the base, a, 
	by 2^(bit location) mod n, and set it equal to a variable, r. 
	After each successive bit i would continue to multiply r
	by either r mod n, if the bit was zero, or r * a mod n, if the 
	bit was 1. 

python's source code for these functions is: 
https://github.com/python-git/python/blob/master/Objects/longobject.c

example key: bit length: 100

public key:  89055526231269632611864235243 

private key:  150757934664043511687051290787 

modulus:  663660874948676603482626535219


 message to encode: "I deserve an A"

enoded message:  [137427453925425015916865563705L, 91641633427099256671523656449L, 146325561723688040812563457161L, 349553220220560970942161116118L, 421492561297145170311776403569L, 349553220220560970942161116118L, 480759952125824858617399016247L, 340519905271574293969781208286L, 349553220220560970942161116118L, 91641633427099256671523656449L, 261613667171149384622411945890L, 250768093565165126266106196551L, 91641633427099256671523656449L, 410841994378904427478940777055L]

decoded message: "I deserve an A"
'''


import sys, random, time, math
import trial_div

def bits(n): #source: from http://eli.thegreenplace.net/2009/03/28/efficient-modular-exponentiation-algorithms
	z = []
	while n > 0:
		z.append(n % 2)
		n /=2
	return z

def lr(a, b, n): #source: from http://eli.thegreenplace.net/2009/03/28/efficient-modular-exponentiation-algorithms
	r = 1
	for x in bits(b)[::-1]:
		r = r * r % n
		if x == 1:
			r = r * a % n
	return r

def witness(a, n): 
	b = n-1
	copy = b
	exp = 0
	while b % 2 == 0:
		exp += 1
		b = b / 2
	u = copy / pow(2, exp)
	x0 = lr(a, u, n)
	x1 = 0
	for i in range(0, exp):
		x1 = lr(x0, 2, n)
		if x1 == 1 and x0 != 1 and x0 != (n - 1):
			return 1
		x0 = x1
	if x1 != 1:
		return 1
	return 0
	
#returns 1 if not prime, 0 if prime
def prime(n):
	if n < 549999991:
		if trial_div.prime(n) == True:
			return 0
		else:
			return 1		
	pseudo = lr(2, n - 1, n)
	l = e_e(pseudo, n)
	if l[0] != 1:
		return 1
	for i in range(0, 40):
		a = random.randint(1, n - 1)
		if witness(a, n) == 1:
			return 1
	return 0


def strip_powers_of_two(c, p, q, gamma, delta): #source: http://www.ucl.ac.uk/~ucahcjm/combopt/ext_gcd_python_programs.pdf
 	c = c / 2
 	if (p % 2 == 0) and (q % 2 == 0):
 		p, q = p//2, q//2
 	else:
 		p, q = (p + delta)//2, (q - gamma)//2
	return c, p, q
def e_e(a,b): #source: http://www.ucl.ac.uk/~ucahcjm/combopt/ext_gcd_python_programs.pdf
 	"""Extended binary GCD.
 	Given input a, b the function returns d, s, t
 	such that gcd(a,b) = d = as + bt."""
 	u, v, s, t, r = 1, 0, 0, 1, 0
 	while (a % 2 == 0) and (b % 2 == 0):
 		a, b, r = a//2, b//2, r+1
 	alpha, beta = a, b
 	while (a % 2 == 0):
 		a, u, v = strip_powers_of_two(a, u, v, alpha, beta)
 	while a != b:
 		if (b % 2 == 0):
 			b, s, t = strip_powers_of_two(b, s, t, alpha, beta)
 		elif b < a:
			 a, b, u, v, s, t = b, a, s, t, u, v
 		else:
			 b, s, t = b - a, s - u, t - v
	return (2 ** r) * a, s, t

def go(bits):
	p_len = bits / 2
	#make p
	random.seed()
	p = random.getrandbits((int)(p_len)) #random.randint(pow(2, p_len - 1), pow(2, p_len) - 1)
	if p % 2 == 0:
		p += 1
	
	while prime(p) == 1:
		p += 2
	
	q_len = bits - math.ceil(math.log(p, 2))
	q = random.getrandbits((int)(q_len)) # random.randint(pow(2, q_len - 1), pow(2, q_len) - 1)
	if q % 2 == 0:
		q += 1

	while prime(q) == 1:
		q += 2
	
	phi = (p-1)*(q-1)
	n = p * q
	
	e = random.randint(2, phi)
	if e % 2 == 0:
		e += 1

	while e_e(e, phi)[0] != 1:
		e += 2

	l = e_e(e, phi)
	d = l[1]

	return [d, e, n]


