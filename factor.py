#!/usr/bin/python

import sys, random, math
from fractions import gcd
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

def f(x, n, m):
	return ( lr(x, 2, n)  - m) % n

def factor(n):
	for m in [1, 1, 1]:
		random.seed()
		a = random.randint(2, n - 1)
		b = a
		b = f(f(a, n, m), n, m)
		a = f(a, n, m)
		c = gcd(a - b, n)
		counter = 0
		stop = math.floor(pow((float)(n), .25))
		while c == 1 and counter < stop:
			if (a <= 0 or b <= 0):
				#print "error in factor"
				return 0
			a = f(a, n, m)
			b = f(f(b, n, m), n, m)
			c = gcd(abs(a - b), n)
			counter += 1
		if(c * (n // c) == n):
			return c
		print "fail"
	print "error in factor"
	return 0


